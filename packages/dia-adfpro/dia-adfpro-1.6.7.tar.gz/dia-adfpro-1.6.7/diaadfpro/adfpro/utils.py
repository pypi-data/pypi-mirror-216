"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

import logging
import math
import os
import pathlib
import pickle
import random
import sys
import time as tm
import traceback
from datetime import datetime, timezone, timedelta

from aimltools.ts.utils.pg_utils import PGDataAccessException
from tzlocal import get_localzone

import ciso8601
import dash_bootstrap_components as dbc
from botocore.exceptions import ClientError
from dash import dcc, html
import dask.dataframe as dd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz
import yaml
from aimltools.ts.preprocessing import DataPreparation
from aimltools.ts.utils import PGDataAccess, PGTSTableDataAccess, DateTimeUtils, Boto3ClientFactory, \
    Boto3ClientException

import hashlib
import psycopg2

from diaadfpro.adfpro.constants import ADFPC

logger = logging.getLogger(__name__)


class ADFPDateUtils:
    @staticmethod
    def get_full_day_interval(start_date: str, end_date: str) -> list:
        # given 2 input dates, returns a date time interval dt1, dt2 such that:
        # - dt1 = 00:00:00 of the day that includes start_date
        # - dt2 = 23:59:59 of the day that includes end_date
        # datetimes have tz set to UTC
        start_date_obj = datetime.combine(ciso8601.parse_datetime(start_date), datetime.min.time())
        end_date_obj = datetime.combine(ciso8601.parse_datetime(end_date), datetime.min.time())
        start_date_obj = pytz.utc.localize(start_date_obj)
        end_date_obj = pytz.utc.localize(end_date_obj)
        end_date_obj = end_date_obj + timedelta(hours=23, minutes=59, seconds=59)  # always consider the full day
        return [start_date_obj, end_date_obj]

    @staticmethod
    def utc_set(dt_str: str) -> datetime:
        date_obj = ciso8601.parse_datetime(dt_str)
        date_obj = pytz.utc.localize(date_obj)
        return date_obj

    @staticmethod
    def get_current_dt(tzaware=True):
        if tzaware:
            utc_dt = datetime.now(timezone.utc)  # UTC time
            return utc_dt.astimezone()  # local time
        else:
            return datetime.now()

    @staticmethod
    def is_tz_aware(d):
        return d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None

    @staticmethod
    def datestr_to_dt(dt_str, tzaware=False):
        # turn date into datetime and set tz to UTC
        date_obj = ciso8601.parse_datetime(dt_str)
        if tzaware:
            date_obj = pytz.utc.localize(date_obj)
        return date_obj

    @staticmethod
    def generate_time_windows(start_time, end_time, window_unit, window_width):

        time_periods = []

        if not window_width and not window_unit:
            time_periods.append((start_time, end_time))
            return time_periods

        if window_unit == 'days':
            interval = timedelta(days=window_width)
        if window_unit == 'hours':
            interval = timedelta(seconds=window_width * 3600)

        period_start = start_time
        while period_start < end_time:
            period_end = min(period_start + interval, end_time)
            time_periods.append((period_start, period_end))
            period_start = period_end

        return time_periods


class DataQualityException(Exception):
    def __init__(self, message="Data Quality Exception"):
        self.message = message
        super().__init__(self.message)


class IOUtilsException(PGDataAccessException):
    pass


