"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

from datetime import datetime, timedelta
import pandas as pd

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from diaadfpro.adfpro.utils import PlotUtils
from diaadfpro.adfpro_ui.constants import ADFPCUI


class OHLCPlotBuilder():

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
                    id="misc_eq",
                    options=self.__equipment_list,
                    value=self.__equipment_list[0]["value"],
                ),
                html.H5("Select tag"),
                dcc.Dropdown(
                    id="misc_tag",
                    options=[{"label": "No Eq", "value": "Select Equipment"}, ],
                    value="Select Equipment",
                ),

            ], width="3"
            ),
            dbc.Col([
                html.H5("Select start date"),
                dcc.Input(
                    id="misc_sd",
                    type='datetime-local',
                    value=self.__sd,
                ),
                html.H5("Select end date"),
                dcc.Input(
                    id="misc_ed",
                    type='datetime-local',
                    value=self.__ed,
                ),

            ], width="3"
            ),
            dbc.Col([
                html.H5("Select Timeframe"),
                dbc.Input(id="misc_tf", type="number", min=1, max=72, step=1, value=4),

            ], width="3"
            ),
            dbc.Col([
                html.H5(""),
                dbc.Button("Generate Plot..", id="misc_click", className="btn btn-primary btn-lg"), ], width="3"
            )
        ])
        return cnt

    def __build_plots_pane(self):
        cnt = html.Div([
            self.__build_ohlc_plot_pane(),
        ], style={"margin-left": "1em"})
        return cnt

    def __build_ohlc_plot_pane(self):
        cnt = html.Div([
            dbc.Row([
                html.H5("OHLC representation of above tag"),
            ]),
            dbc.Row([
                dbc.Col(self.__build_ohlc_graph(), style={"border": "solid 1px black", "text-align": "center"},
                        width=10),

            ]),
        ], style={"margin-top": "1em"})
        return cnt

    def __build_ohlc_graph(self):
        ohlc_plot = html.Div([dcc.Loading(
            id="misc_loading",
            children=[html.Div([
                dcc.Graph(
                    id="misc_ohlc_graph",
                    figure=PlotUtils.get_empty_graph('anomaly_msg'),
                )
            ])],
            type=ADFPCUI.LOADIND_TYPE,
        )

        ])
        return ohlc_plot
