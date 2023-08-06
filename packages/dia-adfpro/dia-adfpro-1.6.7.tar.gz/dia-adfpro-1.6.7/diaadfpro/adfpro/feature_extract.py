import getopt
import logging.config
import os
import pathlib
import sys
import time
from datetime import datetime, timedelta
from enum import Enum
import warnings
from collections import Counter

import numpy as np
import pandas as pd
import pytz
import copy
from tqdm import tqdm
from tzlocal import get_localzone  # $ pip install tzlocal
from dataclasses import dataclass

from aimltools.ts.utils.pi_utils import BoundaryType, PIReader
from aimltools.ts.preprocessing import segmentation, prune

sys.path.insert(0, str(pathlib.Path(__file__).parent.resolve().parent.resolve().parent))
from diaadfpro.adfpro.feature_extractors import FeatureExtractor

import diaadfpro
from diaadfpro.adfpro.constants import ADFPC
from diaadfpro.adfpro.utils import YMLConfigReader, IOUtils, ADFPDateUtils

logger = logging.getLogger(__name__)
warnings.simplefilter(action='ignore', category=FutureWarning)

DEFAULT_TS_FORMAT = 'YYYY-MM-DD hh:mm:ss+hh:mm'

class FeatureExtractExitCodes(Enum):
    NO_ERRORS = 0
    TAG_VALUE_MISMATCH = 1
    ERR_INVALID_CYCLE_IDENTIFICATION_MODE = 2
    ERR_DATA_PREPARATION = 3
    NO_CYCLES_CONTAINING_TAG_VALUES = 4
    ERR_FEATURE_EXTRACTION = 5
    ERR_WRITE_FEATURES = 6
    ERR_TIME_FORMAT = 7
    ERR_INVALID_FEATURE_CALCULATION_MODE = 8
    EMPTY_CAPSULE_LIST = 9
    EMPTY_TAGVALUE_LIST = 10
    EMPTY_FEATURE_DF = 11
    UNSPECIFIED_ERROR = 1000

@dataclass
class FeatureExtractionResults:
    df: pd.DataFrame
    invalid_cycle_cnt: int
    neg_feat_cycle_cnt: int
    zero_feat_cycle_cnt: int
    total_cycle_cnt: int

# test with tags specified in:
# - https://collab.lilly.com/:x:/r/sites/EdgeComputingforIRMAReliabilityMonitoring/_layouts/15/Doc.aspx?sourcedoc=%7B9F453720-4CF7-4E95-9ECA-D8B930EDD146%7D&file=edge_R2WET.xlsx&action=default&mobileredirect=true
# - source PI: XF2EASYPID01.mfg.ema.lilly.com

class DataPreparator:
    def __init__(self):
        pass

    def prepare_data(self, df):
        pass

    @staticmethod
    def build_sequencer_data_preparator(tag_sequencer: str, tag_list: list, tag_sequencer_thr: int) -> "SequencerDataPreparator":
        return SequencerDataPreparator(tag_sequencer, tag_list,  tag_sequencer_thr)

    @staticmethod
    def build_capsule_data_preparator(df_capsules: pd.DataFrame, adjust_capsules_for_resolution=True, resolution_millisec=51) -> "CapsuleDataPreparator":
        return CapsuleDataPreparator(df_capsules, adjust_capsules_for_resolution, resolution_millisec)


