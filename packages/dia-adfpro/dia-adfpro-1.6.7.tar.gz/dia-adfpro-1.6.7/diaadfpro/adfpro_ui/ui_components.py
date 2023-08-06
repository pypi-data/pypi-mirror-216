"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

import math
import pathlib
import sys
import pathlib

import dash
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output, State, callback_context

sys.path.insert(0, '/repos/MQIT_DIA_ADFPRO')

from diaadfpro.adfpro.configuration import ConfigurationManager
from diaadfpro.adfpro.utils import AnomalySummaryUtils, PlotUtils, ArtifactsIOHelper, IOUtils, ADFPDateUtils, \
    RetrainingUtils, AuthenticationUtils

from diaadfpro.adfpro_ui.constants import ADFPCUI
from diaadfpro.adfpro_ui.ui_anomaly_plots import UIAnomalyPlotsBuilder
from diaadfpro.adfpro_ui.ui_ohlc_plots import OHLCPlotBuilder
from diaadfpro.adfpro_ui.ui_summary_table import UISummaryTableBuilder
from diaadfpro.adfpro_ui.ui_retrain import UIRetrainTableBuilder

from diaadfpro.adfpro.train import Trainer
from diaadfpro.adfpro.model import JobList
import yaml
from keras import backend as K

import tensorflow as tf

import logging.config
tf.get_logger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

