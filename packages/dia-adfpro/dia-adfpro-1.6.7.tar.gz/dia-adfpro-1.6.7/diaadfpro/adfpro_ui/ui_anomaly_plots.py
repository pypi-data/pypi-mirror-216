"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

from datetime import datetime, timedelta

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from diaadfpro.adfpro.utils import PlotUtils
from diaadfpro.adfpro_ui.constants import ADFPCUI


class UIAnomalyPlotsBuilder():

    def __init__(self, dropdown_options):
        self.__equipment_list = dropdown_options
        self.__sd = datetime.strftime(datetime.utcnow() - timedelta(days=1), '%Y-%m-%dT%H:%M')
        self.__ed = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M')

    def build(self):
        cnt = html.Div([
            html.Div(
                self.__build_filters()
            ),
            html.Div(
                self.__build_plots_pane()
            )
        ], style={"margin-top": "1em", "width": "100%", "border": "solid 0px black"})

        return cnt

    def __build_filters(self):
        cnt = dbc.Row([
            dbc.Col([
                html.H5("Select equipment"),
                dcc.Dropdown(
                    id=ADFPCUI.ID_DRP_EQUIPMENT,
                    options=self.__equipment_list,
                    value=self.__equipment_list[0]["value"],
                ), ], width="3"
            ),
            dbc.Col([
                html.H5("Select start date"),
                dcc.Input(
                    id=ADFPCUI.ID_DTP_TIMERANGESTART,
                    type='datetime-local',
                    value=self.__sd,
                ), ], width="3"
            ),
            dbc.Col([
                html.H5("Select end date"),
                dcc.Input(
                    id=ADFPCUI.ID_DTP_TIMERANGEEND,
                    type='datetime-local',
                    value=self.__ed,
                ), ], width="3"
            ),
            dbc.Col([
                html.H5(""),
                dbc.Button(ADFPCUI.BTN_AP_REFRESHPLOT, id=ADFPCUI.ID_BTN_REFRESHPLOT,
                           className="btn btn-primary btn-lg"), ], width="3"
            )
        ])
        return cnt

    def __build_plots_pane(self):
        cnt = html.Div([
            self.__build_anomaly_plot_pane(),
            self.__build_shap_plot_pane(),
            self.__build_box_plot_pane()
        ], style={"margin-left": "1em"})
        return cnt

    def __build_anomaly_plot_pane(self):
        cnt = html.Div([
            dbc.Row([
                html.H5(ADFPCUI.LBL_AP_PLOT_ANOMALYTRENDS),
            ]),
            dbc.Row([
                dbc.Col(self.__build_anomaly_graph(), style={"border": "solid 1px black", "text-align": "center"},
                        width=10),

                self.__build_anomaly_graph_details(),
            ]),
        ], style={"margin-top": "1em"})
        return cnt

    def __build_anomaly_graph(self):
        anomaly_plot = html.Div([dcc.Loading(
            id=ADFPCUI.ID_LOADING_ANOMALY,
            children=[html.Div([
                dcc.Graph(
                    id=ADFPCUI.ID_PLOT_ANOMALY,
                    figure=PlotUtils.get_empty_graph('anomaly_empty'),
                )
            ])],
            type=ADFPCUI.LOADIND_TYPE,
        )

        ])
        return anomaly_plot

    def __build_anomaly_graph_details(self):
        plot_details = dbc.Col([
            html.P(ADFPCUI.LBL_AP_START, id=ADFPCUI.ID_ANOMPLOT_START),
            html.P(ADFPCUI.LBL_AP_END, id=ADFPCUI.ID_ANOMPLOT_END),
            html.P("", id=ADFPCUI.ID_DESC_SITE_LINE),
            html.P("", id=ADFPCUI.ID_DESC_EQUIP),
        ])
        return plot_details

    def __build_shap_plot_pane(self):
        cnt = html.Div([
            dbc.Row([
                html.H5(ADFPCUI.LBL_AP_PLOT_ROOTCAUSE),
            ]),
            dbc.Row([
                dbc.Col(
                    self.__build_shap_plot(), style={"border": "solid 1px black", "text-align": "center"}, width=10
                ),
                dbc.Col([
                    html.P(ADFPCUI.LBL_AP_START, id=ADFPCUI.ID_SHAPPLOT_START),
                    html.P(ADFPCUI.LBL_AP_END, id=ADFPCUI.ID_SHAPPLOT_END),
                ])
            ]),
        ], style={"margin-top": "1em"})
        return cnt

    def __build_shap_plot(self):
        shap_plot = html.Div([
            dcc.Loading(
                id=ADFPCUI.ID_LOADING_SHAP,
                children=[html.Div([

                    dcc.Graph(
                        id=ADFPCUI.ID_PLOT_SHAP,
                        figure=PlotUtils.get_empty_graph("shap_empty"),
                    )

                ])],
                type=ADFPCUI.LOADIND_TYPE,
            )
        ])
        return shap_plot

    def __build_box_plot_pane(self):
        cnt = html.Div([
            dbc.Row([
                html.H5(ADFPCUI.LBL_AP_PLOT_BOXPLOT),
            ]),
            dbc.Row([
                dbc.Col(
                    self.__build_box_plot(), style={"border": "solid 1px black", "text-align": "center"}, width=10
                ),
                dbc.Col([
                    html.P(ADFPCUI.LBL_AP_START_TRAIN, id=ADFPCUI.ID_BOXPLOT_START_TRAIN),
                    html.P(ADFPCUI.LBL_AP_END_TRAIN, id=ADFPCUI.ID_BOXPLOT_END_TRAIN),
                    html.P(ADFPCUI.LBL_AP_START, id=ADFPCUI.ID_BOXPLOT_START),
                    html.P(ADFPCUI.LBL_AP_END, id=ADFPCUI.ID_BOXPLOT_END),
                ])
            ])
        ], style={"margin-top": "1em"})
        return cnt

    def __build_box_plot(self):
        box_plot = html.Div([
            dcc.Loading(
                id=ADFPCUI.ID_LOADING_BOX,
                children=[html.Div([
                    PlotUtils.get_empty_graph("box_empty"),
                ])],
                type=ADFPCUI.LOADIND_TYPE,
            )
        ])
        return box_plot