class SequencerDataPreparator(DataPreparator):
    def __init__(self, tag_sequencer: str, tag_list: list, tag_sequencer_thr: int, alpha_prefix = '!_'):
        self.__tag_sequencer = tag_sequencer
        self.__tag_list = tag_list
        self.__tag_focus_list = [tag_sequencer]
        self.__tag_focus_list.extend(tag_list)
        self.__tag_sequencer_thr = tag_sequencer_thr
        self.__alpha_prefix = alpha_prefix

    def prepare_data(self, df):
        df = df[df.tag.isin(self.__tag_focus_list)]
        #SequencerDataPreparator.__switch_values(df, tagname=self.__tag_focus_list[2], value1=1, value2=0)
        df.loc[(df.tag == self.__tag_sequencer), 'tag'] = self.__alpha_prefix + self.__tag_sequencer

        tag_cutter = self.__alpha_prefix + self.__tag_sequencer

        def segmenting_rule_fn(df):
            return (df.tag == tag_cutter) & (df.value == self.__tag_sequencer_thr)

        try:
            df_segm = segmentation(df, segmenting_rule_fn, signal_col='value', order=True, orderby_cols=['time', 'tag'])
            df_clean = prune(df_segm, self.__tag_list, low_perc=0.25, hi_perc=0.75)
            logger.info("Cycles after segmentation: {}. After cleaning: {}. Sequence tag: {}. Threshold: {}.".format(
                len(df_segm.cycle.unique()), len(df_clean.cycle.unique()), tag_cutter, self.__tag_sequencer_thr))
        except Exception as e:
            logger.error("Error during segmentation or prune. Cannot identify cycles correctly.")
            logger.error("Details: {}".format(e))
            return None
        return df_clean

    @staticmethod
    def __switch_values(df, tagname, value1, value2):
        df.loc[(df.tag == tagname) & (df.value == value1), 'value'] = 2
        df.loc[(df.tag == tagname) & (df.value == value2), 'value'] = value1
        df.loc[(df.tag == tagname) & (df.value == 2), 'value'] = value2


class CapsuleDataPreparator(DataPreparator):
    def __init__(self, df_capsules, adjust_capsules_for_resolution=True, resolution_millisec=51):
        self.__df_capsules = df_capsules
        self.__adjust_capsules_for_resolution = adjust_capsules_for_resolution
        self.__resolution_millisec = resolution_millisec

    def prepare_data(self, df):
        if self.__df_capsules is None:
            logger.error("Cannot prepare data with an empty set of capsules!")
            raise(Exception("Cannot prepare data with an empty set of capsules!"))

        df['cycle'] = np.nan
        for r in self.__df_capsules.itertuples():
            cycle_index = int(r[0])
            tstart = r[2]
            if self.__adjust_capsules_for_resolution:
                tstart = tstart - timedelta(seconds=self.__resolution_millisec/1000)

            tend = r[3]
            if self.__adjust_capsules_for_resolution:
                tend = tend + timedelta(seconds=self.__resolution_millisec / 1000)

            idx = df[(df.time >= tstart) & (df.time <= tend)].index
            df.loc[idx, ('cycle')] = cycle_index

        # some observations may not fall in any capsule (cycle) -> let's drop these
        count_na = df['cycle'].isna().sum()
        count_tot = len(df)
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        logger.info(f"Cycles identified using Seeq capsules: {len(df.cycle.unique())}")
        logger.warning(f"{count_na} tag values out of {count_tot} were discarded since they did not fall into any cycle")
        return df