class IOUtils:

    def write_features(df, dbp, dbpwd):
        try:
            db = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],
                              dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
            db.connect()
            tbl_name = dbp[ADFPC.STR_FEAT_TABLE_NAME]
            rc = db.write_results_bulk(df, tbl_name)
            if rc != len(df):
                raise Exception("Error writing feature rows to {} table".format(tbl_name))
            else:
                logger.info("Successfully added {} feature rows to {} table".format(rc, tbl_name))
        finally:
            db.disconnect()

    @staticmethod
    def write_results(df_results, res_table_name, user, passwd, host, port, db, ssl, ssl_cert):
        if len(df_results) == 0:
            logger.info("Empty dataset: no need to write to database")
            return 0

        db = PGDataAccess(user, passwd, host, port, db, ssl, ssl_cert)
        db.connect()
        record_cnt = db.write_results_bulk(df_results, res_table_name)
        db.disconnect()
        if record_cnt == 0:
            logger.info("Zero records written to database")
        return record_cnt

    @staticmethod
    def erase_classification_results(dbp, dbpwd, eqm_id):
        try:
            db = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],
                              dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])

            db.connect()
            db.execute_simple_delete(dbp[ADFPC.STR_CLS_TABLE_NAME], key_fld='eqpm_id', key_val=eqm_id)
            logger.info("Done erasing classification results for component {} corresponding to previously trained model".format(eqm_id))
        finally:
            db.disconnect()

    @staticmethod
    def insert_classification_results(dbp, dbpwd, df_classif_results):
        if len(df_classif_results) == 0:
            logger.info("Empty dataset: no need to write to database")
            return 0

        try:
            db = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],
                              dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])

            db.connect()
            record_cnt = db.write_results_bulk(df_classif_results, dbp[ADFPC.STR_CLS_TABLE_NAME])
            logger.info("Done inserting classification results ({} records)".format(record_cnt))
            return record_cnt
        except PGDataAccessException as e:
            #likely a foreign key violation or a unique key violation...
            raise IOUtilsException(e)
        finally:
            db.disconnect()

    @staticmethod
    def read_features_old(starttime, endtime, user, passwd, host, port, db, ssl, ssl_cert, ft_table_name, feat_names):
        logger.info("Loading features from {} to {}".format(starttime, endtime))
        db = PGTSTableDataAccess(user, passwd, host, port, db, ssl, ssl_cert)
        db.setup_mappings(ft_table_name, 'vtag', 'vtime', 'vvalue', 'svalue')
        db.connect()
        df = db.read_data(starttime, endtime, feat_names, columns=['vtag', 'vtime', 'vvalue'],
                          order_by=[['vtime', 'asc']])
        db.disconnect()

        return df

    @staticmethod
    def read_features(starttime, endtime, dv, dbp, dbpwd, FEATURE_LIST):
        # Fetch data
        logger.info("Loading features from {} to {}".format(starttime, endtime))
        start = tm.time()

        db = PGTSTableDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],
                                 dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])

        db.setup_mappings(dbp[ADFPC.STR_FEAT_TABLE_NAME], 'vtag', 'vtime', 'vvalue', 'svalue')
        db.connect()
        df = db.read_data(starttime, endtime, FEATURE_LIST[dv], columns=['vtag', 'vtime', 'vvalue'],
                          order_by=[['vtime', 'asc']])
        db.disconnect()
        end = tm.time()
        print("Done loading {} feature values in {}s".format(len(df), end - start))
        return df

    @staticmethod
    def normalize(df_ft):
        dp = DataPreparation()

        [scaler, df_train_ft] = dp.normalize(df_ft)
        logger.info("Normalized data")

        return [scaler, df_train_ft]

    @staticmethod
    def get_feature_matrix(dbp, tstart, tend, feature_list, fillna=True, dbpwd=None):
        logger.info("Load features")
        pwd = dbpwd
        if pwd is None:
            pwd = dbp[ADFPC.STR_PASS]

        df_train = IOUtils.read_features_old(tstart,
                                             tend,
                                             dbp[ADFPC.STR_USER],
                                             pwd,
                                             dbp[ADFPC.STR_HOST],
                                             dbp[ADFPC.STR_PORT],
                                             dbp[ADFPC.STR_DBNAME],
                                             dbp[ADFPC.STR_SSL],
                                             dbp[ADFPC.STR_SSL_CERT_PATH],
                                             dbp[ADFPC.STR_FEAT_TABLE_NAME],
                                             feature_list)
        logger.info("Loaded {} feature rows".format(len(df_train)))

        if len(df_train) == 0:
            return None

        logger.info("Check data quality")
        dp = DataPreparation()
        [quality, quality_report] = dp.check_data_quality(df_train, feature_list, 0.4)

        if quality == False:
            logger.error("Bad data quality")
            _ = [logger.error("{}: {}".format(key, value)) for key, value in quality_report.items()]
            raise DataQualityException("Bad data quality encountered in time interval {}-{}".format(tstart, tend))

        logger.info("Transform features into feature matrix")
        df_train_ft = dp.get_feature_matrix(df_train, feature_list)
        logger.info("Successfully loaded {} cycles".format(len(df_train_ft)))
        if fillna:
            logger.info("Filling NA's...")
            df_train_ft = dp.fill_na(df_train_ft)

        return df_train_ft

    @staticmethod
    def read_classification_avgs(model_lst, starttime, endtime, dbp, dbpwd, as_dict=True):
        try:
            model_lst_str = "{}".format(tuple(model_lst))
            if len(model_lst) == 1:
                model_lst_str = model_lst_str.replace(',', '')
            logger.info(
                "Calculating averages per equipment. Model(s): {}, start: {}, end: {}".format(model_lst_str, starttime,
                                                                                              endtime))

            db = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],
                              dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
            db.connect()

            start = tm.time()
            df = db.execute_select(
                "select eqpm_id, avg(score) from {} where modl_id in {} and evnt_time > %(starttm)s and evnt_time <= %(endtm)s group by eqpm_id".format(
                    dbp[ADFPC.STR_CLS_TABLE_NAME], model_lst_str), {'starttm': starttime, 'endtm': endtime})
            end = tm.time()
            logger.info("Done calculating averages in {}s".format(end - start))

            if as_dict:
                avg_dict = {}
                for index, row in df.iterrows():
                    avg_dict[row['eqpm_id']] = row['avg']
                return avg_dict
            else:
                return df
        finally:
            db.disconnect()

    @staticmethod
    def read_classification_results(model_lst, starttime, endtime, eqm_id, dbp, dbpwd, num_threads=8, window_unit=None,
                                    window_width=None):
        try:
            model_lst_str = "{}".format(tuple(model_lst))
            if len(model_lst) == 1:
                model_lst_str = model_lst_str.replace(',', '')
            logger.info("Loading classification results. Model(s): {}, start: {}, end: {}, equipment id: {}".format(
                model_lst_str, starttime, endtime, eqm_id))

            db = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],
                              dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
            db.connect()

            start = tm.time()
            if eqm_id is None:
                df = db.execute_select(
                    "select * from {} where modl_id in {} and (evnt_time >= %(starttm)s and evnt_time <= %(endtm)s) order by evnt_time asc".format(
                        dbp[ADFPC.STR_CLS_TABLE_NAME], model_lst_str), {'starttm': starttime, 'endtm': endtime})
            else:
                df = db.execute_select(
                    "select * from {} where modl_id in {} and (evnt_time >= %(starttm)s and evnt_time <= %(endtm)s) and eqpm_id = %(eqid)s order by evnt_time asc".format(
                        dbp[ADFPC.STR_CLS_TABLE_NAME], model_lst_str),
                    {'starttm': starttime, 'endtm': endtime, 'eqid': eqm_id})

            df["utcsec"] = df.evnt_time.apply(lambda x: DateTimeUtils.datetime_to_epoch(x))
            end = tm.time()
            logger.info("Done loading {} cycles in {}s".format(len(df), end - start))
            return df
        finally:
            db.disconnect()

    @staticmethod
    def fetch_user_id(username, dbp, dbpwd):

        pg = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT], dbp[ADFPC.STR_DBNAME],
                          dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
        pg.connect()
        table = dbp[ADFPC.STR_USERS_TABLE]
        user_id = pg.execute_simple_select(table, "user_name", username)['user_id'].values[0]
        pg.disconnect()

        return user_id

    @staticmethod
    def upsert_table_adpro_equipment_model(dbp, dbpwd, start_time, end_time, current_ts, user_id, component_id,
                                           model_id):
        table = dbp[ADFPC.STR_EQUIPMENT_RETRAIN_TABLE]
        # transform into an upsert statement (assumings
        # NB: RISK OF SQL INJECTION HERE!! MODIFY ASAP TO USE PARAMETRIZED STATEMENTS!!!!
        sql_statement = """INSERT INTO {}(eqpm_id, model_id, start_train, end_train, last_trained, retrained_by)
                            VALUES({}, '{}', '{}', '{}', '{}', {})
                            on conflict (eqpm_id, model_id) DO
                            UPDATE SET start_train = '{}', end_train = '{}', last_trained =  '{}', retrained_by = {}
                            WHERE {}.eqpm_id = {} and {}.model_id = '{}'
                            """.format(table, component_id, model_id, start_time, end_time, current_ts, user_id,
                                       start_time, end_time, current_ts, user_id,
                                       table, component_id, table, model_id)
        logger.info("Triggering query to update model info: {}".format(sql_statement))
        conn = psycopg2.connect(database=dbp[ADFPC.STR_DBNAME], user=dbp[ADFPC.STR_USER], password=dbpwd,
                                host=dbp[ADFPC.STR_HOST], port=dbp[ADFPC.STR_PORT], sslmode=dbp[ADFPC.STR_SSL],
                                sslrootcert=dbp[ADFPC.STR_SSL_CERT_PATH])
        conn.autocommit = True
        cursor = conn.cursor()
        rs = cursor.execute(sql_statement)
        conn.commit()
        conn.close()

    @staticmethod
    def update_adpro_users(dbp, dbpwd, current_ts, user_id):

        table = dbp[ADFPC.STR_USERS_TABLE]

        sql_statement = """UPDATE {} 
                               SET user_last_logged_in = '{}'
                               WHERE user_id = {};""".format(table, current_ts, user_id)

        logger.info("Querry: {}".format(sql_statement))

        conn = psycopg2.connect(database=dbp[ADFPC.STR_DBNAME], user=dbp[ADFPC.STR_USER], password=dbpwd,
                                host=dbp[ADFPC.STR_HOST], port=dbp[ADFPC.STR_PORT], sslmode=dbp[ADFPC.STR_SSL],
                                sslrootcert=dbp[ADFPC.STR_SSL_CERT_PATH])
        conn.autocommit = True
        cursor = conn.cursor()
        rs = cursor.execute(sql_statement)
        conn.commit()
        conn.close()

    @staticmethod
    def read_equipments(dbp, dbpwd):
        try:
            logger.info("Loading equipments")
            db = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],
                              dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
            db.connect()
            start = tm.time()
            # sqlstmt = "select eqpm_id,eqm_name from dia_aas_global.core_equipments where eqpm_id in (select distinct eqpm_id from dia_aas_global.adpro_cl_results)"
            # TODO: make this more robust
            sqlstmt = "select eqpm_id,eqm_name from {} where eqpm_id > 1;".format(dbp[ADFPC.STR_CMP_TABLE_NAME])
            data = db.execute_select(sqlstmt, None)
            end = tm.time()
            logger.info("Done loading {} equipments in {}s".format(len(data), end - start))
            return data
        finally:
            db.disconnect()

    @staticmethod
    def build_pkl_path(sitename, linename, eqmname, model_name):
        # pkl path: <site>_<parent>_<component name>_<model name>.pkl
        return "{}_{}_{}_{}.pkl".format(sitename, linename, eqmname, model_name)

    @staticmethod
    def save_pkl(model_metadata, pkl_basepath_str, pkl_fname_str):
        p = pathlib.Path(pkl_basepath_str, pkl_fname_str).resolve()
        logger.info("Dump to pkl {}".format(p))
        with open(p, 'wb') as f:
            pickle.dump(model_metadata, f)

        return str(p)

    @staticmethod
    def read_pkl(model_name, eqmname, linename, sitename, basepath):
        filename = IOUtils.build_pkl_path(sitename, linename, eqmname, model_name)
        return IOUtils.read_pkl_direct(pathlib.Path(basepath, filename).resolve())

    @staticmethod
    def read_pkl_direct(filepath: pathlib.Path):
        logger.info("Read from pkl {}".format(filepath))
        with open(filepath, 'rb') as f:
            return pickle.load(f)

    # loads data from parquet files contained in a given folder
    # structure of data in files reflect piarchive.picomp structure
    @staticmethod
    def load_component_data(parquet_folder_name, signal_col, tag_col, time_col, taglist, timeinterval,
                            order_columns=True):
        df = dd.read_parquet(parquet_folder_name)

        if len(taglist) > 0:
            df = df[df[tag_col].isin(taglist)]

        if len(timeinterval) == 2:
            df = df[(df[time_col] >= timeinterval[0]) & (df[time_col] <= timeinterval[1])]

        df = df.compute()

        try:
            df.drop(["svalue", "status", "flags"], axis=1, inplace=True)
        except:
            pass

        df[signal_col] = pd.to_numeric(df[signal_col], errors='coerce')
        df.dropna(inplace=True)

        if order_columns:
            df.sort_values(by=["time"], inplace=True)

        df = df.reset_index(drop=True)
        return df


