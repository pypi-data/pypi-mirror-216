"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

import logging
import os
from pathlib import Path
import pandas as pd

from diaadfpro.adfpro.constants import ADFPC
from diaadfpro.adfpro.model import Site, Component, Feature, ModelDescriptor, ANNModelDescriptor, ExplainerDescriptor, \
    ShapExplainerDescriptor
from diaadfpro.adfpro.utils import YMLConfigReader
from aimltools.ts.utils import PGDataAccess

logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class ConfigurationManager(metaclass=Singleton):
    def __init__(self):
        try:
            if self.__site_list is None:
                self.__site_list = None
                self.__model_descriptor = None
                self.__explainer_descriptor = None
                self.__artifacts_path = None
                self.__component_cfg_path = None
                self.__component_cfg_descriptors = None
                self.__current_username = None
                self.__current_userid = None
        except AttributeError as e:
            self.__site_list = None

    @staticmethod
    def initialize(mastercfg_filepath):
        inst = ConfigurationManager.instance()
        inst.__load_configuration(mastercfg_filepath)
        inst.__load_paths()
        inst.__load_components()
        inst.__load_model_descriptor()
        inst.__load_explainer_descriptor()

    @staticmethod
    def instance():
        return ConfigurationManager()

    def get_site(self, site_name):
        for site in self.__site_list:
            if site.name == site_name:
                return site

    def get_site_components(self, site_name):
        site = self.get_site(site_name)
        if not (site is None):
            return site.components

    def get_sites(self):
        return self.__site_list

    def get_model_descriptor(self) -> ModelDescriptor:
        return self.__model_descriptor

    def get_explainer_descriptor(self) -> ExplainerDescriptor:
        return self.__explainer_descriptor

    def get_artifacts_folder(self):
        return self.__artifacts_path

    def get_s3_artifacts_folder(self):
        return self.__s3_artifacts_path

    def get_cmp_configuration_folder(self):
        return self.__component_cfg_path

    def get_database_param_dictionary(self):
        return self.__mastercfg_dct[ADFPC.STR_DB]

    def get_db_password(self):
        db_dct = self.get_database_param_dictionary()
        return os.environ[db_dct[ADFPC.STR_PWD_ENVVAR]]

    def get_aws_param_dictionary(self):
        return self.__mastercfg_dct[ADFPC.STR_AWS]

    def get_aws_svc_acct_password(self):
        aws_dct = self.get_aws_param_dictionary()()
        return os.environ[aws_dct[ADFPC.STR_AWS_SVC_ACCT_PWDENVVAR]]

    def get_shifts_dictionary(self):
        return self.__mastercfg_dct[ADFPC.STR_SHIFTS]

    def get_component_descriptor_paths(self):
        return self.__component_cfg_descriptors

    def get_ui_host(self):
        return self.__mastercfg_dct[ADFPC.STR_DASH][ADFPC.STR_DASH_HOST]

    def get_ui_port(self):
        return self.__mastercfg_dct[ADFPC.STR_DASH][ADFPC.STR_DASH_PORT]

    def get_ui_debug(self):
        return self.__mastercfg_dct[ADFPC.STR_DASH][ADFPC.STR_DASH_DEBUG]

    def get_ui_site(self):
        return self.__mastercfg_dct[ADFPC.STR_DASH][ADFPC.STR_DASH_SITE]

    def get_ui_lines(self):
        return self.__mastercfg_dct[ADFPC.STR_DASH][ADFPC.STR_DASH_LINES]

    def get_current_user(self):
        return self.__current_username

    def set_current_user(self, username):
        self.__current_username = username
        
    def get_current_user_id(self):
        return self.__current_userid

    def set_current_user_id(self, userid):
        self.__current_userid = userid

    def __load_configuration(self, mastercfg_filepath):
        self.__mastercfg_dct = YMLConfigReader.read_full_path(mastercfg_filepath)

    def __find_component(self, cmp_name):
        for site in self.__site_list:
            cmp = site.find_component(cmp_name)
            if not (cmp is None):
                return cmp

    def __configure_component(self, cmp: Component, cmp_dct):
        id = cmp_dct[ADFPC.STR_EQM_ID]

        if cmp.id != id:
            msg = "Component id mismatch. DB: {}, yml: {}".format(cmp.id, id)
            logger.error(msg)
            raise msg

        cls_dct = cmp_dct[ADFPC.STR_CLASSIF]
        trn_dct = cmp_dct[ADFPC.STR_TRAIN]
        cmp.training_interval = [trn_dct[ADFPC.STR_START], trn_dct[ADFPC.STR_END]]
        cmp.training_enabled = trn_dct[ADFPC.STR_ENABLED]

        cmp.classification_mode = cls_dct[ADFPC.STR_CLASSIFICATION_MODE]
        if cmp.classification_mode == Component.CL_MODE_LATEST:
            cmp.latest_classification_date = cls_dct[ADFPC.STR_LATEST_CLASSIF]
            cmp.classification_interval = [cmp.latest_classification_date, None]
        else:
            cmp.classification_interval = [cls_dct[ADFPC.STR_START], cls_dct[ADFPC.STR_END]]

        cmp.classification_mode = cls_dct[ADFPC.STR_CLASSIFICATION_MODE]
        cmp.classification_enabled = cls_dct[ADFPC.STR_ENABLED]

    def __load_paths(self):
        self.__artifacts_path = Path(self.__mastercfg_dct[ADFPC.STR_PATHS][ADFPC.STR_PATHS_ARTIFACT_OUT]).resolve()
        self.__s3_artifacts_path = self.__mastercfg_dct[ADFPC.STR_PATHS][ADFPC.STR_PATHS_S3_ARTIFACT_OUT]
        logger.info("Artifacts path (local): {}".format(self.__artifacts_path))
        logger.info("Artifacts path (s3): {}".format(self.__s3_artifacts_path))
        self.__component_cfg_path = Path(
            self.__mastercfg_dct[ADFPC.STR_PATHS][ADFPC.STR_PATHS_COMPONENT_CFG]).resolve()
        logger.info("Component configuration path: {}".format(self.__component_cfg_path))

    def __load_model_descriptor(self):
        mod_dct = self.__mastercfg_dct[ADFPC.STR_MODEL]
        if mod_dct[ADFPC.STR_TYPE] == ModelDescriptor.TYPE_ANNCLASSIFIER:
            self.__model_descriptor = ANNModelDescriptor(mod_dct[ADFPC.STR_TYPE],
                                                         mod_dct[ADFPC.STR_VERSION],
                                                         mod_dct[ADFPC.STR_EPOCHS],
                                                         mod_dct[ADFPC.STR_HIDDEN_LAYERS],
                                                         mod_dct[ADFPC.STR_HIDDEN_NEURONS],
                                                         mod_dct[ADFPC.STR_OUTLIERS_FRACTION],
                                                         mod_dct[ADFPC.STR_RESET_KERAS_BEFORE_FIT])

    def __load_explainer_descriptor(self):
        exp_dct = self.__mastercfg_dct[ADFPC.STR_EXPLAINER]
        if exp_dct[ADFPC.STR_TYPE] == ExplainerDescriptor.TYPE_SHAPEXPLAINER:
            self.__explainer_descriptor = ShapExplainerDescriptor(exp_dct[ADFPC.STR_TYPE],
                                                                  exp_dct[ADFPC.STR_SUMMARY_SIZE],
                                                                  exp_dct[ADFPC.STR_SUMMARY_TYPE])

    def __load_components(self):
        # 1: load components' structure from DB
        logger.info("Loading site/component structure from DB")
        dbp = self.__mastercfg_dct[ADFPC.STR_DB]
        dbpwd = self.get_db_password()
        st_loader = SiteLoader()
        self.__site_list = st_loader.load(user=dbp[ADFPC.STR_USER],
                                          pwd=dbpwd,
                                          host=dbp[ADFPC.STR_HOST],
                                          port=dbp[ADFPC.STR_PORT],
                                          db=dbp[ADFPC.STR_DBNAME],
                                          ssl=dbp[ADFPC.STR_SSL],
                                          ssl_cert=dbp[ADFPC.STR_SSL_CERT_PATH],
                                          eqpm_table=dbp[ADFPC.STR_CMP_TABLE_NAME],
                                          eqpm_feat_table=dbp[ADFPC.STR_CMPFEAT_TABLE_NAME])

        # 2: complete components' configuration by loading information from files
        self.__component_cfg_descriptors = {}
        cmpcfg_path = self.__mastercfg_dct[ADFPC.STR_PATHS][ADFPC.STR_PATHS_COMPONENT_CFG]
        logger.info("Completing component configuration, reading from configuration files in {}".format(Path(cmpcfg_path).resolve()))
        pathlist = Path(cmpcfg_path).glob('*.yml')
        for path in pathlist:
            path_resolved = path.resolve()
            logger.info("Reading {}".format(path_resolved))
            cmp_dct = YMLConfigReader.read_full_path(path_resolved)
            cmp_name = path.stem
            cmp = self.__find_component(cmp_name)
            if not (cmp is None):
                logger.debug("Found component {}. Configuring component from file.".format(cmp_name))
                self.__configure_component(cmp, cmp_dct)
                self.__component_cfg_descriptors[cmp] = path_resolved
            else:
                logger.error("Cannot find component named {} in tree structure loaded from DB".format(cmp_name))
                