class PIFeatureExtractor:

    def __init__(self, pi_params_dct, alpha_prefix = '!_', invalid_cycles_thr_seg = 0.05, invalid_cycles_thr_negftr = 0.05, invalid_cycles_thr_zerftr = 0.05, tqdm_enabled = False):
        self.__alpha_prefix = alpha_prefix
        self.__invalid_cycles_thr_seg = invalid_cycles_thr_seg
        self.__invalid_cycles_thr_negftr = invalid_cycles_thr_negftr
        self.__invalid_cycles_thr_zerftr = invalid_cycles_thr_zerftr
        self.__zero_feat_tolerance = 0.01

        self.__tqdm_enabled = tqdm_enabled
        self.__pi_srv_url = pi_params_dct['server']
        if pi_params_dct['method'] == 'osi sdk':
            self.__pi_reader = PIReader.build_afsdk_pireader(pi_params_dct['server'], "%Y-%m-%d %H:%M:%S", "yyyy-MM-ddTHH:mm:ss.fff", BoundaryType.INSIDE)
        elif pi_params_dct['method'] == 'seeq':
            seeq_pwd = os.environ[pi_params_dct['password envvar']]
            self.__pi_reader = PIReader.build_seeq_pireader(pi_params_dct['server'], pi_params_dct['user'], seeq_pwd, pi_params_dct['proxy'])
        else:
            raise BaseException(f"Unknown PI read method specified in config file ('{pi_params_dct['method']}')")

    @property
    def pi_server_url(self):
        return self.__pi_srv_url

    def read_tag_data(self, taglist, start_ts, end_ts):
        taglist = list(set(taglist)) #avoid duplicated tags...
        pi_data = self.__pi_reader.read_tags(taglist, start_ts, end_ts)
        pi_data['time'] = pd.to_datetime(pi_data['time'], unit='ms', origin='unix')
        return pi_data

    def read_capsule_data(self, capsule_id_list, start_ts, end_ts, workbook_id=None, by_name=False):
        df_capsules = None
        try:
            logger.info(f"Searching for capsules. Capsule id: {capsule_id_list}, workbook: {workbook_id}, start: {start_ts}, end: {end_ts}, by name: {by_name}")
            if by_name:
                if workbook_id is None:
                    logger.warning("Searching by name with no workbook scope: may get multiple capsules with the same name!")
                    df_capsules = self.__pi_reader.read_capsules(capsule_id_list, start_ts, end_ts, by_name=by_name)
                else:
                    df_capsules = self.__pi_reader.read_capsules(capsule_id_list, start_ts, end_ts, workbook_id=workbook_id, by_name=by_name)
            else:
                if workbook_id is None:
                    logger.warning("Searching by ID requires a valid workbook ID!")
                else:
                    df_capsules = self.__pi_reader.read_capsules(capsule_id_list, start_ts, end_ts, workbook_id=workbook_id, by_name=by_name)

            if (df_capsules is None) or (len(df_capsules) == 0):
                logger.warning(f"No capsules identified with given parameters")
            else:
                df_capsules['Capsule Start'] = pd.to_datetime(df_capsules['Capsule Start'], unit='ms', origin='unix')
                df_capsules['Capsule End'] = pd.to_datetime(df_capsules['Capsule End'], unit='ms', origin='unix')

            return df_capsules
        except AttributeError as e1:
            logger.error("Details: {}".format(e1))
            logger.error("Error retrieving capsules: please make sure an instance of SeekPIReader is used")
            logger.error("For SeekPIReader, please specify 'method: seeq' in the configuration file")
            return None
        except Exception as e1:
            logger.error("Details: {}".format(e1))
            return None

    def two_tag_feature_extractor(self, df, tag_list, feat_names, keep_negatives=False, keep_zero=False):

        try:
            df_clean_4val = self.__purge_invalid_cycles(df, 4)
        except AssertionError:
            logger.error("Percentage of cycles with an invalid number of values ({}) exceeds {}".format(4, self.__invalid_cycles_thr_seg))
            return None
        except Exception as e:
            logger.error("Error eliminating cycles with an invalid number of values")
            logger.error("Details: {}".format(e))
            return None

        logger.info("Cycles after purging invalid ones: {}".format(len(df_clean_4val.cycle.unique())))
        logger.info("Starting feature calculation")
        try:
            f_extractor = FeatureExtractor.build_simple_2wise(keep_negatives, keep_zero, self.__invalid_cycles_thr_seg, self.__invalid_cycles_thr_negftr, self.__invalid_cycles_thr_zerftr)
            ft_extract_results = f_extractor.extract_features(df_clean_4val, tag_list, feat_names)
            return ft_extract_results
        except Exception as e:
            logger.error("Error while calculating features (2-wise)")
            logger.error("Details: {}".format(e))
            return None

    def three_tag_feature_extractor(self, df, tag_list, feat_names, keep_negatives=False, keep_zero=False):

        try:
            df_clean_4val = self.__purge_invalid_cycles(df, 6)
        except AssertionError:
            logger.error("Percentage of cycles with an invalid number of values ({}) exceeds {}".format(6, self.__invalid_cycles_thr_seg))
            return None
        except Exception as e:
            logger.error("Error eliminating cycles with an invalid number of values")
            logger.error("Details: {}".format(e))
            return None

        logger.info("Cycles after purging invalid ones: {}".format(len(df_clean_4val.cycle.unique())))
        logger.info("Starting feature calculation")
        try:
            f_extractor = FeatureExtractor.build_simple_3wise(keep_negatives, keep_zero, self.__invalid_cycles_thr_seg,
                                                              self.__invalid_cycles_thr_negftr,
                                                              self.__invalid_cycles_thr_zerftr)
            ft_extract_results = f_extractor.extract_features(df_clean_4val, tag_list, feat_names)
            return ft_extract_results
        except Exception as e:
            logger.error("Error while calculating features (3-wise)")
            logger.error("Details: {}".format(e))
            return None
        
    def four_tag_feature_extractor(self, df, tag_list, feat_names, keep_negatives=False, keep_zero=False):
        try:
            df_clean_8val = self.__purge_invalid_cycles(df, 8)
        except AssertionError:
            logger.error("Percentage of cycles with an invalid number of values ({}) exceeds {}".format(8, self.__invalid_cycles_thr_seg))
            return None
        except Exception as e:
            logger.error("Error eliminating cycles with an invalid number of values")
            logger.error("Details: {}".format(e))
            return None

        logger.info("Cycles after purging invalid ones: {}".format(len(df_clean_8val.cycle.unique())))
        logger.info("Starting feature calculation")
        try:
            f_extractor = FeatureExtractor.build_simple_4wise(keep_negatives, keep_zero, self.__invalid_cycles_thr_seg,
                                                              self.__invalid_cycles_thr_negftr,
                                                              self.__invalid_cycles_thr_zerftr)
            ft_extract_results = f_extractor.extract_features(df_clean_8val, tag_list, feat_names)
            return ft_extract_results
        except Exception as e:
            logger.error("Error while calculating features (4-wise)")
            logger.error("Details: {}".format(e))
            return None

    def __purge_invalid_cycles(self, df, value_thr):
        logger.info(
            f"Purging cycles having an invalid number of values (!={value_thr}) and ensuring their percentage does not exceed {self.__invalid_cycles_thr_seg}"
        )
        nc = len(df.cycle.unique())

        df_values_per_cycle = df.pivot_table(columns='cycle', aggfunc='size', fill_value=0)
        df_more = df_values_per_cycle[df_values_per_cycle > value_thr]
        df_less = df_values_per_cycle[df_values_per_cycle < value_thr]

        rm = round(float(len(df_more)) / nc, 3)
        rl = round(float(len(df_less)) / nc, 3)

        logger.debug(
            f"Found {len(df_more)} cycles ({rm}) with more than {value_thr} values"
        )
        logger.debug(
            f"Found {len(df_less)} cycles ({rl}) with less than {value_thr} values"
        )

        logger.info(f"<{value_thr} values: {rl} - >{value_thr} values: {rm}")
        # we do not want to discard too many cycles...
        assert (rm <= self.__invalid_cycles_thr_seg)
        assert (rl <= self.__invalid_cycles_thr_seg)

        discarded_cycles = sorted(list(set(df_less.index.values) | set(df_more.index.values)))
        assert (len(discarded_cycles) == len(df_less) + len(df_more))

        df_purged = df.drop(df[df.cycle.isin(discarded_cycles)].index)
        assert (len(df_purged.cycle.unique()) == (len(df.cycle.unique()) - len(discarded_cycles)))
        return df_purged