class YMLConfigReader:
    @staticmethod
    def version():
        return yaml.__version__

    @staticmethod
    def read_full_path(p):
        with open(p, "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def read(path, filename):
        p = pathlib.PurePath(path, filename)
        return YMLConfigReader.read_full_path(p)

    @staticmethod
    def write(d, fullpath):
        with open(fullpath, "w") as f:
            yaml.safe_dump(d, f, default_flow_style=False)


class PlotUtils:

    @staticmethod
    def generate_shap_plot_data(dct_points, shap_explainer, data_scaler, time_delta_s, dv, dbp, dbpwd, FEATURE_LIST):
        logger.info("Start generating SHAP plot data")
        logger.info(str(dct_points))

        if dct_points == None:
            return FEATURE_LIST[dv], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        else:
            DATEFMT = '%Y-%m-%d %H:%M'
            pt = dct_points['points'][0]
            sdate = str(pt['x'])
            sdate_utcsec = str(pt['customdata'][0])
            date_time_obj = datetime.strptime(sdate, DATEFMT)
            later = date_time_obj + timedelta(seconds=time_delta_s)
            edate = later.strftime(DATEFMT)
            logger.info("Filtering data corresponding to clicked point: start={}, end={}".format(sdate, edate))
            logger.info(edate)

            sd = date_time_obj
            ed = later

            df_test = IOUtils.read_features(sd, ed, dv, dbp, dbpwd, FEATURE_LIST)

            # Prepare data
            dp = DataPreparation()
            df_test_ft = dp.get_feature_matrix(df_test, FEATURE_LIST[dv])
            arr_test_ft_norm = data_scaler.transform(dp.fill_na(df_test_ft))

            d = {}
            for i, colname in enumerate(df_test_ft.columns):
                d[colname] = arr_test_ft_norm[:, i]
                i += 1
            df_test_ft_norm = pd.DataFrame.from_dict(d)
            # Calculate SHAP valus
            logger.info("Type of df_test_ft_norm = {}".format(type(df_test_ft_norm)))
            logger.info("Size of df_test_ft_norm = {}".format(df_test_ft_norm.shape))
           
            
            shap_values = shap_explainer.shap_values(df_test_ft_norm)
            
            logger.info("DEBUG : Shap values = {}".format(shap_values))
            
            df_features = FEATURE_LIST[dv]
            dd = {}
            ii = 0
            for ev in df_features:
                dd[ev] = shap_values[:, ii]
                ii = ii + 1
            shap_values_df = pd.DataFrame(dd)
            v = []
            for i in shap_values_df.mean(axis=0):
                v.append(i)
            return df_features, v, sd, ed

    @staticmethod
    def get_empty_graph(graph_type):
        anomaly_msg = "Click Inspect to generate anomaly graph"
        shap_msg = "Click data point on anomaly graph to generate Shap explainations"
        box_msg = "Click data point on anomaly graph to generate box plot"
        data_missing_msg = "No data found in specified period"

        msg = ""
        if graph_type == 'anomaly_empty':
            msg = anomaly_msg

        if graph_type == 'shap_empty':
            msg = shap_msg

        if graph_type == 'box_empty':
            msg = box_msg

        if graph_type == 'No_data_empty':
            msg = data_missing_msg

        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": msg,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 10
                    }
                }
            ]
        )

        boxfig = dcc.Graph(figure=fig, )

        if graph_type == 'box_empty':
            return boxfig
        return fig

    @staticmethod
    def get_ohlc_graph(dbp, dbpwd, selected_tag, sd, ed, tf):

        db = PGTSTableDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],
                                 dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
        db.setup_mappings(dbp[ADFPC.STR_FEAT_TABLE_NAME], 'vtag', 'vtime', 'vvalue', 'svalue')
        db.connect()
        df = db.read_data(sd, ed, [selected_tag], columns=['vtag', 'vtime', 'vvalue'], order_by=[['vtime', 'asc']])
        db.disconnect()

        fig = PlotUtils.get_empty_graph("No_data_empty")
        if len(df) > 0:
            df = df.set_index('vtime')
            timeframe = str(int(tf) * 60) + "Min"
            dff = df['vvalue'].resample(timeframe).ohlc()
            fig = go.Figure(
                data=go.Ohlc(x=dff.index, open=dff['open'], high=dff['high'], low=dff['low'], close=dff['close']))

        return fig

    #  Function to Generate Anomaly graph
    @staticmethod
    def generate_anomaly_graph(start_time, end_time, dv, duration, graph_theme, datetime_format, dbp, dbpwd, Eqpm_id,site_name,line_no):
        # TODO: remove hard coded site and line
        st_line = "Site: "+str(site_name)+", Line: "+str(line_no)
        eq_detail = "Equipment: " + dv

        start_date_object = ADFPDateUtils.utc_set(start_time)
        end_date_object = ADFPDateUtils.utc_set(end_time)

        model_lst = ['ANNClassifier 3']

        df = IOUtils.read_classification_results(model_lst, start_date_object, end_date_object, Eqpm_id, dbp, dbpwd,
                                                 window_unit='hours', window_width=1)
        if df.shape[0] == 0:
            fig = PlotUtils.get_empty_graph("No_data_empty")
        else:
            df_agg = PlotUtils.aggregate(df, start_time, end_time, 600, datetime_format)
            fig = px.scatter(df_agg, x="time", y="value", hover_data=['time', 'utcsec'], height=300,
                             template=graph_theme)
            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
            fig.update_layout(transition_duration=500)

        return st_line, eq_detail, fig

    @staticmethod
    def generate_shap_plot(dv, clickData, graph_theme, classifier_dct: dict, dbp, dbpwd, FEATURE_LIST):
        #K.clear_session()

        data_scaler = classifier_dct["SCALER OBJECT"]
        shap_explainer = classifier_dct["EXPLAINER"]
        start_train = classifier_dct["TRAINSTART"]
        end_train = classifier_dct["TRAINEND"]
        
        logger.info("DEBUG: Size of artifact  = {} and explainer = {} , keys = {}".format(sys.getsizeof(classifier_dct), sys.getsizeof(shap_explainer),str(classifier_dct.keys())))
            
        [feat_list, v, sd, ed] = PlotUtils.generate_shap_plot_data(clickData, shap_explainer, data_scaler, 600, dv,
                                                                   dbp, dbpwd,
                                                                   FEATURE_LIST)
        #K.clear_session()

        data_shap = {}
        data_shap['Tags'] = feat_list
        data_shap['Shap_Values'] = v
        df_shap = pd.DataFrame.from_dict(data_shap)
        #K.clear_session()
        fig = px.bar(df_shap, x="Shap_Values", y="Tags", orientation='h', height=250, template=graph_theme)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        fig.update_layout(transition_duration=500)
        return fig, start_train, end_train, sd, ed

    @staticmethod
    def generate_box_plot(dv, dct_points, classifier_dct: dict, dbp, dbpwd, feature_list):

        #K.clear_session()

        train_boxplot_df = classifier_dct['TRAINING DATA']

        DATEFMT = '%Y-%m-%d %H:%M'
        pt = dct_points['points'][0]
        sdate = str(pt['x'])
        date_time_obj = datetime.strptime(sdate, DATEFMT)
        later = date_time_obj + timedelta(seconds=600)

        sd = date_time_obj
        ed = later

        df_test = IOUtils.read_features(sd, ed, dv, dbp, dbpwd, feature_list)

        # Prepare data
        dp = DataPreparation()
        df_test_ft = dp.get_feature_matrix(df_test, feature_list[dv])
        df_test_ft = dp.fill_na(df_test_ft)

        tags = df_test_ft.columns.tolist()
        tags.reverse()

        def create_single_boxplot(df_train, df_sample, tagname):
            fig = go.Figure()
            fig.add_trace(go.Box(x=df_sample, marker_color='#3D9970', name="Sample"))
            fig.add_trace(go.Box(x=df_train, marker_color='#646CFA', name="Train"))
            fig.update_layout(height=250, width=420, title_text='<b>' + tagname + '</b>', showlegend=False,
                              margin=dict(l=10, r=5, t=35, b=10), title_font_size=10)
            fig.update_traces(orientation='h')
            return fig

        def generate_dbc_row(boxplot_pair):
            dbc_cols = []
            for boxplot in boxplot_pair:
                dbc_cols.append(
                    dbc.Col(
                        dcc.Graph(
                            figure=boxplot
                        ),
                    )
                )
            row = dbc.Row(dbc_cols, style={"width": "100%"})
            return row

        i = 0
        dbc_row_list = []
        boxplot_pair = []
        for every in tags:
            f = create_single_boxplot(train_boxplot_df[every].tolist(), df_test_ft[every].tolist(), every)
            boxplot_pair.append(f)
            if i % 2 == 1:
                dbc_row = generate_dbc_row(boxplot_pair)
                dbc_row_list.append(dbc_row)
                boxplot_pair = []
            i = i + 1

        # add last boxplot (if number of tags is odd)
        if len(boxplot_pair) > 0:
            dbc_row = generate_dbc_row(boxplot_pair)
            dbc_row_list.append(dbc_row)

        plot_div = html.Div(
            dbc_row_list,
            style={"width": "100%"}
        )

        return plot_div

    @staticmethod
    def multicycle_plot(df, taglist, sample_ratio=0.1, seed=0, cycle_col="cycle", tag_col="tag", value_col="value",
                        dct_golden=None, out_path=None):
        ntags = len(taglist)
        nplot_rows = int(ntags / 2)
        cycle_list = list(df[cycle_col].unique())
        cycle_count = len(cycle_list)
        cycle_count_sampled = cycle_count
        if cycle_count_sampled > 100:
            cycle_count_sampled = max(100, math.ceil(cycle_count * sample_ratio))

        random.seed(seed)
        cycle_list = random.sample(cycle_list, int(cycle_count_sampled))

        fig, ax = plt.subplots(nplot_rows, 2, figsize=(18, 2.5 * nplot_rows))
        plt.subplots_adjust(wspace=0.2, hspace=0.5)

        logger.info("plotting {} of {} cycles".format(len(cycle_list), cycle_count))

        i = 1
        for tagn in taglist:
            logger.info("plotting {}, #{}".format(tagn, i))
            plt.subplot(nplot_rows, 2, i)
            dft = df[df[tag_col] == tagn]
            for cyclen in cycle_list:
                plt.plot(dft[dft[cycle_col] == cyclen][value_col].values, 'b', alpha=0.5)

            try:
                plt.plot(dct_golden[tagn], 'g', linewidth=4, alpha=0.9)
            except Exception as e:
                logger.error(e)
                logger.error("unable to plot golden for {}".format(tagn))
                pass

            plt.title("{}".format(tagn))
            i = i + 1
        if out_path is None:
            plt.show()
        else:
            plt.savefig(out_path)
            plt.close()

    @staticmethod
    def __numpy_aggregate(col_agg, col_val, datetime_format, start_epoch=-1, window_sz_sec=600):
        start_ts = start_epoch
        time_list = []
        value_list = []

        logger.info("start: {}, limit: {}".format(
            DateTimeUtils.epoch_to_string_tz(start_ts, datetime_format, timezone.utc),
            DateTimeUtils.epoch_to_string_tz(col_agg[-1], datetime_format, timezone.utc)))
        while start_ts < col_agg[-1]:
            end_ts = start_ts + window_sz_sec
            idx = np.arange(np.searchsorted(col_agg, start_ts), np.searchsorted(col_agg, end_ts))
            if len(idx) > 0:
                a = np.mean(col_val[idx])
                time_list.append(start_ts)
                value_list.append(a)
            start_ts = end_ts
        return [time_list, value_list]

    @staticmethod
    def __numpy_aggregate_df(df, datetime_format, start_epoch=-1, window_sz_sec=600):
        x1 = df["utcsec"].values
        x2 = df["score"].values
        [time_list, value_list] = PlotUtils.__numpy_aggregate(x1, x2, datetime_format, start_epoch=start_epoch,
                                                              window_sz_sec=window_sz_sec)
        d = {"utcsec": time_list, "value": value_list}
        df_agg = pd.DataFrame.from_dict(d)
        df_agg["time"] = df_agg.utcsec.apply(
            lambda x: DateTimeUtils.epoch_to_string_tz(x, datetime_format, timezone.utc))
        return df_agg

    @staticmethod
    def aggregate(df, start_date, end_date, window_sz_sec, datetime_format):
        logger.info("Start calculating MA using window size: {}".format(window_sz_sec))
        logger.info("Start date {}, end date {}".format(start_date, end_date))
        s = DateTimeUtils.string_to_epoch_ciso8601(start_date)
        start = tm.time()
        df_agg = PlotUtils.__numpy_aggregate_df(df, datetime_format, start_epoch=s, window_sz_sec=window_sz_sec)
        end = tm.time()
        logger.info("Done calculating MA in {}s".format(end - start))
        try:
            logger.info(
                "MA values: {}. Fist: {}, last: {}".format(len(df_agg), df_agg.time.values[0], df_agg.time.values[-1]))
        except:
            pass
        return df_agg