class SiteLoader:
    def __init__(self):
        self.__col_fcltycode = "fclty_code"
        self.__col_eqmid = "eqpm_id"
        self.__col_eqmname = "eqm_name"
        self.__col_fcltyname = "fclty_name"
        self.__col_parentid = "parent_id"
        self.__col_ftrid = "ftr_id"
        self.__col_ftrname = "ftr_name"

    def load(self, user, pwd, host, port, db, ssl, ssl_cert, eqpm_table, eqpm_feat_table):
        db = PGDataAccess(user, pwd, host, port, db, ssl, ssl_cert)
        try:
            db.connect()
            #dbp = ConfigurationManager.instance().__mastercfg_dct[ADFPC.STR_DB]
            qry = """select ce.eqpm_id, ce.eqm_name, ce.fclty_code, ce.fclty_name, ce.parent_id, cef.ftr_id, cef.ftr_name from {} ce 
                        left join {} cef 
                        on cef.eqpm_id = ce.eqpm_id order by ce.eqm_name asc, cef.ftr_id asc;""".format(eqpm_table, 
                                                                                                        eqpm_feat_table)
            df = db.execute_select(qry, params=[])
        except Exception as e:
            logger.error("Error retrieving information on components from DB")
            logger.error("Details: {}".format(e))
        finally:
            db.disconnect()

        df = df.set_index([self.__col_fcltycode, self.__col_eqmid])
        site_list = self.__load_sites(df)
        return site_list

    def __load_sites(self, df):
        fcode_list = df.index.get_level_values(self.__col_fcltycode).unique()
        site_list = []
        for fcode in fcode_list:
            logger.debug("Load fclty code {}".format(fcode))
            site_list.append(self.__load_site(fcode, df.xs(fcode)))
        return site_list

    def __load_site(self, fcode, df):
        # df contains cross section of entire dataframe for given site
        # 1. get unique id's of top level (root) components and put them in a list
        df_parent_cmp = df[df[self.__col_parentid].isna()]
        root_cmp_list = df_parent_cmp.index.get_level_values(self.__col_eqmid).unique()
        s = Site(df[self.__col_fcltyname].values[0], fcode)
        # 2. loop on all root components
        for cmp_id in root_cmp_list:
            cmp = Component(cmp_id, df.xs(cmp_id)[self.__col_eqmname], site=s, parent_cmp=None)
            logger.debug("Load component {}".format(cmp.name))
            self.__load_component(cmp, df)
            s.add_component(cmp)
        return s

    def __load_component(self, cmp, df):
        # df contains cross section of entire dataframe for given site
        # df contains multiple rows for each eqpm_id (since we are left-joining with the feature table)
        # 1. get list of child components and their unique id's
        child_cmp_df = df[df[self.__col_parentid] == cmp.id]
        child_cmp_lst = child_cmp_df.index.get_level_values(self.__col_eqmid).unique().sort_values()
        if len(child_cmp_lst) == 0:
            return

        for cmp_id in child_cmp_lst:
            # focus on component having id = cmp_id
            if isinstance(df.xs(cmp_id), pd.DataFrame):
                chld_cmp = Component(cmp_id, df.xs(cmp_id)[self.__col_eqmname].values[0], site=cmp.site, parent_cmp=cmp)
                logger.debug("Load component {} (parent = {})".format(chld_cmp.name, cmp.name))
                for index, row in df.xs(cmp_id).iterrows():
                    ftr = Feature(row[self.__col_ftrid], row[self.__col_ftrname])
                    chld_cmp.add_feature(ftr)
                    logger.debug("Add feature {}".format(ftr.name))
            else:
                # means a component has only 1 feature
                chld_cmp = Component(cmp_id, df.xs(cmp_id)[self.__col_eqmname], site=cmp.site, parent_cmp=cmp)
                logger.debug("Load component {} (parent = {})".format(chld_cmp.name, cmp.name))
                ftr = Feature(df.xs(cmp_id)[self.__col_ftrid], df.xs(cmp_id)[self.__col_ftrname])
                chld_cmp.add_feature(ftr)

            # recurse on child components
            self.__load_component(chld_cmp, df)
            cmp.add_child(chld_cmp)