def parse_options(argv):
    options, remainder = getopt.getopt(argv, 'c:d:', ['config=', 'data='])
    logging.info(f"Options: {options}")
    cfg_path = ""
    data_path = ""
    for opt, arg in options:
        if opt in ('-c', '--config'):
            cfg_path = arg
        elif opt in ('-d', '--data'):
            data_path = arg

    return [cfg_path, data_path]

def use_fixed_time_interval(cfg_dict: dict):
    use_custom_ts = False
    if 'custom timestamps' in cfg_dict:
        use_custom_ts = True
    return use_custom_ts

def get_fixed_time_interval(cfg_dict: dict):
    start_ts = cfg_dict['custom timestamps']['start']
    if isinstance(start_ts, str) or (not ADFPDateUtils.is_tz_aware(start_ts)):
        logger.error("Start time should be timezone aware! Please fix it in cfg_dict[\'custom timestamps\'][\'start\']")
        logger.error("Please use {} as a format".format(DEFAULT_TS_FORMAT))
        return None
    end_ts = cfg_dict['custom timestamps']['end']
    if isinstance(end_ts, str) or (not ADFPDateUtils.is_tz_aware(end_ts)):
        logger.error("End time should be timezone aware! Please fix it in cfg_dict[\'custom timestamps\'][\'start\']")
        logger.error("Please use {} as a format".format(DEFAULT_TS_FORMAT))
        return None
    return [start_ts, end_ts]

