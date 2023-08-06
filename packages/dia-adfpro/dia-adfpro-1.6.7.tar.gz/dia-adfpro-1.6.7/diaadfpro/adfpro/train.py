"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

import logging
import time

import shap

from diaadfpro.adfpro.configuration import ConfigurationManager
from diaadfpro.adfpro.constants import ADFPC
from diaadfpro.adfpro.model import Component, ModelDescriptor, ShapExplainerDescriptor, JobList, Site
from diaadfpro.adfpro.utils import IOUtils, DataQualityException, ArtifactsIOHelper, RetrainingUtils, ADFPDateUtils

logger = logging.getLogger(__name__)


class Trainer():

    @staticmethod
    def build(modl_descriptor: ModelDescriptor, expl_descriptor: ShapExplainerDescriptor, dbp, pwd, artifacts_path):
        trn = Trainer()
        trn.__set_model_descriptor(modl_descriptor)
        trn.__set_explainer_descriptor(expl_descriptor)
        trn.__set_db_params(dbp, pwd)
        trn.__set_artifacts_path(artifacts_path)
        return trn

    def __set_model_descriptor(self, modl_descriptor: ModelDescriptor):
        self.__model_descriptor = modl_descriptor

    def __set_explainer_descriptor(self, expl_descriptor: ShapExplainerDescriptor):
        self.__explainer_descriptor = expl_descriptor

    def __set_db_params(self, dbp, pwd):
        self.__db_params = dbp
        self.__pwd = pwd

    def __set_artifacts_path(self, artifacts_path):
        self.__artifacts_path = artifacts_path

    def execute_train_job(self, job_list: JobList, site: Site):
        if not job_list.get_train_enabled():
            return

        logger.info("Start training components in job list")

        train_start = job_list.get_train_start()
        train_end = job_list.get_train_end()
        cmp_list = job_list.get_components()

        for cmp_name in cmp_list:
            cmp = site.find_component(cmp_name)
            if cmp is None:
                logger.error(f">>>Cannot find any component named {cmp_name}")
                continue
            try:
                self.train_component(cmp, train_start, train_end)
            except DataQualityException as e:
                logger.error("Unable to train component {} due to bad data quality".format(cmp.name))
                logger.error("Details: {}".format(e))
            except Exception as e:
                logger.error("Unable to train component named {}. Please check if the component name specified in the "
                             "job list corresponds to a valid component.".format(cmp_name))
                logger.error("Details: {}".format(e))

        logger.info("Done training components in job list")


    def train_component(self, cmp: Component, train_start=None, train_end=None):
        tstart = train_start
        tend = train_end
        if (train_start is None) or (train_end is None):
            tstart = cmp.training_interval[Component.INTV_START]
            tend = cmp.training_interval[Component.INTV_END]

        feat_list = [fn.name for fn in cmp.features]
        logger.info("Training component {}".format(cmp.name))
        logger.info("Train start: {}".format(tstart))
        logger.info("Train end: {}".format(tend))

        df_train_ft = IOUtils.get_feature_matrix(self.__db_params, tstart, tend, feat_list,
                                                 fillna=True, dbpwd=self.__pwd)

        if df_train_ft is None:
            logger.info("No data found in specified time window")
            return

        [scaler, df_train_ft_ok] = IOUtils.normalize(df_train_ft)

        if df_train_ft_ok is None:
            logger.info("No data found in specified time window")
            return

        logger.info("Train model on {} cycles".format(len(df_train_ft_ok)))

        model = self.__model_descriptor.create_model(len(feat_list))
        version = self.__model_descriptor.version

        start = time.time()
        model.fit(df_train_ft_ok)
        end = time.time()
        logger.info("Done training model in {}s".format(end - start))

        logger.info("Calculate SHAP explainer based on model and training set data")
        st = self.__explainer_descriptor.summary_type
        ssz = self.__explainer_descriptor.summary_size

        start = time.time()
        df_shap = shap.kmeans(df_train_ft_ok, 5)
        if st == ADFPC.SUMMARY_KMEANS:
            df_shap = shap.kmeans(df_train_ft_ok, ssz)
        elif st == ADFPC.SUMMARY_SAMPLE:
            df_shap = shap.sample(df_train_ft_ok, nsamples=ssz, random_state=0)
        explainer = shap.KernelExplainer(model.predict_proba, df_shap)
        end = time.time()
        logger.info("Done calculating explainer in {}s".format(end - start))

        model_metadata = {}
        model_metadata[ADFPC.STR_TRAINSTART] = tstart
        model_metadata[ADFPC.STR_TRAINEND] = tend
        model_metadata[ADFPC.STR_SCALEROBJ] = scaler
        model_metadata[ADFPC.STR_CLASIFIEROBJ] = model

        model_metadata[ADFPC.STR_CLASSIFIERNAME] = str(type(model).__name__)
        model_metadata[ADFPC.STR_CLASSIFIERVERSION] = version
        model_metadata[ADFPC.STR_EXPLAINER] = explainer
        model_metadata[ADFPC.STR_SUMMARY_TYPE] = st
        model_metadata[ADFPC.STR_SUMMARY_SIZE] = ssz

        model_metadata[ADFPC.STR_TRAININGDATA] = df_train_ft

        pkl_fname = IOUtils.build_pkl_path(cmp.site.name, cmp.parent_component.name, cmp.name,
                                                model_metadata[ADFPC.STR_CLASSIFIERNAME])

        fname = IOUtils.save_pkl(model_metadata, self.__artifacts_path, pkl_fname)
        logger.info("Pack everything in dictionary and save as pkl ({})".format(fname))

        # copy pkl to S3
        artifacts_helper = ArtifactsIOHelper(ConfigurationManager.instance().get_artifacts_folder(),
                                             ConfigurationManager.instance().get_s3_artifacts_folder(),
                                             ConfigurationManager.instance().get_aws_param_dictionary())
        artifacts_helper.reset_s3_client()
        fname_s3 = artifacts_helper.write_to_s3(fname, "")
        logger.info("Copied pkl to s3 ({})".format(fname_s3))

        #erase classifications produced with previously trained model (for current component)
        logger.info("Erasing classification values obtained with previously trained model, for component {} ({})".
                    format(cmp.name, cmp.id))
        IOUtils.erase_classification_results(
            ConfigurationManager.instance().get_database_param_dictionary(),
            ConfigurationManager.instance().get_db_password(),
            cmp.id
        )
        #write data to DB table that keeps track of when models were last trained and using which time interval, and who triggered the (re)training
        status = IOUtils.upsert_table_adpro_equipment_model(
            ConfigurationManager.instance().get_database_param_dictionary(),
            ConfigurationManager.instance().get_db_password(),
            tstart,
            tend,
            ADFPDateUtils.get_current_dt(),
            ConfigurationManager.instance().get_current_user_id(),
            cmp.id,
            ConfigurationManager.instance().get_model_descriptor().type_and_version
        )
        # ConfigurationManager.get_model_descriptor().type_and_version
        logger.info("Done training component {}".format(cmp.name))