class AnomalySummaryUtils:

    @staticmethod
    def get_equipment_list(artifacts_path, model_name, components):

        equipments = {}
        eqpm_ids = {}
        dropdown_options = []
        classifier_pkl_paths = {}
        features_dict = {}

        for component in components:
            c_name = component.name
            c_id = component.id

            equipments[c_id] = c_name
            eqpm_ids[c_name] = c_id

            d = {}
            d['label'] = c_name
            d['value'] = c_name
            dropdown_options.append(d)

            tags = []
            for feature in component.features:
                tags.append(feature.name)

            features_dict[c_name] = tags
            classifier_pkl_paths[c_name] = str(pathlib.Path(artifacts_path, IOUtils.build_pkl_path(component.site.name,
                                                                                                   component.parent_component.name,
                                                                                                   c_name,
                                                                                                   model_name)).resolve())

        return equipments, eqpm_ids, dropdown_options, classifier_pkl_paths, features_dict
            
    @staticmethod
    def get_retrain_table(dbp, dbpwd, equipments):
        # Function to read data from "dia_aas_global.adpro_equipment_model"
        try:
            pg = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
            pg.connect()
            in_clause = "({})".format(','.join(['%s'] * len(equipments.values())))
            sql_stmt = ("SELECT b.eqpm_model_id, a.eqpm_id, a.eqm_name, b.model_id, b.start_train, b.end_train, b.last_trained from {} a, {} b "
                        "where a.eqpm_id = b.eqpm_id and a.eqm_name in {} "
                        "order by a.eqpm_id asc;").format(dbp[ADFPC.STR_CMP_TABLE_NAME], dbp[ADFPC.STR_EQUIPMENT_RETRAIN_TABLE], in_clause)
            data = pg.execute_select(sql_stmt, list(equipments.values()))
            pg.disconnect()
        finally:
            pg.disconnect()

        df_retrain = data
        df_retrain.rename(columns = {'eqpm_model_id':'id','eqm_name':'Component'}, inplace = True)
        return df_retrain
    

    @staticmethod
    def generate_tabdata(mdlist, dbp, dbpwd, equipments_dct):

        ct = datetime.now()
        #ct = ct - timedelta(days=67)       # This has to be removed for live data
        #ct = DateTimeUtils.string_to_datetime_ciso8601("2022-06-20 01:00:00")

        last_4h_start = ct - timedelta(hours=4)
        last_24h_start = ct - timedelta(days=1)
        last_week_start = ct - timedelta(days=7)
        last_4h_end = last_week_end = last_24h_end = ct

        avgs_4h = IOUtils.read_classification_avgs(mdlist, last_4h_start, last_4h_end, dbp, dbpwd)
        avgs_24h = IOUtils.read_classification_avgs(mdlist, last_24h_start, last_24h_end, dbp, dbpwd)
        avgs_week = IOUtils.read_classification_avgs(mdlist, last_week_start, last_week_end, dbp, dbpwd)

        df_list = []
        for every in equipments_dct.keys():
            ll = []
            ll.append(equipments_dct[every])

            if every in avgs_4h.keys():
                ll.append(avgs_4h[every])
            else:
                ll.append(None)

            if every in avgs_24h.keys():
                ll.append(avgs_24h[every])
            else:
                ll.append(None)

            if every in avgs_week.keys():
                ll.append(avgs_week[every])
            else:
                ll.append(None)

            df_list.append(ll)

        cols = ["Equipment", "Last_4hr", "Last_24hr", "Last_Week"]
        tabdata = pd.DataFrame(df_list, columns=cols)

        tabdata = tabdata.sort_values("Last_Week", ascending=False)
        tabdata.insert(0, 'id', range(1, 1 + len(tabdata)))

        datefmt = '%Y-%m-%dT%H:%M'
        times_dict_report = {'ct': datetime.strftime(ct, datefmt),
                             'Last_4hr_start': datetime.strftime(last_4h_start, datefmt),
                             'Last_4hr_end': datetime.strftime(last_4h_end, datefmt),
                             'Last_24hr_start': datetime.strftime(last_24h_start, datefmt),
                             'Last_24hr_end': datetime.strftime(last_24h_end, datefmt),
                             'Last_Week_start': datetime.strftime(last_week_start, datefmt),
                             'Last_Week_end': datetime.strftime(last_week_end, datefmt),
                             }

        try:
            tabdata["Last_4hr"] = tabdata['Last_4hr'].round(3)
        except Exception as e:
            tabdata["Last_4hr"] = 'NA'

        try:
            tabdata["Last_24hr"] = tabdata['Last_24hr'].round(3)
        except Exception as e:
            tabdata["Last_24hr"] = 'NA'

        try:
            tabdata["Last_Week"] = tabdata['Last_Week'].round(3)
        except Exception as e:
            tabdata["Last_Week"] = 'NA'

        return tabdata, ct.astimezone(pytz.timezone(str(get_localzone()))), times_dict_report