def get_data(pife: PIFeatureExtractor, start_ts, end_ts, max_ti_len_hrs, tag_list, data_path = None, df_data = None):
    try:
        if data_path:
            # filter out data read from local parquet file...
            df = df_data[(df_data.time > str(start_ts)) & (df_data.time < str(end_ts))]
            logger.info("Read from local file ({}). Extracted {} tag values.".format(data_path, len(df)))
        else:
            df = pife.read_tag_data(tag_list, str(start_ts), str(end_ts))
            logger.info("Read from PI ({}). Extracted {} tag values.".format(pife.pi_server_url, len(df)))
        return df
    except Exception as e:
        logger.error("Failure while reading {}".format(tag_list))
        logger.error("Details: {}".format(e))
        logger.error("Skipping to the next component")
        return None

class FeatureCalculationMode(Enum):
    UNKNOWN = 1
    SIMPLE_2WISE = 2
    SIMPLE_3WISE = 3
    SIMPLE_4WISE = 4


class FeatureExtractionParameters:
    tags_list: list
    thr_val: int
    tag_sequencer_name: str
    capsule_id: str
    feats_list: list
    keep_neg_feature_vals: bool
    keep_zero_feature_vals: bool

    feature_calculation_mode: FeatureCalculationMode

    @property
    def full_tag_list(self):
        if self.tag_sequencer_name:
            return [self.tag_sequencer_name] + self.tags_list
        else:
            return self.tags_list

    def infer_feature_calculation_mode(self):
        if len(self.tags_list) == 2:
            self.feature_calculation_mode = FeatureCalculationMode.SIMPLE_2WISE
        elif len(self.tags_list) == 3:
            self.feature_calculation_mode = FeatureCalculationMode.SIMPLE_3WISE
        elif len(self.tags_list) == 4:
            self.feature_calculation_mode = FeatureCalculationMode.SIMPLE_4WISE
        else:
            logger.error("Unable to infer calculation mode")


    def set_feature_calculation_mode(self, cmode_str: str):
        pass

    @staticmethod
    def build_from_dictionary(cmp_dct):
        fep = FeatureExtractionParameters()
        fep.tags_list = cmp_dct['tags']

        if 'sequencer' in cmp_dct:
            fep.thr_val = cmp_dct['threshold']
            fep.tag_sequencer_name = cmp_dct['sequencer']

        if 'capsule' in cmp_dct:
            fep.capsule_id = cmp_dct['capsule']

        if 'feat calculation mode' in cmp_dct:
            fep.set_feature_calculation_mode(cmp_dct['feat calculation mode'])
        else:
            fep.infer_feature_calculation_mode()

        fep.feats_list = cmp_dct['features']

        fep.keep_neg_feature_vals = False
        if 'keep negative features' in cmp_dct.keys():
            fep.keep_neg_feature_vals = cmp_dct['keep negative features']

        fep.keep_zero_feature_vals = True
        if 'keep zero features' in cmp_dct.keys():
            fep.keep_zero_feature_vals = cmp_dct['keep zero features']

        if not fep.keep_neg_feature_vals:
            logger.warning("Please note that cycles having negative feature values will be DISCARDED (idea is that this denotes bad segmentation)")

        if not fep.keep_zero_feature_vals:
            logger.warning("Please note that cycles having feature values equal to zero will be DISCARDED (idea is that zero features are due to PLC 50ms resolution limit)")

        return fep


