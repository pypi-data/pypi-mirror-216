"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

from pathlib import Path
import json
import logging
import pandas as pd
import numpy as np
from aimltools.ts.distances import DTWMixin
from aimltools.ts.golden import real_golden_cycle
from aimltools.ts.preprocessing import prune, segmentation
from tqdm import tqdm
import time
import inspect

from diaadfpro.adfpro.utils import YMLConfigReader, PlotUtils

logger = logging.getLogger(__name__)


class GoldenCycleHelper():
    def __init__(self, tagfield="tag", timefield="time", valuefield="value", cyclefield="cycle"):
        self.__tagfield = tagfield
        self.__timefield = timefield
        self.__valuefield = valuefield
        self.__cyclefield = cyclefield

    def set_output_path(self, out_path):
        self.__out_path = out_path

    def set_pruning_percentiles(self, low_perc=0.25, hi_perc=0.75):
        self.__low_perc = low_perc
        self.__hi_perc = hi_perc

    def calculate_golden_from_cfg(self, cfg_file_path, fn_loader):
        cfg_dict = YMLConfigReader.read_full_path(cfg_file_path)
        global_start = time.time()

        base_parquet_folder_name = cfg_dict['source']
        for cmp in cfg_dict['components'].keys():
            cmp_start = time.time()

            cmp_data_dict = cfg_dict['components'][cmp]
            golden_calc_enabled = cmp_data_dict['enabled']

            if not golden_calc_enabled:
                logger.info("====skipping {}: golden calculation not enabled".format(cmp))
                continue

            generate_diagnostics = cmp_data_dict['diagnostics']
            sequence_tag = cmp_data_dict['sequencer']
            sequence_thr = cmp_data_dict['sequence threshold']
            sequence_thr_end = None
            try:
                sequence_thr_end = cmp_data_dict['sequence threshold end']
            except:
                pass

            sequence_thr_after = None
            try:
                sequence_thr_after = cmp_data_dict['sequence threshold after']
            except:
                pass

            taglist = cmp_data_dict['taglist']
            time_start = cmp_data_dict['time start']
            time_end = cmp_data_dict['time end']

            logger.info("====processing " + cmp)
            logger.info("loading data in interval [{}, {}]".format(time_start, time_end))
            parquet_folder_name = base_parquet_folder_name.format(cmp)
            start = time.time()
            df = fn_loader(parquet_folder_name, self.__valuefield, self.__tagfield, self.__timefield, taglist,
                           [time_start, time_end])
            logger.info("data loaded in {:.3f}s".format(time.time() - start))

            if len(df) == 0:
                logger.error("no data found")
                return

            logger.info(
                "retained data in [{}, {}]".format(df[self.__timefield].values[0], df[self.__timefield].values[-1]))

            taglist_read = df[self.__tagfield].unique()
            taglist_read.sort()
            taglist.sort()

            assert (list(taglist_read) == taglist)

            taglist.remove(sequence_tag)
            logger.info("segmenting and pruning...")
            start = time.time()
            if sequence_thr_end is None:
                def fn(df):
                    return (df[self.__tagfield] == sequence_tag) & (df[self.__valuefield] == sequence_thr)

                logger.info("...using segmentation function:\n{}".format(inspect.getsource(fn)))
                df = GoldenCycleHelper.segment_and_prune(df, taglist, fn)
            else:
                if sequence_thr_after is None:
                    logger.info("...using 2-edges segmentation")
                    df_segm = GoldenCycleHelper.segment_two_edges(df, self.__tagfield, self.__timefield,
                                                                  self.__valuefield, self.__cyclefield, sequence_tag,
                                                                  sequence_thr, sequence_thr_end, order_columns=True)
                else:
                    logger.info("...using 2-edges segmentation (enhanced)")
                    df_segm = GoldenCycleHelper.segment_two_edges_enh(df, self.__tagfield, self.__timefield,
                                                                      self.__valuefield, self.__cyclefield,
                                                                      sequence_tag, sequence_thr, sequence_thr_end,
                                                                      sequence_thr_after, order_columns=True)

                logger.info("...found {} cycles".format(len(df_segm[self.__cyclefield].unique())))
                logger.info("...now running pruning algorithm")
                df = prune(df_segm, taglist, low_perc=self.__low_perc, hi_perc=self.__hi_perc)

            logger.info("segmentation and pruning complete in {:.3f}s".format(time.time() - start))
            logger.info("detected {} cycles".format(len(df[self.__cyclefield].unique())))

            dtw = DTWMixin()
            logger.info("start calculating golden cycles for {}".format(cmp))
            start = time.time()
            dct_golden = real_golden_cycle(df, dtw, barycenter_type='dtw_avg')
            logger.info("golden cycle calculation completed in {:.3f}s".format(time.time() - start))

            if generate_diagnostics:
                out_path = Path(self.__out_path, "{}.png".format(cmp))
                logger.info("generating tag plots and saving to {}".format(out_path))
                start = time.time()
                PlotUtils.multicycle_plot(df, taglist, sample_ratio=0.01, dct_golden=dct_golden, out_path=out_path)
                logger.info("tag plots generation completed in {:.3f}s".format(time.time() - start))

            GoldenCycleHelper.save_golden(dct_golden, cmp, dst_path=self.__out_path)
            logger.info("====done processing {} in {:.3f}s".format(cmp, time.time() - cmp_start))

        logger.info("====done processing all components in {:.3f}s".format(time.time() - global_start))

    @staticmethod
    def segment_two_edges(df, tag_col, time_col, value_col, cycle_col, sqn_tag, sqn_start_val, sqn_end_val,
                          order_columns=True):
        try:
            df.drop(["svalue", "status", "flags"], axis=1, inplace=True)
        except:
            pass

        df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
        df.dropna(inplace=True)
        df[time_col] = pd.to_datetime(df[time_col])

        if order_columns == True:
            df.sort_values(by=[time_col], inplace=True)

        df = df.reset_index(drop=True)

        df_sqn = df[df[tag_col] == sqn_tag]
        times_start = df_sqn[df_sqn[value_col] == sqn_start_val][time_col].values
        times_end = df_sqn[df_sqn[value_col] == sqn_end_val][time_col].values

        df[cycle_col] = np.nan
        for i, tms in enumerate(tqdm(times_start)):
            times_tmp = times_end[times_end > tms]
            if len(times_tmp) == 0:
                break
            tme = times_tmp[0]
            cycle_index = df[(df[time_col] >= tms) & (df[time_col] <= tme)].index
            vals = np.empty(len(cycle_index))
            vals.fill(i)
            df.loc[cycle_index, (cycle_col)] = vals

        df = df[df[cycle_col].notna()]
        return df

    @staticmethod
    def segment_two_edges_enh(df, tag_col, time_col, value_col, cycle_col, sqn_tag, sqn_start_val, sqn_end_val,
                              sqn_after_val, order_columns=True):
        try:
            df.drop(["svalue", "status", "flags"], axis=1, inplace=True)
        except:
            pass

        df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
        df.dropna(inplace=True)
        df[time_col] = pd.to_datetime(df[time_col])

        if order_columns == True:
            df.sort_values(by=[time_col], inplace=True)

        df = df.reset_index(drop=True)

        df_sqn = df[df[tag_col] == sqn_tag]
        times_start = df_sqn[df_sqn[value_col] == sqn_start_val][time_col].values
        times_end = df_sqn[df_sqn[value_col] == sqn_end_val][time_col].values

        df[cycle_col] = np.nan
        for i, tms in enumerate(tqdm(times_start)):
            times_tmp = times_end[times_end > tms]
            if len(times_tmp) == 0:
                break
            tme = times_tmp[0]

            # find first sqn_after_val after tme
            df_tmp = df_sqn[(df_sqn[time_col] >= tme) & (df_sqn[value_col] == sqn_after_val)]
            if len(df_tmp) == 0:
                logger.warning("no {} after {} was found".format(sqn_after_val, tme))
                continue

            tma = df_tmp[time_col].values[0]
            cycle_index = df[(df[time_col] >= tms) & (df[time_col] <= tma)].index
            vals = np.empty(len(cycle_index))
            vals.fill(i)
            df.loc[cycle_index, (cycle_col)] = vals

        df = df[df[cycle_col].notna()]
        return df

    @staticmethod
    def segment_and_prune(df, taglist, segmenting_rule_fn, valuefield='value', low_perc=0.25, hi_perc=0.75):
        df_segm = segmentation(df, segmenting_rule_fn, signal_col=valuefield, order_columns=True)
        df_clean = prune(df_segm, taglist, low_perc=low_perc, hi_perc=hi_perc)
        return df_clean

    @staticmethod
    def save_golden(dct_golden, cmp_name, dst_path="."):
        fname = "{}_golden.json".format(cmp_name)
        dst_file_path = Path(dst_path, fname)
        with open(dst_file_path, 'w') as fp:
            json.dump(dct_golden, fp, indent=4)
        logger.info("saved golden cycles to {}".format(str(dst_file_path)))
