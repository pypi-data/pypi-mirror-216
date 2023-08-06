"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

import yaml
from aimltools.ts.utils import Boto3ClientFactory, Boto3ClientException, PGTSTableDataAccess
import logging
import os
from datetime import datetime, timedelta
from io import BytesIO, StringIO

logger = logging.getLogger(__name__)


class PGtoS3Connector():
    def __init__(self, **kwargs):
        if 'config_file' in kwargs:
            config_file = kwargs.pop('config_file')
            with open(config_file) as file:
                config_dict = yaml.load(file, Loader=yaml.BaseLoader)

            self.pg_connection_args = config_dict['PG']['CONNECTION']
            self.pg_setup_args = config_dict['PG']['SETUP']
            self.S3_connection_args = config_dict['S3']['CONNECTION']
            self.offload_args = config_dict['PARAMS']['OFFLOAD_DATA']
        else:
            self.pg_connection_args = kwargs.pop('pg_connection_args', None)
            self.pg_setup_args = kwargs.pop('pg_setup_args', None)
            self.S3_connection_args = kwargs.pop('s3_connection_args', None)

        USE_GATEWAY = True
        s3 = Boto3ClientFactory().create()
        if USE_GATEWAY:
            aws_account_id = self.S3_connection_args['AWS_ACCOUNT_ID']
            gw_s3_access_role = self.S3_connection_args['GW_S3_ACCESS_ROLE']
            cert_path = self.S3_connection_args['CERT_PATH']  # <Ceritifcate file with path (.crt file) >
            cert_key_path = self.S3_connection_args['CERT_KEY_PATH']  # <Ceritifcate file key with path (.crt file) >
            bucket = self.S3_connection_args['BUCKET']
            proxy = self.S3_connection_args['PROXY']
            proxy_dict = {
                "http": proxy,
                "https": proxy,
                "ftp": proxy
            }
            request_url = self.S3_connection_args['REQUEST_URL']
            request_url = request_url + aws_account_id
            boto3_gw_client_factory = Boto3ClientFactory()
            boto3_gw_client_factory = boto3_gw_client_factory.set_service_account(os.environ['dia_ml_service_account']) \
                .set_aws_account_id(aws_account_id) \
                .set_aws_access_role(gw_s3_access_role) \
                .set_certificate_path(cert_path) \
                .set_certificate_key_path(cert_key_path) \
                .set_gw_url(request_url) \
                .set_proxies(proxy, proxy, proxy)
            try:
                self.s3 = boto3_gw_client_factory.create_using_gw(os.environ['dia_ml_service_passwd'])
                logger.info("self.s3 object created")
            except Boto3ClientException as exc:
                logging.error(exc.message)

        self.pg = PGTSTableDataAccess(**self.pg_connection_args)
        self.pg.connect()

        self.pg.setup_mappings(table_name=self.pg_setup_args['TABLE'],
                               name_fld=self.pg_setup_args['NAME_FLD'],
                               time_fld=self.pg_setup_args['TIME_FLD'],
                               value_fld=self.pg_setup_args['VALUE_FLD'],
                               status_fld=self.pg_setup_args['STATUS_FLD'])

    def offload_data(self, **kwargs):
        end_time = kwargs.pop('end_time', 'auto')
        start_time = kwargs.pop('start_time', 'auto')
        
        window_unit = self.offload_args['WINDOW_UNIT']
        window_width = int(self.offload_args['WINDOW_WIDTH'])
        delete_on_offload = self.offload_args['DELETE_ON_OFFLOAD']
        num_units_data_retained = int(self.offload_args['NUM_UNITS_DATA_RETAINED'])
        
        
        # window_unit = kwargs.pop('window_unit', 'days')
        # window_width = kwargs.pop('window_width', 1)
        # delete_on_offload = kwargs.pop('delete_on_offload', False)

        table_name = self.pg_setup_args['TABLE']
        bucket = self.S3_connection_args['BUCKET']
        time_fld = self.pg_setup_args['TIME_FLD']

        if end_time == 'auto':
            end_time = datetime.now() - timedelta(num_units_data_retained)
            end_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        else:
            end_time = datetime.strptime(end_time, '%Y-%m-%d')
            end_time = end_time.replace(tzinfo=None)

        if start_time == 'auto':
            query = "SELECT MIN({}) FROM {}".format(time_fld, table_name)
            df = self.pg.execute_select(query, params=None)
            start_time = df['min'][0]
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        else:
            start_time = datetime.strptime(start_time, '%Y-%m-%d')
            start_time = start_time.replace(tzinfo=None)

        if start_time > end_time:
            raise Exception("'start_date' is later than 'end_date'")

        
        logger.info("Start time: {}".format(start_time))
        logger.info("End time: {}".format(end_time))

        self.generate_windows(start_time, end_time, window_width=window_width, window_unit=window_unit)

        for time_period in self.time_periods:
            p_start = time_period[0].strftime('%Y-%m-%d %H:%M:%S')
            p_end = time_period[1].strftime('%Y-%m-%d %H:%M:%S')
            df = self.pg.read_data(start=p_start, end=p_end)
            year_month = str(time_period[0].year) + "-" + str('{:02d}'.format(time_period[0].month))

            filename = "offloaded_data/" + table_name + "/" + year_month + "/" + "start_" + p_start + "_" + "end_" + p_end + ".parquet"
            logger.info(filename)
            self.dataframe_to_s3(s3_client=self.s3, input_datafame=df, bucket_name=bucket, filepath=filename,
                                 format='parquet')

            if delete_on_offload:
                self.pg.delete_data(p_start, p_end)

        self.pg.disconnect()
        logger.info("Data offloaded from {} to {}".format(start_time, end_time))

    def download_data(self, **kwargs):
        pass

    def generate_windows(self, start_time, end_time, window_width, window_unit):
        if window_unit == 'days':
            interval = timedelta(days=window_width)
        if window_unit == 'hours':
            interval = timedelta(seconds=window_width * 3600)

        self.time_periods = []

        period_start = start_time
        while period_start < end_time:
            period_end = min(period_start + interval, end_time)
            self.time_periods.append((period_start, period_end))
            period_start = period_end

    def dataframe_to_s3(self, s3_client, input_datafame, bucket_name, filepath, format):
        if format == 'parquet':
            out_buffer = BytesIO()
            input_datafame.to_parquet(out_buffer, index=False)
            logger.info("Temp parquet file created and stored in-memory")

        elif format == 'csv':
            out_buffer = StringIO()
            input_datafame.to_parquet(out_buffer, index=False)
            logger.info("Temp CSV file created and stored in-memory")

        s3_client.put_object(Bucket=bucket_name, Key=filepath, Body=out_buffer.getvalue())
        logger.info("Upload to S3 complete")