def failed(exit_codes):
    errs = [FeatureExtractExitCodes.ERR_INVALID_CYCLE_IDENTIFICATION_MODE,
            FeatureExtractExitCodes.ERR_DATA_PREPARATION,
            FeatureExtractExitCodes.ERR_FEATURE_EXTRACTION,
            FeatureExtractExitCodes.ERR_WRITE_FEATURES,
            FeatureExtractExitCodes.ERR_TIME_FORMAT,
            FeatureExtractExitCodes.ERR_INVALID_FEATURE_CALCULATION_MODE]

    if len(set(errs).intersection(exit_codes)) > 0:
        return True

    return False


def reset_time_interval_start(start_ts, end_ts, max_ti_len_hrs):
    new_start_ts = start_ts
    diff = end_ts - new_start_ts
    if diff.total_seconds() > max_ti_len_hrs * 3600:
        new_start_ts = end_ts - timedelta(hours=max_ti_len_hrs)
        logger.warning("Time interval duration exceeds limit ({} hrs). Risk of overloading PI server.".format(
            max_ti_len_hrs))
        logger.warning("RE-SETTING INTERVAL START TO {}.".format(str(new_start_ts)))
        logger.warning("NEW TIME INTERVAL IS: ({}, {})".format(new_start_ts, end_ts))
    return new_start_ts

