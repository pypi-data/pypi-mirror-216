import pandas as pd
import numpy as np
from dataclasses import dataclass
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

@dataclass
class FeatureExtractionResults:
    df: pd.DataFrame
    invalid_cycle_cnt: int
    neg_feat_cycle_cnt: int
    zero_feat_cycle_cnt: int
    total_cycle_cnt: int


class FeatureExtractor:
    def __init__(self, keep_neg: bool, keep_zero: bool, invalid_accpt_ratio: float, negative_accpt_ratio: float, zero_accpt_ratio: float):
        self.__keep_neg_feature_vals = keep_neg
        self.__keep_zero_feature_vals = keep_zero
        self.__invalid_accpt_ratio = invalid_accpt_ratio
        self.__negative_accpt_ratio = negative_accpt_ratio
        self.__zero_accpt_ratio = zero_accpt_ratio

        self.__zero_feat_tolerance = 1e-3
        self.__tqdm_enabled = False

    def extract_features(self, df_rawdata: pd.DataFrame, tag_list: list, feature_list: list) -> FeatureExtractionResults:
        return None

    def is_feature_extraction_valid(self, invalid_cycle_cnt, neg_feat_cycle_cnt, zero_feat_cycle_cnt, total_cycle_cnt, mode='EXCLUSIVE'):
        r_inv = round(float(invalid_cycle_cnt) / total_cycle_cnt, 3)
        r_neg = round(float(neg_feat_cycle_cnt) / total_cycle_cnt, 3)
        r_zer = round(float(zero_feat_cycle_cnt) / total_cycle_cnt, 3)

        if invalid_cycle_cnt > 0:
            logger.warning(f"Discarded {invalid_cycle_cnt} cycles ({r_inv}) due to mismatching number of tag values")

        if neg_feat_cycle_cnt > 0:
            logger.warning(f"Discarded {neg_feat_cycle_cnt} cycles ({r_neg}) due to negative features")

        if zero_feat_cycle_cnt > 0:
            logger.warning(f"Discarded {zero_feat_cycle_cnt} cycles ({r_zer}) due to zero features")

        if mode == 'EXCLUSIVE':
            return self.__is_feature_extraction_valid_excl(r_inv, r_neg, r_zer)

        if mode == 'CUMULATIVE':
            return self.__is_feature_extraction_valid_cumul(r_inv, r_neg, r_zer)

    @property
    def keep_negatives(self):
        return self.__keep_neg_feature_vals

    @property
    def keep_zeroes(self):
        return self.__keep_zero_feature_vals

    @property
    def zero_feat_tolerance(self) -> float:
        return self.__zero_feat_tolerance

    @zero_feat_tolerance.setter
    def zero_feat_tolerance(self, zft:float):
        self.__zero_feat_tolerance = zft

    @property
    def progress_enabled(self) -> bool:
        return self.__tqdm_enabled

    @progress_enabled.setter
    def progress_enabled(self, prog_enabled: bool):
        self.__tqdm_enabled = prog_enabled

    def __validate_inputs(self, df_rawdata: pd.DataFrame, tag_list: list, feature_list: list) -> bool:
        return False
    
    def __is_feature_extraction_valid_excl(self, r_inv, r_neg, r_zer):
        if r_inv > self.__invalid_accpt_ratio:
            logger.warning(
                f"Discarded too many cycles ({r_inv} > {self.__invalid_accpt_ratio}) due to mismatching tag values. No features will be returned."
            )
            return False

        if r_neg > self.__negative_accpt_ratio:
            logger.warning(
                f"Discarded too many cycles ({r_neg} > {self.__negative_accpt_ratio}) due to negative features. No features will be returned."
            )
            return False

        if r_zer > self.__zero_accpt_ratio:
            logger.warning(
                f"Discarded too many cycles ({r_zer} > {self.__zero_accpt_ratio}) due to zero features. No features will be returned."
            )
            return False
        return True

    def __is_feature_extraction_valid_cumul(self, r_inv, r_neg, r_zer):
        if r_inv+r_neg+r_zer > self.__invalid_accpt_ratio+self.__negative_accpt_ratio+self.__zero_accpt_ratio:
            logger.error(
                "Overall ratio of discarded cycles is too high. No features will be returned."
            )
            return False
        return True


    @staticmethod
    def build_simple_2wise(keep_neg_feature_vals: bool, keep_zero_feature_vals: bool, invalid_accpt_ratio: float, negative_accpt_ratio: float, zero_accpt_ratio: float) -> 'Simple2WiseFtExtractor':
        return Simple2WiseFtExtractor(keep_neg_feature_vals, keep_zero_feature_vals, invalid_accpt_ratio, negative_accpt_ratio, zero_accpt_ratio)

    @staticmethod
    def build_simple_3wise(keep_neg_feature_vals: bool, keep_zero_feature_vals: bool, invalid_accpt_ratio: float, negative_accpt_ratio: float, zero_accpt_ratio: float) -> 'Simple3WiseFtExtractor':
        return Simple3WiseFtExtractor(keep_neg_feature_vals, keep_zero_feature_vals, invalid_accpt_ratio, negative_accpt_ratio, zero_accpt_ratio)

    @staticmethod
    def build_simple_4wise(keep_neg_feature_vals: bool, keep_zero_feature_vals: bool, invalid_accpt_ratio: float, negative_accpt_ratio: float, zero_accpt_ratio: float) -> 'Simple4WiseFtExtractor':
        return Simple4WiseFtExtractor(keep_neg_feature_vals, keep_zero_feature_vals, invalid_accpt_ratio, negative_accpt_ratio, zero_accpt_ratio)


