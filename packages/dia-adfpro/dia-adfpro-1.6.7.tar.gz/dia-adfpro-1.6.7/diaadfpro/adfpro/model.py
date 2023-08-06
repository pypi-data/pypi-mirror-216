"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

import logging
import numpy as np
from typing import List

from aimltools.ts.classification import ANNClassifier

from diaadfpro.adfpro.constants import ADFPC
from diaadfpro.adfpro.utils import ADFPDateUtils, YMLConfigReader

logger = logging.getLogger(__name__)


class Site:
    def __init__(self, name, code):
        self.__name = name
        self.__code = code
        self.__cmp_list = []

    def add_component(self, cmp):
        self.__cmp_list.append(cmp)

    @property
    def components(self):
        return self.__cmp_list

    @property
    def name(self):
        return self.__name

    @property
    def code(self):
        return self.__code

    def find_component(self, component_name):
        for cmp in self.__cmp_list:
            c = cmp.find_component(component_name)
            if not (c is None):
                return c
        return None

    def get_flattened_component_list(self) -> List['Component']:
        cmp_list = []
        for cmp in self.components:
            cmp_list.extend(cmp.get_flattened_component_list())
        return cmp_list

    def __str__(self):
        return "Site: {} - {}".format(self.__code, self.__name)


class Feature:
    def __init__(self, fid, name):
        self.__id = fid
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id