def main(argv):
    if len(argv) < 1:
        logger.error("Not enough input arguments")
        sys.exit(1)

    [cfg_path, data_path] = parse_options(argv)
    logger.info("Using configuration file: {}".format(cfg_path))

    cfg_dict = YMLConfigReader.read_full_path(cfg_path)

    if not 'log cfg file' in cfg_dict:
        logger.error("Please specify a valid path to a configuration file for the logger")
        logger.error("Use \'{}\' as a key in {}".format('log cfg file', cfg_path))
        sys.exit(1)
    else:
        featextract_cfg_log_path = cfg_dict['log cfg file']
        logging.config.fileConfig(featextract_cfg_log_path, disable_existing_loggers=False)
        logger.warning("Using log configuration file at {}".format(featextract_cfg_log_path))

    logger.info(">>> Start data extraction and feature calculation <<<")
    logger.info("Using {} from ADFPRO {}".format(__file__, diaadfpro.__version__))

    fixed_ti = use_fixed_time_interval(cfg_dict)
    if fixed_ti:
        [start_ts, end_ts] = get_fixed_time_interval(cfg_dict)
    else:
        # end_ts can be immediately set
        # start_ts needs to be calculated based on the latest date when a component was last processed
        end_ts = datetime.now(pytz.timezone(str(get_localzone())))

    if data_path:
        df_data_from_file = pd.read_parquet(data_path)
        logger.warning("Reading data from local file parquet file ({})".format(data_path))

    cmp_dict = cfg_dict['components']
    max_ti_len_hrs = cfg_dict['max time interval len (h)']
    cycle_identification_mode = cfg_dict['cycle identification mode']
    pife = PIFeatureExtractor(cfg_dict['pi read'], cfg_dict['alpha prefix'], cfg_dict['invalid cycles thr'],
                              cfg_dict['invalid cycles thr nf'], cfg_dict['invalid cycles thr zf'],
                              cfg_dict['show progress'])

    adjust_capsules_for_resolution = True
    if 'adjust capsules' in cfg_dict['pi read']:
        adjust_capsules_for_resolution = cfg_dict['pi read']['adjust capsules']

    read_by_name = False
    if 'capsule search mode' in cfg_dict['pi read']:
        if cfg_dict['pi read']['capsule search mode'] == 'name':
            read_by_name = True

    workbook_id = None
    if 'seeq workbook id' in cfg_dict['pi read']:
        workbook_id = cfg_dict['pi read']['seeq workbook id']

    resolution_millisec = 50
    if 'resolution millisec' in cfg_dict['pi read']:
        resolution_millisec = cfg_dict['pi read']['resolution millisec']

    tot_cmp = len(cmp_dict.keys())
    cur_cmp = 0
    exit_codes = []
    start_calc = time.time()
    for cmp_name in cmp_dict.keys():
        logger.info(f"===Calculating features for component {cmp_name} ({cur_cmp} of {tot_cmp})")
        start_cmp_calc = time.time()
        cur_cmp += 1
        
        fep = FeatureExtractionParameters.build_from_dictionary(cmp_dict[cmp_name])
        logger.info("Tags: {}".format(fep.tags_list))

        if not fixed_ti:
            start_ts = cmp_dict[cmp_name]['latest']
            if isinstance(start_ts, str) or (not ADFPDateUtils.is_tz_aware(start_ts)):
                exit_codes.append(FeatureExtractExitCodes.ERR_TIME_FORMAT)
                logger.error("Start time should be timezone aware! Please fix it in the 'latest' key of the configuration file, related to the component named {}".format(cmp_name))
                logger.error("Please use {} as a format".format(DEFAULT_TS_FORMAT))
                logger.error("Skipping to the next component")
                continue

        logger.info("Time interval: ({}, {})".format(start_ts, end_ts))
        start_ts = reset_time_interval_start(start_ts, end_ts, max_ti_len_hrs)

        if cycle_identification_mode == 'sequencer':
            data_prep = DataPreparator.build_sequencer_data_preparator(fep.tag_sequencer_name, fep.tags_list, fep.thr_val)
        elif cycle_identification_mode == 'capsules':
            fep.tag_sequencer_name = None
            logger.info(f"Building capsule data preparator. Workbook: {workbook_id}, capsule: {fep.capsule_id}, by name: {read_by_name}")
            df_capsules = pife.read_capsule_data([fep.capsule_id], start_ts, end_ts, workbook_id=workbook_id, by_name=read_by_name)
            if df_capsules is None:
                # warning already logged in pife.read_capsule_data...no need to log again
                exit_codes.append(FeatureExtractExitCodes.EMPTY_CAPSULE_LIST)
                continue
            else:
                data_prep = DataPreparator.build_capsule_data_preparator(df_capsules, adjust_capsules_for_resolution, resolution_millisec)
        else:
            exit_codes.append(FeatureExtractExitCodes.ERR_INVALID_CYCLE_IDENTIFICATION_MODE)
            logger.error(f"Invalid cycle identification mode: {cycle_identification_mode}")
            logger.error("Skipping to the next component")
            continue

        if data_path:
            df = get_data(pife, start_ts, end_ts, max_ti_len_hrs, fep.full_tag_list, data_path, df_data_from_file)
        else:
            df = get_data(pife, start_ts, end_ts, max_ti_len_hrs, fep.full_tag_list)

        if len(df) == 0:
            exit_codes.append(FeatureExtractExitCodes.EMPTY_TAGVALUE_LIST)
            logger.warning("No tag values available in given time interval. Tags: {}, start: {}, end: {}".format(fep.tags_list, start_ts, end_ts))
            continue

        try:
            df_clean = data_prep.prepare_data(df)
        except:
            exit_codes.append(FeatureExtractExitCodes.ERR_DATA_PREPARATION)
            logger.error(f"Unable to run data preparation (cycle segmentation related operations)")
            logger.error("Skipping to the next component")
            continue

        if len(df_clean) == 0:
            exit_codes.append(FeatureExtractExitCodes.NO_CYCLES_CONTAINING_TAG_VALUES)
            logger.error(f"Unable to identify any cycle that contains valid tag values")
            logger.error("Skipping to the next component")
            continue

        if fep.feature_calculation_mode == FeatureCalculationMode.SIMPLE_2WISE:
            feat_extr_results = pife.two_tag_feature_extractor(df_clean, fep.tags_list, fep.feats_list, fep.keep_neg_feature_vals, fep.keep_zero_feature_vals)
        elif fep.feature_calculation_mode == FeatureCalculationMode.SIMPLE_3WISE:
            feat_extr_results = pife.three_tag_feature_extractor(df_clean, fep.tags_list, fep.feats_list, fep.keep_neg_feature_vals, fep.keep_zero_feature_vals)
        elif fep.feature_calculation_mode == FeatureCalculationMode.SIMPLE_4WISE:
            feat_extr_results = pife.four_tag_feature_extractor(df_clean, fep.tags_list, fep.feats_list, fep.keep_neg_feature_vals, fep.keep_zero_feature_vals)
        else:
            exit_codes.append(FeatureExtractExitCodes.ERR_INVALID_FEATURE_CALCULATION_MODE)
            logger.error("Unknown feature calculation mode. Skipping to next component.")
            continue

        if feat_extr_results is None:
            exit_codes.append(FeatureExtractExitCodes.ERR_FEATURE_EXTRACTION)
            logger.error("Error calculating features or empty feature set. Skipping to next component.")
            continue

        df_feat = feat_extr_results.df
        if df_feat is None or len(df_feat) == 0:
            exit_codes.append(FeatureExtractExitCodes.EMPTY_FEATURE_DF)
            logger.warning("Error calculating features or empty feature set. Skipping to next component.")
            continue
            
        logger.info("Calculated {} feature rows".format(len(df_feat)))

        # write features to DB and update timestamp on configuration file
        dbp = cfg_dict['DB']
        if dbp[ADFPC.STR_WRITE_ENABLED]:
            try:
                start = time.time()
                logger.info("Start writing features...")
                IOUtils.write_features(df_feat, dbp, os.environ[dbp[ADFPC.STR_PWD_ENVVAR]])
                tsecs = round(time.time()-start, 2)
                logger.info("Wrote {} feature rows. Time: {}s (includes query preparation).".format(len(df_feat), tsecs))
                if not fixed_ti:
                    #save time on yml file
                    cmp_dict[cmp_name]['latest'] = copy.deepcopy(end_ts)
                    YMLConfigReader.write(cfg_dict, cfg_path)
                    logger.info("Updated latest timestamp for successful feature calculation")
            except Exception as e:
                exit_codes.append(FeatureExtractExitCodes.ERR_WRITE_FEATURES)
                logger.error("Error while writing features or updating timestamp on configuration file")
                logger.error("Details: {}".format(e))

        if 'dump csv' in cfg_dict:
            p = pathlib.Path(cfg_dict['dump csv'], cmp_name + '.csv')
            logger.info("Dump features to csv file ({})".format(str(p)))
            df_feat.to_csv(p)

        exit_codes.append(FeatureExtractExitCodes.NO_ERRORS)
        logger.info("===Component {} completed".format(cmp_name))
        tsecs = round(time.time() - start_cmp_calc, 2)
        logger.info(f"===Time: {tsecs}s (includes writing if enabled).")
    logger.info(">>> Feature calculation completed for all components in configuration file <<<")
    logger.info(">>> Count of exit codes <<<")
    logger.info(f">>> Total: {len(exit_codes)}")
    c = Counter(exit_codes)
    for n in c.keys():
        logger.info(f">>> {n}: {c[n]}")

    tsecs = round(time.time() - start_calc, 2)
    logger.info(f">>> Time {tsecs}s <<<")
    if failed(exit_codes):
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    #use -d "C:/Users/c206539/Downloads/M24-STXX.tag.parquet" for reading from local parquet file
    try:
        main(sys.argv[1:])
    except Exception as e:
        logger.error("Failure while running feature extraction")
        logger.error(f"Details: {e}")