class Simple2WiseFtExtractor(FeatureExtractor):
    def __validate_inputs(self, df_rawdata: pd.DataFrame, tag_focus_list: list, feature_list: list) -> bool:
        if len(tag_focus_list) != 2:
            return False

        if len(feature_list) != 2:
            return False

        return True

    def extract_features(self, df_rawdata: pd.DataFrame, tag_list: list, feature_list: list) -> FeatureExtractionResults:
        if not self.__validate_inputs(df_rawdata, tag_list, feature_list):
            return None

        tag_name_01 = tag_list[0]
        tag_name_02 = tag_list[1]
        feat_name_01 = feature_list[0]
        feat_name_02 = feature_list[1]

        feat_names_list = []
        feat_values_list = []
        feat_times_list = []

        invalid_cycle_cnt = 0
        neg_feat_cycle_cnt = 0
        zero_feat_cycle_cnt = 0
        for cycle_no in tqdm(df_rawdata.cycle.unique(), disable=not self.progress_enabled):
            df_tmp = df_rawdata[df_rawdata.cycle == cycle_no]

            # here we are implicitly assuming that order is CMD1->INP1->CMD0->INP0: is this correct?
            inp_times = df_tmp[df_tmp.tag == tag_name_02].time.values.astype(np.int64) / int(1e6)
            cmd_times = df_tmp[df_tmp.tag == tag_name_01].time.values.astype(np.int64) / int(1e6)

            try:
                [f1, f2] = (inp_times - cmd_times)
                [f1, f2] = [int(f1), int(f2)]
                s = min([f1, f2])
                if s < 0 and (not self.keep_negatives):
                    logger.debug(
                        f"Discarding cycle {cycle_no} due to negative features ({[f1, f2]})"
                    )
                    neg_feat_cycle_cnt += 1
                elif abs(s) < self.zero_feat_tolerance and (not self.keep_zeroes):
                    logger.debug(
                        f"Discarding cycle {cycle_no} due to zero features ({[f1, f2]}). Tolerance for zero features is {self.zero_feat_tolerance}"
                    )
                    zero_feat_cycle_cnt += 1
                else:
                    feat_names_list.extend([feat_name_01, feat_name_02])
                    feat_values_list.extend([f1, f2])
                    # feature values related to the same cycle should have identical timestamps
                    feat_times_list.extend([df_tmp.time.values[0], df_tmp.time.values[0]])
            except Exception as e:
                invalid_cycle_cnt += 1
                logger.warning(
                    f"Mismatching number of tag values in cycle {cycle_no}...skipping to next cycle.\n{tag_name_02} = {len(inp_times)}, {tag_name_01} = {len(cmd_times)}"
                )
                continue

        if v := self.is_feature_extraction_valid(invalid_cycle_cnt, neg_feat_cycle_cnt, zero_feat_cycle_cnt, len(df_rawdata.cycle.unique()), mode='EXCLUSIVE'):
            return FeatureExtractionResults(
                pd.DataFrame.from_dict(
                    {
                        'vtag': feat_names_list,
                        'vtime': feat_times_list,
                        'vvalue': feat_values_list,
                        'svalue': None
                    }),
                invalid_cycle_cnt,
                neg_feat_cycle_cnt,
                zero_feat_cycle_cnt,
                len(df_rawdata.cycle.unique())
            )
        else:
            return None