class Component:
    CL_MODE_LATEST = 'latest'
    CL_MODE_FIXED = 'fixed'
    INTV_START = 'start'
    INTV_END = 'end'

    def __init__(self, id, name, site: Site, parent_cmp=None):
        self.__id = id
        self.__name = name
        self.__site = site
        self.__parent_cmp = parent_cmp
        self.__ftr_list = []
        self.__child_cmp_list = []
        self.__cl_mode = Component.CL_MODE_LATEST
        self.__cls_enabled = False
        self.__trn_enabled = False
        self.__trn_interval = {Component.INTV_START: None, Component.INTV_END: None}
        self.__cls_interval = {Component.INTV_START: None, Component.INTV_END: None}
        self.__latest_classif_date = None

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def site(self):
        return self.__site

    @property
    def parent_component(self):
        return self.__parent_cmp

    def add_feature(self, ftr: Feature):
        self.__ftr_list.append(ftr)

    def reset_features(self):
        self.__ftr_list.clear()

    @property
    def features(self):
        return self.__ftr_list

    def reset_children(self):
        self.__child_cmp_list.clear()

    def add_child(self, cmp):
        self.__child_cmp_list.append(cmp)

    @property
    def child_components(self):
        return self.__child_cmp_list

    def find_component(self, component_name):
        logger.debug("Find component {}".format(component_name))
        if self.__name == component_name:
            logger.debug("Found! It was myself!")
            return self

        if len(self.__child_cmp_list) == 0:
            logger.debug("Empty children list.")
            return None

        logger.debug("Scanning children of {}".format(self.name))
        for cmp in self.__child_cmp_list:
            logger.debug("Scanning {}".format(cmp.name))
            if cmp.name == component_name:
                return cmp
            else:
                c = cmp.find_component(component_name)
                if not (c is None):
                    return c
        return None

    @property
    def training_interval(self):
        return self.__trn_interval

    @training_interval.setter
    def training_interval(self, trn_interval):
        start_dt = trn_interval[0]
        end_dt = trn_interval[1]

        if not (ADFPDateUtils.is_tz_aware(start_dt)):
            raise Exception("Start datetime for training interval is not tz aware")
        if not (ADFPDateUtils.is_tz_aware(end_dt)):
            raise Exception("End datetime for training interval is not tz aware")

        if end_dt <= start_dt:
            raise Exception(
                "End of training interval should be later than its start: please check your training interval dates")

        self.__trn_interval[Component.INTV_START] = start_dt
        self.__trn_interval[Component.INTV_END] = end_dt

    @property
    def training_enabled(self):
        return self.__trn_enabled

    @training_enabled.setter
    def training_enabled(self, en):
        self.__trn_enabled = en

    @property
    def classification_mode(self):
        return self.__cl_mode

    @classification_mode.setter
    def classification_mode(self, cl_mode):
        if cl_mode.lower() == Component.CL_MODE_LATEST:
            self.__cl_mode = Component.CL_MODE_LATEST
        elif cl_mode.lower() == Component.CL_MODE_FIXED:
            self.__cl_mode = Component.CL_MODE_FIXED
        else:
            raise "Unknown classification model: {}".format(cl_mode)

    @property
    def classification_interval(self):
        return self.__cls_interval

    @classification_interval.setter
    def classification_interval(self, cls_interval):
        start_dt = cls_interval[0]
        end_dt = cls_interval[1]

        if not (ADFPDateUtils.is_tz_aware(start_dt)):
            raise Exception("Start datetime for classification interval is not tz aware")
        self.__cls_interval[Component.INTV_START] = start_dt

        if not (end_dt is None):
            if not (ADFPDateUtils.is_tz_aware(end_dt)):
                raise Exception("End datetime for classification interval is not tz aware")

            if end_dt <= start_dt:
                raise Exception(
                    "End of classification interval should be later than its start: please check your classification interval dates")

            self.__cls_interval[Component.INTV_END] = end_dt

    @property
    def classification_enabled(self):
        return self.__cls_enabled

    @classification_enabled.setter
    def classification_enabled(self, en):
        self.__cls_enabled = en

    @property
    def latest_classification_date(self):
        return self.__latest_classif_date

    @latest_classification_date.setter
    def latest_classification_date(self, dt):
        self.__latest_classif_date = dt

    def from_cfg_dictionary(self, cmp_dct):
        # currently relying on ConfigurationManager.__configure_component()...
        # ...do we really need this?
        pass

    def to_cfg_dictionary(self):
        cmp_dct = {}
        cmp_dct[ADFPC.STR_EQM_ID] = self.id
        cls_dct = {}
        cls_dct[ADFPC.STR_ENABLED] = self.classification_enabled
        cls_dct[ADFPC.STR_CLASSIFICATION_MODE] = self.classification_mode
        cls_dct[ADFPC.STR_LATEST_CLASSIF] = self.latest_classification_date
        cls_dct[ADFPC.STR_START] = self.classification_interval[Component.INTV_START]
        cls_dct[ADFPC.STR_END] = self.classification_interval[Component.INTV_END]
        cmp_dct[ADFPC.STR_CLASSIF] = cls_dct
        
        trn_dct = {}
        trn_dct[ADFPC.STR_ENABLED] = self.training_enabled
        trn_dct[ADFPC.STR_START] = self.training_interval[Component.INTV_START]
        trn_dct[ADFPC.STR_END] = self.training_interval[Component.INTV_END]
        cmp_dct[ADFPC.STR_TRAIN] = trn_dct
        return cmp_dct

    def get_flattened_component_list(self) -> List['Component']:
        chld_cmp_list = self.child_components
        cmp_list = [self]
        for cmp in chld_cmp_list:
            cmp_list.extend(cmp.get_flattened_component_list())
        return cmp_list

    def __str__(self):
        return "Component: {} - {} - train: [{}, {}] - classification: [{}, {}]".format(self.__id, self.__name,
                                                                                        self.__trn_interval[Component.INTV_START],
                                                                                        self.__trn_interval[Component.INTV_END],
                                                                                        self.__cls_interval[Component.INTV_START],
                                                                                        self.__cls_interval[Component.INTV_END])


class ModelDescriptor:
    TYPE_ANNCLASSIFIER = 'ANNClassifier'

    def __init__(self, type, version):
        self.__type = type
        self.__version = version

    @property
    def type(self):
        return self.__type

    @property
    def version(self):
        return self.__version

    @property
    def type_and_version(self):
        return "{} {}".format(self.type, self.version)

    def create_model(self, ftr_count):
        pass  # implement in inheriting class