class UIBuilder:

    def __init__(self):
        self.__site_name = ConfigurationManager.instance().get_ui_site()
        #print(self.__site_name)
        self.__site_lines = ConfigurationManager.instance().get_ui_lines()
        print(self.__site_lines)
        
        site_obj = ConfigurationManager.instance().get_site(self.__site_name)
        #print(site_obj)
        #print(type(site_obj))
        #print(ConfigurationManager.instance().__site_list)
        
        components = []
        for lname in self.__site_lines:
            components.extend(site_obj.find_component(lname).child_components)

        logger.info("Site: {}".format(self.__site_name))
        logger.info("Lines: {}".format(self.__site_lines))

        self.__mdlist = [ConfigurationManager.instance().get_model_descriptor().type_and_version]
        self.__dbp = ConfigurationManager.instance().get_database_param_dictionary()
        self.__shifts = ConfigurationManager.instance().get_shifts_dictionary()

        self.__equipments, self.__eqpm_ids, self.__dropdown_options, self.__classifier_pkl_paths, self.__feature_dict = \
            AnomalySummaryUtils.get_equipment_list(ConfigurationManager.instance().get_artifacts_folder(),
                                                   ConfigurationManager.instance().get_model_descriptor().type,
                                                   components)

        logger.debug("Equipments - {}".format(str(self.__equipments)))
        logger.debug("Dropdown options = {}".format(self.__dropdown_options))
        
        self.__tabdata_retrain = AnomalySummaryUtils.get_retrain_table(self.__dbp,ConfigurationManager.instance().get_db_password(),self.__equipments)
        
        self.__tabdata, self.__ct, self.__times_dict_report = AnomalySummaryUtils.generate_tabdata(self.__mdlist,
                                                                                                   self.__dbp,
                                                                                                   ConfigurationManager.instance().get_db_password(),
                                                                                                   self.__equipments)
                                        
        self.__smm_tbl_builder = UISummaryTableBuilder(self.__ct, self.__tabdata)
        self.__version = "[report version]"
        self.__plots_builder = UIAnomalyPlotsBuilder(self.__dropdown_options)
        self.__ohlc_plots_builder = OHLCPlotBuilder(self.__dropdown_options)
        self.__themes_list = ["BOOTSTRAP", "CYBORG", "DARKLY", "SLATE", "SOLAR", "SUPERHERO", "CERULEAN", "COSMO",
                              "FLATLY", "JOURNAL", "LITERA", "LUMEN", "LUX", "MATERIA", "MINTY", "PULSE", "SANDSTONE",
                              "SIMPLEX", "SKETCHY", "SPACELAB", "UNITED", "YETI", "DEFAULT", "MORPH", "QUARTZ", "VAPOR",
                              "ZEPHYR", ]
        self.__graph_templates = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
        self.__graph_theme = "plotly_white"
        self.__DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S%z"
        
        # Retrain changes
        self.__retrain_tbl_builder = UIRetrainTableBuilder(self.__tabdata_retrain)

    def get_layout(self):
        layout = html.Div(
            [
                dbc.Row([
                    dbc.Col(
                        html.Div([self.__build_header(), ]), style={"text-align": "center"},
                    ),
                ], style={"margin-top": "2em"}),
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            self.__build_tabs(),
                        ])
                    ),
                ], style={"margin": "auto", "margin-top": "2em", "width": "80%", "border": "solid 0px black"}),
            ]
        )
        return layout

    def __build_header(self):
        hdr = html.Div([
            html.H1(ADFPCUI.LBL_REPORT_DESCRIPTION),
            html.H6("Site: {}, Line: {} ".format(self.__site_name, ', '.join(self.__site_lines))),
            html.H6("non-GMP use - Version: " + ADFPCUI.REPORT_VERSION)
        ])
        return hdr

    def __build_tabs(self):
        tabs = dbc.Tabs(
            id=ADFPCUI.ID_TABS, active_tab=ADFPCUI.ID_TAB_SUMMARY_TABLE, children=[
                dbc.Tab(self.__wrap_in_card(self.__build_tab_summary()), label=ADFPCUI.LBL_TAB_SUMMARY_TABLE,
                        tab_id=ADFPCUI.ID_TAB_SUMMARY_TABLE),
                dbc.Tab(self.__wrap_in_card(self.__build_tab_anomaly_plots()), label=ADFPCUI.LBL_TAB_ANOM_PLOTS,
                        tab_id=ADFPCUI.ID_TAB_PLOTS),
                
                # dbc.Tab(self.__wrap_in_card(self.__build_tab_settings()),
                #         label="Settings",
                #         tab_id=ADFPCUI.ID_TAB_SETTINGS),

                 dbc.Tab(self.__wrap_in_card(self.__build_tab_retrain()),
                        label="Retraining",
                        tab_id=ADFPCUI.ID_TAB_RETRAIN),
                
                dbc.Tab(self.__wrap_in_card(self.__build_tab_ohlc()),
                        label="OHLC",
                        tab_id=ADFPCUI.ID_TAB_MISC),
                
                dbc.Tab(self.__wrap_in_card(self.__build_tab_about()),
                        label="About",
                        tab_id=ADFPCUI.ID_TAB_ABOUT),
                
            ]
        )
        return tabs

    def __wrap_in_card(self, obj):
        tab = dbc.Card(
            dbc.CardBody([
                obj,
            ]), className="mt-3"
        )
        return tab

    def __build_tab_summary(self):
        return self.__smm_tbl_builder.build()

    def __build_tab_anomaly_plots(self):
        return self.__plots_builder.build()

    def __build_tab_about(self):
        tab = html.Div(
            [
                html.H2(
                    "Combining edge and cloud computing for anomaly detection and classification of time series - Sesto R3 usecase"),
                dcc.Markdown('''
                [White Paper](https://collab.lilly.com/:w:/r/sites/mqdiateam/Shared%20Documents/DIA%20Advanced%20Analytics%20Solutions/Anomaly%20detection%20in%20multivariate%20time%20series/Anomaly%20detection%20and%20classification%20of%20time%20series%20-%20Sesto%20R3%20use%20case.docx?d=w5100b056ccb54182af88ec7f29565a66&csf=1&web=1&e=vSApS6 "White paper")
                [Presentation](https://collab.lilly.com/:p:/r/sites/mqdiateam/Shared%20Documents/DIA%20Advanced%20Analytics%20Solutions/Anomaly%20detection%20in%20multivariate%20time%20series/ACME_Anomaly%20detection%20and%20classification%20of%20time%20series%20-%20Sesto%20R3%20use%20case.pptx?d=w0dfc7ab9c055412a9376170eb7ce59f6&csf=1&web=1&e=5P80U1 "ppt")
                '''),
            ]
        )
        return tab

    def __build_tab_retrain(self):
        return self.__retrain_tbl_builder.build()
    
    def __build_tab_ohlc(self):
        return self.__ohlc_plots_builder.build()

    def callback_tab1_refresh(self):
        self.__tabdata, self.__ct, self.__times_dict_report = AnomalySummaryUtils.generate_tabdata(self.__mdlist,
                                                                                                   self.__dbp,
                                                                                                   ConfigurationManager.instance().get_db_password(),
                                                                                                   self.__equipments)
        return self.__tabdata, self.__ct

    def callback_set_graph_theme(self, th):
        self.__graph_theme = th

    def callback_dynamic_changes(self, n1, clickData, n2, start_time, end_time, dv, active_cell, changed_id):
        
        def create_result(res):
            result = {}
            result['TABS'] = res[0]
            result['CELL_SELECTED'] = res[1]
            result['DESC_SITE_LINE'] = res[2]
            result['DESC_EQUIP'] = res[3]
            result['PLOT_ANOMALY'] = res[4]
            result['PLOT_SHAP'] = res[5]
            result['DTP_TIMERANGESTART'] = res[6]
            result['DTP_TIMERANGEEND'] = res[7]
            result['DRP_EQUIPMENT'] = res[8]
            result['LOADING_BOX'] = res[9]
            result['ANOMPLOT_START'] = res[10]
            result['ANOMPLOT_END'] = res[11]
            result['SHAPPLOT_START'] = res[12]
            result['SHAPPLOT_END'] = res[13]
            result['BOXPLOT_START_TRAIN'] = res[14]
            result['BOXPLOT_END_TRAIN'] = res[15]
            result['BOXPLOT_START'] = res[16]
            result['BOXPLOT_END'] = res[17]
            return result

        if changed_id == ADFPCUI.ID_BTN_REFRESHPLOT:  # 'submit-val':
            st_line, eq_detail, fig = PlotUtils.generate_anomaly_graph(start_time, end_time, dv, 'Custom',
                                                                       self.__graph_theme, self.__DATETIME_FORMAT,
                                                                       self.__dbp, ConfigurationManager.instance().get_db_password(),
                                                                       self.__eqpm_ids[dv],self.__site_name,self.__site_lines)

            sfig = PlotUtils.get_empty_graph("shap_empty")
            bfig = PlotUtils.get_empty_graph("box_empty")
            
            res = [dash.no_update, '', st_line, eq_detail, fig, sfig, dash.no_update, dash.no_update, dash.no_update, bfig, ADFPCUI.LBL_START + start_time, ADFPCUI.LBL_END + end_time, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]

            result = create_result(res)
            return result

        assert self.__feature_dict, "Feature dict object is empty."

        if changed_id == ADFPCUI.ID_PLOT_ANOMALY:  # 'anomaly-graph':
            # read pkl from s3 and then pass dictionary to "generate_shap_plot" and "generate_box_plot"
            K.clear_session()
            pkl_dct = self.__read_pkl_from_s3(self.__classifier_pkl_paths[dv])
            
           

            shap_plot, start_train, end_train, sd_ph, ed_ph = PlotUtils.generate_shap_plot(dv, clickData,
                                                                                           self.__graph_theme,
                                                                                           pkl_dct,
                                                                                           self.__dbp,
                                                                                           ConfigurationManager.instance().get_db_password(),
                                                                                           self.__feature_dict)
            box_plot = PlotUtils.generate_box_plot(dv, clickData, pkl_dct, self.__dbp,
                                                   ConfigurationManager.instance().get_db_password(),
                                                   self.__feature_dict)
            res = [dash.no_update, '', dash.no_update, dash.no_update, dash.no_update, shap_plot, dash.no_update, dash.no_update, dash.no_update, box_plot, ADFPCUI.LBL_START + start_time, ADFPCUI.LBL_END + end_time, ADFPCUI.LBL_START + str(
                sd_ph), ADFPCUI.LBL_END + str(ed_ph), ADFPCUI.LBL_TRAIN_START + str(
                start_train), ADFPCUI.LBL_TRAIN_END + str(end_train), ADFPCUI.LBL_START + str(
                sd_ph), ADFPCUI.LBL_END + str(ed_ph)]
            
            result = create_result(res)
            return result

        if changed_id == ADFPCUI.ID_INSPECT:

            if active_cell:
                row = active_cell['row']
                row_id = active_cell['row_id']
                col_name = active_cell['column_id']
                equip_name = self.__tabdata.iloc[int(row_id) - 1][ADFPCUI.LBL_ST_TBLHDR_COMPNAME]

                time_range = ""

                if col_name in ['id', ADFPCUI.LBL_ST_TBLHDR_COMPNAME]:
                    col_name = 'Last_24hr'

                if math.isnan(self.__tabdata.iloc[int(row_id) - 1][col_name]):
                    data = "No data for selected cell"
                    res = [dash.no_update, data, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]
                    
                    result = create_result(res)
                    return result
                    
                else:
                    start_time = self.__times_dict_report[col_name + "_start"]
                    end_time = self.__times_dict_report[col_name + "_end"]
                    stt = str(start_time)
                    ett = str(end_time)
                    st_line, eq_detail, fig = PlotUtils.generate_anomaly_graph(start_time, end_time, equip_name,
                                                                               col_name, self.__graph_theme,
                                                                               self.__DATETIME_FORMAT, self.__dbp,
                                                                               ConfigurationManager.instance().get_db_password(),
                                                                               self.__eqpm_ids[equip_name],self.__site_name,self.__site_lines)
                    sfig = PlotUtils.get_empty_graph("shap_empty")
                    bfig = PlotUtils.get_empty_graph("box_empty")
                    res = [ADFPCUI.ID_TAB_PLOTS, '', st_line, eq_detail, fig, sfig, stt, ett, equip_name, bfig, ADFPCUI.LBL_START + start_time, ADFPCUI.LBL_END + end_time, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]
                    
                    result = create_result(res)
                    return result
            else:
                data = "No cell selected"
                res =[dash.no_update, data, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update]
                result = create_result(res)
                return result

    def callback_misc_dynamic_dropdown(self, dv, n, st, cid, sd, ed, tf):
        if cid == "misc_eq":
            ll = self.__feature_dict[dv]
            op = []
            for k in ll:
                d = {}
                d['label'] = k
                d['value'] = k
                op.append(d) 

            fig = PlotUtils.get_empty_graph('anomaly_msg')
            return op, fig

        if cid == "misc_click":
            fig = PlotUtils.get_ohlc_graph(self.__dbp, ConfigurationManager.instance().get_db_password(), st, sd, ed, tf)
            return dash.no_update, fig

    def __read_pkl_from_s3(self, local_pkl_path: str):
        artifacts_helper = ArtifactsIOHelper(ConfigurationManager.instance().get_artifacts_folder(),
                                             ConfigurationManager.instance().get_s3_artifacts_folder(),
                                             ConfigurationManager.instance().get_aws_param_dictionary())
        artifacts_helper.reset_s3_client()
        pkl_filename = pathlib.Path(local_pkl_path).name

        logger.info("Downloading file {} from s3 to {}".format(pkl_filename, local_pkl_path))
        # download pkl file that stores model from S3 to local folder
        artifacts_helper.read_from_s3(pkl_filename, local_pkl_path)
        # load model from pkl file
        pkl_data = IOUtils.read_pkl_direct(local_pkl_path)

        return pkl_data

    def retrain_components(self, srt, ert, selected_row, uname):
        # Generate YML
        component_list = []
        component_id = []
        start_retrain_date_object = ADFPDateUtils.utc_set(srt)
        end_retrain_date_object = ADFPDateUtils.utc_set(ert)
        
        for row_id in selected_row:
            component_list.append(self.__tabdata_retrain.iloc[row_id]['Component'])
            component_id.append(self.__tabdata_retrain.iloc[row_id]['eqpm_id'])
            
        logger.info("Components selected {} , {} , {}".format(str(component_list),start_retrain_date_object,end_retrain_date_object))
        
        master_cfg_path, jobs_list_path = RetrainingUtils.initiate_retraining(srt, ert, component_list,self.__site_name)
        
        # Initiate Retrain by reading yml
        logger.info("Creating Trainer...")
        trn = Trainer.build(ConfigurationManager.instance().get_model_descriptor(),
                        ConfigurationManager.instance().get_explainer_descriptor(),
                        ConfigurationManager.instance().get_database_param_dictionary(),
                        ConfigurationManager.instance().get_db_password(),
                        ConfigurationManager.instance().get_artifacts_folder()
                        )
        logger.info("...trainer created")
        
        jobs_list_path = ADFPCUI.RETRAIN_YML
        job_list = JobList(pathlib.Path(jobs_list_path).resolve())
        logger.info("Job list is {}".format(job_list))
        
        logger.info("Retrieving site from job list...")
        site = ConfigurationManager.instance().get_site(job_list.get_site())
        logger.info("...done retrieving site {}".format(site.name))
        
        logger.info("Executing training...")
        trn.execute_train_job(job_list, site)
        logger.info("..done executing training")
        
        # Fetch uid using uname
        user_id = IOUtils.fetch_user_id(uname, self.__dbp, ConfigurationManager.instance().get_db_password())
        
        current_ts = ADFPDateUtils.get_current_dt()
        IOUtils.update_adpro_users(self.__dbp, ConfigurationManager.instance().get_db_password(), current_ts, user_id)
        
        logger.info("..done updating tables after retraining")
        
        # Refresh table retraining
        updated_retrain_table = AnomalySummaryUtils.get_retrain_table(self.__dbp,ConfigurationManager.instance().get_db_password(),self.__equipments)
        
        return updated_retrain_table

    def validate_user(self, uname, pwd):
        # returns True or false
        status = AuthenticationUtils.authenticate(uname, pwd, self.__dbp, ConfigurationManager.instance().get_db_password())
        return status
    
    def get_user_id(self, uname):
        user_id = IOUtils.fetch_user_id(uname, self.__dbp, ConfigurationManager.instance().get_db_password())
        return user_id
