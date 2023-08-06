"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

import logging
import pandas as pd
from aimltools.ts.preprocessing import DataPreparation

logger = logging.getLogger(__name__)


class SHAPExplainer():
    def __init__(self, feat_names, shap_explainer, data_scaler):
        self.__feat_names = feat_names
        self.__shap_explainer = shap_explainer
        self.__data_scaler = data_scaler

    def mean_shap_values(self, df):
        dp = DataPreparation()
        df_ft = dp.get_feature_matrix(df, self.__feat_names)
        arr_ft_norm = self.__data_scaler.transform(dp.fill_na(df_ft))

        d = {}
        for i, colname in enumerate(df_ft.columns):
            d[colname] = arr_ft_norm[:, i]

        df_ft_norm = pd.DataFrame.from_dict(d)
        df_ft_norm = df_ft_norm.iloc[0:2, :]

        shap_values = self.__shap_explainer.shap_values(df_ft_norm)

        d = {}
        for i in range(len(shap_values[0])):
            d[self.__feat_names[i]] = shap_values[:, i]

        shap_values_df = pd.DataFrame.from_dict(d)
        return shap_values_df.mean(axis=0)