class Simple3WiseFtExtractor(FeatureExtractor):
    def __validate_inputs(self, df_rawdata: pd.DataFrame, tag_focus_list: list, feature_list: list) -> bool:
        if len(tag_focus_list) != 3:
            return False

        if len(feature_list) != 4:
            return False

        return True

    def extract_features(self, df_rawdata: pd.DataFrame, tag_list: list, feature_list: list) -> FeatureExtractionResults:
        if not self.__validate_inputs(df_rawdata, tag_list, feature_list):
            return None

        tag_name_01 = tag_list[0]
        tag_name_02 = tag_list[1]
        tag_name_03 = tag_list[2]
        feat_name_01 = feature_list[0]
        feat_name_02 = feature_list[1]
        feat_name_03 = feature_list[2]
        feat_name_04 = feature_list[3]

        feat_names_list = []
        feat_values_list = []
        feat_times_list = []

        invalid_cycle_cnt = 0
        neg_feat_cycle_cnt = 0
        zero_feat_cycle_cnt = 0
        for cycle_no in tqdm(df_rawdata.cycle.unique(), disable=not self.progress_enabled):
            df_tmp = df_rawdata[df_rawdata.cycle == cycle_no]

            cmd_times = df_tmp[df_tmp.tag == tag_name_01].time.values.astype(np.int64) / int(1e6)
            inp_times_ON = df_tmp[df_tmp.tag == tag_name_02].time.values.astype(np.int64) / int(1e6)
            inp_times_OFF = df_tmp[df_tmp.tag == tag_name_03].time.values.astype(np.int64) / int(1e6)

            try:
                [f2, f4] = (inp_times_ON - cmd_times)
                [f1, f3] = (inp_times_OFF - cmd_times)
                [f1, f2, f3, f4] = [int(f1), int(f2), int(f3), int(f4)]
                s = min([f1, f2, f3, f4])
                if s < 0 and (not self.keep_negatives):
                    logger.debug(
                        f"Discarding cycle {cycle_no} due to negative features ({[f1, f2, f3, f4]})"
                    )
                    neg_feat_cycle_cnt += 1
                elif abs(s) < self.zero_feat_tolerance and (not self.keep_zeroes):
                    logger.debug(
                        f"Discarding cycle {cycle_no} due to zero features ({[f1, f2, f3, f4]}). Tolerance for zero features is {self.zero_feat_tolerance}"
                    )
                    zero_feat_cycle_cnt += 1
                else:
                    feat_names_list.extend([feat_name_01, feat_name_02, feat_name_03, feat_name_04])
                    feat_values_list.extend([f1, f2, f3, f4])
                    # feature values related to the same cycle should have identical timestamps
                    feat_times_list.extend(
                        [df_tmp.time.values[0], df_tmp.time.values[0], df_tmp.time.values[0], df_tmp.time.values[0]])
            except Exception as e:
                invalid_cycle_cnt += 1
                logger.warning(
                    f"Mismatching number of tag values in cycle {cycle_no}...skipping to next cycle.\n{tag_name_02} = {len(inp_times_ON)}, {tag_name_01} = {len(inp_times_OFF)}, {tag_name_01} = {len(cmd_times)}"
                )
                continue

        if v := self.is_feature_extraction_valid(invalid_cycle_cnt, neg_feat_cycle_cnt, zero_feat_cycle_cnt,
                                                   len(df_rawdata.cycle.unique()), mode='EXCLUSIVE'):
            return FeatureExtractionResults(
                pd.DataFrame.from_dict(
                    {
                        'vtag': feat_names_list,
                        'vtime': feat_times_list,
                        'vvalue': feat_values_list,
                        'svalue': None
                    }
                ),
                invalid_cycle_cnt,
                neg_feat_cycle_cnt,
                zero_feat_cycle_cnt,
                len(df_rawdata.cycle.unique())
            )
        else:
            return None