class ANNModelDescriptor(ModelDescriptor):
    HN_MODE_MAX = 'MAX'

    def __init__(self,
                 type,
                 version,
                 epochs=30,
                 hidden_layers=1,
                 hidden_neurons_mode=HN_MODE_MAX,
                 outliers_fraction=0.001,
                 reset_keras_before_fit=True):
        super().__init__(type, version)
        self.__epochs = epochs
        self.__hidden_layers = hidden_layers
        self.__hidden_neurons_mode = hidden_neurons_mode
        self.__outliers_fraction = outliers_fraction
        self.__reset_keras_before_fit = reset_keras_before_fit

    @property
    def epochs(self):
        return self.__epochs

    @property
    def hidden_layers(self):
        return self.__hidden_layers

    @property
    def hidden_neurons_mode(self):
        return self.__hidden_neurons_mode

    @property
    def outliers_fraction(self):
        return self.__outliers_fraction

    @property
    def reset_keras_before_fit(self):
        return self.__reset_keras_before_fit

    def __get_hidden_neuron_layers(self, hnmode, hnlayers, ftr_count):
        if not hnmode in ["MAX", "RECOMMENDED"]:
            logger.warning("Encountered invalid hidden layer mode ({}). Resetting to 'RECOMMENDED'.".format(hnmode))
            hnmode = "RECOMMENDED"

        hn = np.empty((0, hnlayers), int)
        if hnmode == "MAX":
            hn = np.full(hnlayers, ftr_count)
        elif hnmode == "RECOMMENDED":
            hn = np.full(hnlayers, int(ftr_count * 0.5 + 1))

        return list(hn)

    def create_model(self, ftr_count):
        of = 0.001
        try:
            of = self.outliers_fraction  # cfg_dct[ADFPC.STR_OUTLIERS_FRACTION]
        except:
            logger.warning("Using default value for outliers fraction")

        ep = 30
        try:
            ep = self.epochs  # cfg_dct[ADFPC.STR_EPOCHS]
        except:
            logging.warning("Using default value for epochs")

        hnmode = "MAX"
        hnlayers = 1
        try:
            hnmode = self.hidden_neurons_mode  # cfg_dct[ADFPC.STR_HIDDEN_NEURONS]
        except:
            logging.warning("Using default value for hidden neurons mode ({})".format(hnmode))

        try:
            hnlayers = self.hidden_layers  # cfg_dct[ADFPC.STR_HIDDEN_LAYERS]
            if hnlayers < 0:
                hnlayers = 0
                logging.warning("Encountered invalid number of hidden layers ({}). Resetting to {}".format(
                    self.hidden_layers, hnlayers))
            elif hnlayers > 5:
                hnlayers = 5
                logging.warning("Encountered invalid number of hidden layers ({}). Resetting to {}".format(
                    self.hidden_layers, hnlayers))
        except:
            logging.warning("Using default value for hidden layers ({})".format(hnlayers))

        hn = self.__get_hidden_neuron_layers(hnmode, hnlayers, ftr_count)

        rk = True
        try:
            rk = self.reset_keras_before_fit  # cfg_dct[ADFPC.STR_RESET_KERAS_BEFORE_FIT]
        except:
            logging.warning("Using default value for reset Keras before fit")

        return ANNClassifier(outliers_fraction=of, epochs=ep, hidden_neurons=hn, reset_keras_before_fit=rk)


class ExplainerDescriptor:
    TYPE_SHAPEXPLAINER = "shap"

    def __init__(self, type):
        self.__type = type

    @property
    def type(self):
        return self.__type


class ShapExplainerDescriptor(ExplainerDescriptor):
    SUMMARY_TYPE_KMEANS = "kmeans"

    def __init__(self, type, summary_size=5, summary_type=SUMMARY_TYPE_KMEANS):
        super().__init__(type)
        self.__summary_size = summary_size
        self.__summary_type = summary_type

    @property
    def summary_size(self):
        return self.__summary_size

    @property
    def summary_type(self):
        return self.__summary_type


class JobList:
    def __init__(self, fpath):
        self.__job_dct = YMLConfigReader.read_full_path(fpath)

    def get_components(self):
        return self.__job_dct[ADFPC.STR_COMPONENTS]

    def get_train_start(self):
        return self.__job_dct[ADFPC.STR_TRAIN][ADFPC.STR_START]

    def get_train_end(self):
        return self.__job_dct[ADFPC.STR_TRAIN][ADFPC.STR_END]

    def get_train_enabled(self):
        return self.__job_dct[ADFPC.STR_TRAIN][ADFPC.STR_ENABLED]

    def get_site(self):
        return self.__job_dct[ADFPC.STR_SITE]

    def get_classification_start(self):
        try:
            return self.__job_dct[ADFPC.STR_CLASSIF][ADFPC.STR_START]
        except:
            return None

    def get_classification_end(self):
        try:
            return self.__job_dct[ADFPC.STR_CLASSIF][ADFPC.STR_END]
        except:
            return None

    def get_classification_enabled(self):
        return self.__job_dct[ADFPC.STR_CLASSIF][ADFPC.STR_ENABLED]