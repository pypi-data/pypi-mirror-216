"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

import logging
import pathlib
import time
from datetime import datetime
from enum import Enum

from aimltools.ts.utils import GenericUtils
from tabulate import tabulate

from diaadfpro.adfpro.configuration import ConfigurationManager
from diaadfpro.adfpro.constants import ADFPC
from diaadfpro.adfpro.utils import IOUtils, YMLConfigReader, ADFPDateUtils, DiagnosticsUtils, DataQualityException, \
    ArtifactsIOHelper, IOUtilsException
from diaadfpro.adfpro.model import Component, ModelDescriptor, JobList, Site

logger = logging.getLogger(__name__)

class ClassifierExitCodes(Enum):
    NO_ERRORS = 0
    DATA_QUALITY_WARNING = 1
    CLASSIFICATION_RESULT_WRITE_ERROR = 2
    COMPONENT_NOT_FOUND = 3
    UNSPECIFIED_ERROR = 1000


class Classifier():
    @staticmethod
    def build(modl_descriptor: ModelDescriptor, dbp, pwd, artifacts_path, cmp_descriptor_dct, send_notification_email = False):
        cls = Classifier()
        cls.__set_model_descriptor(modl_descriptor)
        cls.__set_db_params(dbp, pwd)
        cls.__set_artifacts_path(artifacts_path)
        cls.__set_classification_date(ADFPDateUtils.get_current_dt())
        cls.__set_cmp_descriptor_dictionary(cmp_descriptor_dct)
        cls.__set_notification_email_enabled(send_notification_email)
        return cls

    def __init__(self):
        self.__diagnostics = DiagnosticsUtils()
        self.__exit_codes = []

    def __set_notification_email_enabled(self, notif_email_enabled):
        self.__notification_email_enabled = notif_email_enabled

    def __set_cmp_descriptor_dictionary(self, cmp_descriptor_dct):
        self.__cmp_descriptor_dct = cmp_descriptor_dct

    def __set_model_descriptor(self, modl_descriptor: ModelDescriptor):
        self.__model_descriptor = modl_descriptor

    def __set_db_params(self, dbp, pwd):
        self.__dbp = dbp
        self.__dbpwd = pwd

    def __set_artifacts_path(self, artifacts_path):
        self.__artifacts_path = artifacts_path

    def __set_classification_date(self, dt: datetime):
        self.__classif_date = dt

    @property
    def failed(self):
        if ClassifierExitCodes.UNSPECIFIED_ERROR in self.__exit_codes:
            return True

        if ClassifierExitCodes.CLASSIFICATION_RESULT_WRITE_ERROR in self.__exit_codes:
            return True

        return False

    def override_latest_classif_date(self, dt):
        assert(ADFPDateUtils.is_tz_aware(dt))
        logger.warning("Overriding latest classification date with: {}".format(dt))
        self.__ovr_latest_classif_date = dt

    def execute_classify_job(self, job_list: JobList, site: Site):
        if not job_list.get_classification_enabled():
            return

        cls_start = job_list.get_classification_start()
        cls_end = job_list.get_classification_end()
        
        cmp_list = job_list.get_components()

        for cmp_name in cmp_list:
            try:
                cmp = site.find_component(cmp_name)
                if cmp is None:
                    logger.error(f">>>Cannot find any component named {cmp_name}")
                    self.__exit_codes.append(ClassifierExitCodes.COMPONENT_NOT_FOUND)
                else:
                    self.classify_component(cmp, cls_start, cls_end)
                    self.__exit_codes.append(ClassifierExitCodes.NO_ERRORS)
            except DataQualityException as e:
                error_msg = "Classification for equipment {} failed at {}, due to bad data quality encountered in classification time interval\n".format(
                    cmp_name, time.ctime())
                self.__diagnostics.capture(equipment=cmp_name, site=cmp.site, site_line=cmp.parent_component.name,
                                           error_msg=error_msg)
                logger.warning(">>>Could not classify equipment: {} - Bad data quality".format(cmp_name))
                logger.warning(">>>{}".format(e))
                self.__exit_codes.append(ClassifierExitCodes.DATA_QUALITY_WARNING)
            except IOUtilsException as e:
                error_msg = "Classification for equipment {} failed at {}, due to errors writing to database\n".format(
                    cmp_name, time.ctime())
                self.__diagnostics.capture(equipment=cmp_name, site=cmp.site, site_line=cmp.parent_component.name,
                                           error_msg=error_msg)
                logger.error(">>>Error classifying equipment: {} - Unable to write classification results to DB".format(cmp_name))
                logger.error(">>>{}".format(e))
                self.__exit_codes.append(ClassifierExitCodes.CLASSIFICATION_RESULT_WRITE_ERROR)
            except Exception as e:
                error_msg = "Classification for equipment {} failed at {}\n".format(
                    cmp_name, time.ctime())
                self.__diagnostics.capture(equipment=cmp_name, site=cmp.site, site_line=cmp.parent_component.name,
                                           error_msg=error_msg)

                logger.error(">>>Error classifying equipment: {}".format(cmp_name))
                logger.error(">>>{}".format(e))
                self.__exit_codes.append(ClassifierExitCodes.UNSPECIFIED_ERROR)

        if self.__dbp[ADFPC.STR_WRITE_ENABLED]:
            self.__diagnostics.notify(self.__dbp, self.__dbpwd, self.__notification_email_enabled)
            logger.info("Notified errors (database/email)")
        else:
            logger.warning("Write to DB disabled")
            logger.warning("Skipped writing diagnostics to DB and generating disgnostics")

    def classify_component(self, cmp: Component, cls_start=None, cls_end=None):
        if cmp is None:
            logger.error("Cannot classify null component")
            return

        logger.info("Classifying {}".format(cmp.name))

        cl_start = None
        cl_end = None
        if not(cls_start is None) and not(cls_end is None):
            # use classification interval provided as input
            cl_start = cls_start
            cl_end = cls_end
        elif (cls_start is None) and (cls_end is None):
            # calculate classification interval from data stored in component
            cl_start = cmp.classification_interval[Component.INTV_START]
            cl_end = cmp.classification_interval[Component.INTV_END]
            if cmp.classification_mode == Component.CL_MODE_LATEST:
                cl_end = self.__classif_date
        else:
            # this should not happen and is to be considered as an error
            logger.error("Inconsistent information related to start/end of classification interval. Skipping classification.")
            return

        logger.info("Classification start: {}".format(cl_start))
        logger.info("Classification end: {}".format(cl_end))

        feat_list = [fn.name for fn in cmp.features]
        df_train_ft = IOUtils.get_feature_matrix(self.__dbp, cl_start, cl_end, feat_list, fillna=True, dbpwd=self.__dbpwd)

        if df_train_ft is None:
            logger.info("No data found in specified time window")
            return

        pkl_filename = IOUtils.build_pkl_path(cmp.site.name, cmp.parent_component.name, cmp.name, self.__model_descriptor.type)
        pkl_path_local = pathlib.Path(ConfigurationManager.instance().get_artifacts_folder(), pkl_filename).resolve()

        # download pkl file that stores model from S3 to local folder
        artifacts_helper = ArtifactsIOHelper(ConfigurationManager.instance().get_artifacts_folder(),
                                             ConfigurationManager.instance().get_s3_artifacts_folder(),
                                             ConfigurationManager.instance().get_aws_param_dictionary())
        artifacts_helper.reset_s3_client()
        artifacts_helper.read_from_s3(str(pkl_filename), str(pkl_path_local))

        # load model from pkl file
        pkl_data = IOUtils.read_pkl_direct(pkl_path_local)

        scaler = pkl_data[ADFPC.STR_SCALEROBJ]
        model = pkl_data[ADFPC.STR_CLASIFIEROBJ]
        model_name = pkl_data[ADFPC.STR_CLASSIFIERNAME]
        model_version = pkl_data[ADFPC.STR_CLASSIFIERVERSION]
        model_description = "{} {}".format(model_name, model_version)
        logger.info('Using model: {}'.format(model_description))

        logger.info("Classifying {} cycles found on database".format(len(df_train_ft)))
        start = time.time()
        test_norm = scaler.transform(df_train_ft)
        preds = model.predict(test_norm)
        pred_proba = model.predict_proba(test_norm)
        end = time.time()
        logger.info("Done classifying cycles in {}s".format(end - start))
        
        df_results = GenericUtils.cls_to_df(df_train_ft, pred_proba, preds, cmp.id, model_description, self.__dbp[ADFPC.STR_CLS_TABLE_OCOLS])
        
        logger.debug("Classification results:")
        logger.debug("\n{}".format(tabulate(df_results)))

        if self.__dbp[ADFPC.STR_WRITE_ENABLED]:
            logger.info("Writing results to database")
            record_cnt = IOUtils.insert_classification_results(self.__dbp, self.__dbpwd, df_classif_results=df_results)
            if (record_cnt == len(df_results)) and (cmp.classification_mode == Component.CL_MODE_LATEST):
                cmp.latest_classification_date = self.__classif_date
                logger.info("Updating latest classification time on file for component {}".format(cmp.name))
                YMLConfigReader.write(cmp.to_cfg_dictionary(), self.__cmp_descriptor_dct[cmp])
            else:
                logger.error("There was an error writing classification results to database: latest classification time was not updated")
        else:
            logger.warning("Write to DB disabled")
            logger.warning("Skipped writing results to DB")
            logger.warning("Skipped updating latest classification on file")