class Notifier:
    """
    Class to manage the notification system on Domino
    """

    @staticmethod
    def incident_email(payload):
        """
        Email generated when an incident occurs (when incidents dataframe is non-empty)
        """

        incidents_table = payload['incidents_df'].to_html()
        run_no = payload['run_no']

        email_content = """
        <head>
        <title>[INC] R3 anomaly detection - Run #{0} - Auto-alert</title>
        </head>
        <body>
        <h2> One or more incidents were detected during run {0}. Please refer to the table below for details.
        </h2>
        <h3>
        For all recorded incidents, please view the "dia_aas_global.ADPRO_CL_DIAGNOSTICS" table in the database. 
        </h3>
        <h3>{1}</h3>
        </body>
        """.format(run_no, incidents_table)

        f = open('email.html', 'w')
        f.write(email_content)
        f.close()

        logger.info("Email sent - incident")

    @staticmethod
    def no_incident_email(payload):
        """
        Email generated when no incident occurs and the run is normal (when incidents dataframe is empty)
        """

        run_no = payload['run_no']

        email_content = """
        <head>
        <title>[NORMAL] R3 anomaly detection - Run #{0} - Auto-alert</title>
        </head>
        <body>
        <h3>No incidents detected by the system during run {0}.</h3>
        </body>
        """.format(run_no)

        f = open('email.html', 'w')
        f.write(email_content)
        f.close()

        logger.info("Email sent - no incident")