class Simple4WiseFtExtractor(FeatureExtractor):
    def __validate_inputs(self, df_rawdata: pd.DataFrame, tag_focus_list: list, feature_list: list) -> bool:
        if len(tag_focus_list) != 4:
            return False

        if len(feature_list) != 4:
            return False

        return True

    def extract_features(self, df_rawdata: pd.DataFrame, tag_list: list, feature_list: list) -> FeatureExtractionResults:
        if not self.__validate_inputs(df_rawdata, tag_list, feature_list):
            return None

        tag_A_01 = tag_list[0]
        tag_A_02 = tag_list[1]
        tag_B_01 = tag_list[2]
        tag_B_02 = tag_list[3]
        feat_name_01 = feature_list[0]
        feat_name_02 = feature_list[1]
        feat_name_03 = feature_list[2]
        feat_name_04 = feature_list[3]

        feat_names_list = []
        feat_values_list = []
        feat_times_list = []

        invalid_cycle_cnt = 0
        neg_feat_cycle_cnt = 0
        zero_feat_cycle_cnt = 0
        for cycle_no in tqdm(df_rawdata.cycle.unique(), disable=not self.progress_enabled):
            df_tmp = df_rawdata[df_rawdata.cycle == cycle_no]

            try:
                # group A tags
                # here we are implicitly assuming that order is CMD1->INP1->CMD0->INP0: is this correct?
                inp_times = df_tmp[df_tmp.tag == tag_A_01].time.values.astype(np.int64) / int(1e6)
                cmd_times = df_tmp[df_tmp.tag == tag_A_02].time.values.astype(np.int64) / int(1e6)

                [f1, f2] = (inp_times - cmd_times)
                [f1, f2] = [int(f1), int(f2)]

                # group B tags
                # here we are implicitly assuming that order is CMD1->INP1->CMD0->INP0: is this correct?
                inp_times = df_tmp[df_tmp.tag == tag_B_01].time.values.astype(np.int64) / int(1e6)
                cmd_times = df_tmp[df_tmp.tag == tag_B_02].time.values.astype(np.int64) / int(1e6)

                [f3, f4] = (inp_times - cmd_times)
                [f3, f4] = [int(f3), int(f4)]
                s = min([f1, f2, f3, f4])
                if s < 0 and (not self.keep_negatives):
                    logger.debug(
                        f"Discarding cycle {cycle_no} due to negative features ({[f1, f2, f3, f4]})"
                    )
                    neg_feat_cycle_cnt += 1
                elif abs(s) < self.zero_feat_tolerance and (not self.keep_zeroes):
                    logger.debug(
                        f"Discarding cycle {cycle_no} due to zero features ({[f1, f2, f3, f4]}). Tolerance for zero features is {self.zero_feat_tolerance}"
                    )
                    zero_feat_cycle_cnt += 1
                else:
                    feat_names_list.extend([feat_name_01, feat_name_02, feat_name_03, feat_name_04])
                    feat_values_list.extend([f1, f2, f3, f4])
                    # feature values related to the same cycle should have identical timestamps
                    feat_times_list.extend(
                        [df_tmp.time.values[0], df_tmp.time.values[0], df_tmp.time.values[0], df_tmp.time.values[0]])
            except Exception as e:
                invalid_cycle_cnt += 1
                logger.warning(
                    f"Mismatching number of tag values in cycle {cycle_no}...skipping to next cycle"
                )
                continue

        if v := self.is_feature_extraction_valid(invalid_cycle_cnt, neg_feat_cycle_cnt, zero_feat_cycle_cnt,
                                                   len(df_rawdata.cycle.unique()), mode='EXCLUSIVE'):
            return FeatureExtractionResults(
                pd.DataFrame.from_dict(
                    {'vtag': feat_names_list, 'vtime': feat_times_list, 'vvalue': feat_values_list, 'svalue': None}
                ),
                invalid_cycle_cnt,
                neg_feat_cycle_cnt,
                zero_feat_cycle_cnt,
                len(df_rawdata.cycle.unique())
            )
        else:
            return None