class DiagnosticsUtils:
    """
    Class to manage the capture and recording of diagnostics data
    """

    def __init__(self):
        self.__incidents_df = pd.DataFrame(
            columns=["equipment", "site", "site_line", "run_no", "incident_timestamp", "source_file",
                     "code_line", "code_line_no", "function_name", "message"])
        self.__run_no = os.environ['DOMINO_RUN_NUMBER']

    @staticmethod
    def __get_traceback():
        """
        When called after an exception occurs, fetches exception-related metadata
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()

        if exc_traceback is None:
            raise TypeError("Traceback object is NoneType. Verify if an exception is being raised in the code.")

        st_summary = traceback.extract_tb(exc_traceback)
        st_entry = st_summary[-1]

        filename = st_entry.filename
        line = st_entry.line
        lineno = st_entry.lineno
        local_vars = st_entry.locals
        function_name = st_entry.name

        return filename, line, lineno, function_name, local_vars

    def capture(self, equipment, site, site_line, error_msg):
        """
        Records the results of get_traceback() in incidents dataframe
        """

        incident_timestamp = tm.ctime()

        try:
            source_file, code_line, code_line_no, function_name, local_vars = DiagnosticsUtils.__get_traceback()

            row = {"equipment": equipment, "site": site.name, "site_line": site_line, "code_line": code_line,
                   "run_no": self.__run_no, "incident_timestamp": incident_timestamp,
                   "source_file": source_file, "code_line_no": code_line_no,
                   "function_name": function_name, "message": error_msg}

            self.__incidents_df = self.__incidents_df.append(row, ignore_index=True)

            logger.info("Appended to incidents_df")
            logger.info("Len of incidents_df = {}".format(len(self.__incidents_df)))

        except TypeError as e:
            logging.warning(str(e))

    def notify(self, config_dict, dp_passw, notification_email_enabled = False):
        """
        Write incident logs to the database and creates email.html
        """

        table_name = config_dict[ADFPC.STR_DIAG_TABLE_NAME]
        user = config_dict[ADFPC.STR_USER]
        password = dp_passw
        host = config_dict[ADFPC.STR_HOST]
        port = config_dict[ADFPC.STR_PORT]
        database = config_dict[ADFPC.STR_DBNAME]
        ssl = config_dict[ADFPC.STR_SSL]
        ssl_cert = config_dict[ADFPC.STR_SSL_CERT_PATH]

        logger.info("Write diagnostics data to database ({})".format(table_name))
        IOUtils.write_results(df_results=self.__incidents_df, res_table_name=table_name,
                              user=user, passwd=password, host=host, port=port, db=database, ssl=ssl, ssl_cert=ssl_cert)

        if notification_email_enabled:
            if len(self.__incidents_df) > 0:
                payload = {"incidents_df": self.__incidents_df, "run_no": self.__run_no}
                Notifier.incident_email(payload)
            else:
                payload = {"run_no": self.__run_no}
                Notifier.no_incident_email(payload)


class ShiftHelper:

    def __init__(self, shifts_dct):
        assert (len(shifts_dct.keys()) == 3)
        self.__shifts_dct = shifts_dct
        self.__SEPCHAR = ':'

    def __get_starting_minutes(self):
        starting_minutes = []
        try:
            [h, m] = self.__shifts_dct[ADFPC.STR_SHIFTSTART_01].split(self.__SEPCHAR)
            starting_minutes.append(int(h) * 60 + int(m))

            [h, m] = self.__shifts_dct[ADFPC.STR_SHIFTSTART_02].split(self.__SEPCHAR)
            starting_minutes.append(int(h) * 60 + int(m))

            [h, m] = self.__shifts_dct[ADFPC.STR_SHIFTSTART_03].split(self.__SEPCHAR)
            starting_minutes.append(int(h) * 60 + int(m))

            assert (starting_minutes[0] < starting_minutes[1])
            assert (starting_minutes[1] < starting_minutes[2])

            return starting_minutes
        except Exception as e:
            logger.error("Unable to parse shift structure from dictionary ({}), or invalid shift structure".format(
                self.__shifts_dct))
            raise e

    def __get_shift_no(self, dt_sample):
        shift_starting_minutes = self.__get_starting_minutes()
        elapsed_mins = dt_sample.hour * 60 + dt_sample.minute

        if elapsed_mins > shift_starting_minutes[2]:
            logger.info("> {}".format(self.__shifts_dct[ADFPC.STR_SHIFTSTART_03]))
            shift_n = 3
            return [shift_n, elapsed_mins - shift_starting_minutes[2]]

        if elapsed_mins > shift_starting_minutes[1]:
            logger.info("> {}".format(self.__shifts_dct[ADFPC.STR_SHIFTSTART_02]))
            shift_n = 2
            return [shift_n, elapsed_mins - shift_starting_minutes[1]]

        if elapsed_mins > shift_starting_minutes[0]:
            logger.info("> {}".format(self.__shifts_dct[ADFPC.STR_SHIFTSTART_01]))
            shift_n = 1
            return [shift_n, elapsed_mins - shift_starting_minutes[0]]
        else:
            logger.info("> {}".format(self.__shifts_dct[ADFPC.STR_SHIFTSTART_03]))
            shift_n = 3
            return [shift_n, elapsed_mins - shift_starting_minutes[2]]

    def get_current_shift(self, dt_sample):
        [shift_n, remainder_mins] = self.__get_shift_no(dt_sample)

        if remainder_mins >= 0:
            ds = dt_sample - timedelta(minutes=remainder_mins)
        else:
            ds = dt_sample - timedelta(hours=24, minutes=remainder_mins)

        de = ds + timedelta(hours=8)
        return [ds, de]

    def get_previous_shift(self, dt_sample):
        [current_shift_start_dt, current_shift_end_dt] = self.get_current_shift(dt_sample)
        return [current_shift_start_dt - timedelta(hours=8), current_shift_end_dt - timedelta(hours=8)]


class ArtifactsIOHelper:
    def __init__(self, local_base_path: str, s3_base_path: str, aws_params_dct: dict):
        #example s3_base_path: s3://lly-dia-aas-prod/adfpro/artifacts/
        logging.info("Creating {}".format(type(self).__name__))
        self.__bucket = s3_base_path.split('/')[0]
        self.__base_key = s3_base_path[s3_base_path.find('/')+1:]
        self.__local_base_path = local_base_path
        self.__boto3_gw_client_factory = Boto3ClientFactory()
        self.__aws_params_dct = aws_params_dct
        proxy = aws_params_dct[ADFPC.STR_AWS_PROXY]

        cert_path = pathlib.Path(aws_params_dct[ADFPC.STR_AWS_SSL_CERTPATH]).resolve()
        cert_key_path = pathlib.Path(aws_params_dct[ADFPC.STR_AWS_SSL_KEYPATH]).resolve()
        if (pathlib.Path.is_file(cert_path) & pathlib.Path.is_file(cert_key_path)):
            logging.info("Using certificate found at: {}".format(cert_path))
            logging.info("Using certificate key found at: {}".format(cert_key_path))
        else:
            logging.error("Invalid certificate and/or key path...execution will fail")

        self.__boto3_gw_client_factory.set_service_account(aws_params_dct[ADFPC.STR_AWS_SVC_ACCT]) \
            .set_aws_account_id(str(aws_params_dct[ADFPC.STR_AWS_ACCT_ID])) \
            .set_aws_access_role(aws_params_dct[ADFPC.STR_AWS_GW_ROLE]) \
            .set_certificate_path(aws_params_dct[ADFPC.STR_AWS_SSL_CERTPATH]) \
            .set_certificate_key_path(aws_params_dct[ADFPC.STR_AWS_SSL_KEYPATH]) \
            .set_gw_url(aws_params_dct[ADFPC.STR_AWS_GW_ADDRESS] + str(aws_params_dct[ADFPC.STR_AWS_ACCT_ID])) \
            .set_proxies(proxy, proxy, proxy)
        self.__s3 = Boto3ClientFactory().create()

    #Use this to reset credentials (credentials expire every few hours)
    def reset_s3_client(self):
        logging.info("Resetting S3 boto client")
        try:
            svc_acct_pwd_envvar = self.__aws_params_dct[ADFPC.STR_AWS_SVC_ACCT_PWDENVVAR]
            self.__s3 = self.__boto3_gw_client_factory.create_using_gw(os.environ[svc_acct_pwd_envvar])
            logging.info("S3 boto client was successfully created")
        except Boto3ClientException as exc:
            logging.error("Error encountered while creating S3 boto client")
            logging.error(exc.message)

    #example:
    #self.__bucket = "bucket"
    #self.__base_key = "base/path/"
    #local_filepath = "/mnt/folder/test.pkl
    #s3_filepath = "anotherfolder/"
    #file will be copied to s3 as: "bucket/base/path/anotherfolder/test.pkl"
    def write_to_s3(self, local_filepath: str, s3_filepath=""):
        try:
            target_file_key = self.__base_key + s3_filepath + pathlib.Path(local_filepath).name
            response = self.__s3.upload_file(local_filepath, self.__bucket, target_file_key)
            file_key = target_file_key
            return file_key
        except ClientError as e:
            logging.error("Cannot write to s3: {}.\nDetails: {}".format(target_file_key, e))
            raise e
        except Exception as e:
            logging.error("Cannot write to s3: {}.\nDetails: {}".format(target_file_key, e))
            raise e

    def read_from_s3(self, s3_filepath: str, local_filepath: str):
        try:
            self.__s3.download_file(self.__bucket, self.__base_key + s3_filepath, local_filepath)
            logging.info("Successfully downloaded file {} to {}".format(s3_filepath, local_filepath))
        except ClientError as e:
            logging.error("Cannot download file {}.\nDetails: {}".format(s3_filepath, e))
            raise e
        except Exception as e:
            logging.error("Cannot download file {}.\nDetails: {}".format(s3_filepath, e))
            raise e

    def delete_from_s3(self, s3_filepath: str):
        try:
            self.__s3.delete_object(Bucket=self.__bucket, Key=self.__base_key + s3_filepath)
            logging.info("Successfully deleted file {}".format(s3_filepath))
        except ClientError as e:
            logging.error("Cannot delete file {}.\nDetails: {}".format(s3_filepath, e))
            raise e
        except Exception as e:
            logging.error("Cannot delete file {}.\nDetails: {}".format(s3_filepath, e))
            raise e

            
class RetrainingUtils:
    
    @staticmethod
    def initiate_retraining(srt,ert,component_list,site_name):
        
        start_retrain_date_object = ADFPDateUtils.utc_set(srt)
        end_retrain_date_object = ADFPDateUtils.utc_set(ert)
        
        retrain_job = dict(
        SITE= site_name, # Hardcoded - remove this later
        COMPONENTS = component_list,
        TRAIN = dict(
          ENABLED=bool('true'),
          START=start_retrain_date_object,
          END=end_retrain_date_object,
        ),
        CLASSIFICATION = dict(ENABLED=bool('true'))
        ) 
        
        directory_path = "/mnt/py/cfg.jobs/" # Hardcoded - fetch from CfgManager
        logger.info("Files Before creation {}".format(os.listdir(directory_path)))
        logger.info("Files data {}".format(retrain_job))
        
        path = "/mnt/py/cfg.jobs/temp_retrain_job.yml"
        with open(path, 'w') as outfile:
            yaml.dump(retrain_job, outfile, default_flow_style=False)
            
        logger.info("Yml file to be dumped @ {}".format(str(retrain_job)))
        logger.info("Retrain Yml file created @ {}".format(path))
        logger.info("Files After creation {}".format(os.listdir(directory_path)))
        
        logger.info("Initiate training jobs")
        
        master_cfg_path = "/mnt/py/master_cfg_prd.yml" # Hardcoded - path
        jobs_list_path = path
        logging.info("Using master configuration file: {}".format(master_cfg_path))
        logging.info("Using job list: {}".format(jobs_list_path))
        
        return master_cfg_path, jobs_list_path


class AuthenticationUtils:

    @staticmethod
    def create_user(user, pwd, dbp, dbpwd):

        pg = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
        pg.connect()

        table = dbp[ADFPC.STR_USERS_TABLE]

        user = user.lower()
        user_metadata = {}
        user_metadata['user_name'] = [user]
        
        sql_username_exists = "SELECT exists (SELECT 1 FROM {} WHERE user_name = '{}' LIMIT 1)".format(table, user)
        status = pg.execute_select(sql_username_exists, params ={})
        
        if status.bool():
            logger.info("Username already exists. Skipping write.")
            return 
        
        logger.info("Creating new user: {}".format(user))
        
        pwd_hashed = hashlib.sha256(pwd.encode())
        user_metadata['user_password'] = [pwd_hashed.hexdigest()]
        
        created_on = tm.gmtime()
        user_metadata['user_created_on'] = str(tm.strftime("%Y-%m-%d %H:%M:%S", created_on))
        user_metadata['user_last_logged_in'] = str(tm.strftime("%Y-%m-%d %H:%M:%S", created_on)) 
        user_metadata_df = pd.DataFrame.from_dict(user_metadata)
        
        pg.write_results_bulk(user_metadata_df, table)

        logger.info("User {} created.".format(user))

        pg.disconnect()


    @staticmethod
    def authenticate(user, pwd, dbp, dbpwd):

        pg = PGDataAccess(dbp[ADFPC.STR_USER], dbpwd, dbp[ADFPC.STR_HOST], dbp[ADFPC.STR_PORT],dbp[ADFPC.STR_DBNAME], dbp[ADFPC.STR_SSL], dbp[ADFPC.STR_SSL_CERT_PATH])
        pg.connect()

        table = dbp[ADFPC.STR_USERS_TABLE]
    
        user_lower = user.lower()
        hashed_pwd_input = hashlib.sha256(pwd.encode()).hexdigest()
        
        try:
            hashed_pwd_db = pg.execute_simple_select(table, "user_name", user_lower)['user_password'].values[0]
            pg.disconnect()
        except Exception:
            logger.error("Username {} not found. Try again.".format(user_lower))
            pg.disconnect()
            return False
        
        if hashed_pwd_input == hashed_pwd_db:
            logger.error("User {} authenticated!".format(user_lower))
            pg.disconnect()
            return True
        else:
            logger.error("Password mismatch for user {}. Try again.".format(user_lower))
            pg.disconnect()
            return False