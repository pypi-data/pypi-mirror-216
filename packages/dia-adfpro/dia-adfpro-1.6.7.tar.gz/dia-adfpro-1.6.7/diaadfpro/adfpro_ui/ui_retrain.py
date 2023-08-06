from dash import html
from dash import dcc
from dash import dash_table
import dash_bootstrap_components as dbc

from diaadfpro.adfpro_ui.constants import ADFPCUI


class UIRetrainTableBuilder():
    def __init__(self,tabdata):
        self.__tabdata = tabdata

    def build(self):
        
               
        email_input = dbc.Row(
                            [
                                dbc.Label("Username", html_for="example-email-row", width=2),
                                dbc.Col(
                                    dbc.Input(
                                        type="text", id="example-username-row", placeholder="Enter username"
                                    ),
                                    width=10,
                                ),
                            ],
                            className="mb-3",
                        )
        
        password_input = dbc.Row(
                                [
                                    dbc.Label("Password", html_for="example-password-row", width=2),
                                    dbc.Col(
                                        dbc.Input(
                                            type="password",
                                            id="example-password-row",
                                            placeholder="Enter password",
                                        ),
                                        width=10,
                                    ),
                                ],
                                className="mb-3",
                            )
        form = dbc.Form([email_input, password_input,dbc.Button("Authorize for retraining", id="auth-retrain"),])
        
        collapse = html.Div(
                            [
                                dbc.Button(
                                    "Retrain",
                                    id="collapse-button",
                                    className="mb-3",
                                    color="primary",
                                    n_clicks=0,
                                ),
                                dbc.Collapse(
                                    dbc.Card([dbc.CardBody("Authorization required to perform retrain action"),
                                                dbc.CardBody("PLEASE NOTE THAT RETRAINING WILL ERASE ALL PREVIOUS CLASSIFICATION HISTORY!"),
                                              dbc.Row([
                                                  dbc.Col([
                                                  form,
                                                  ], width="11"),
                                              ]),
                                              
                                             ]),
                                    id="collapse",
                                    is_open=False,
                                ),
                            ]
                        )
        
        tab = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Div([
                            html.Br(),
                            self.__build_retrain_table(),
                            html.Br(),
                            
                        ]), width=12),
                        
                        
                    ]
                ),
                
                dbc.Row([
                            dbc.Col([
                                    html.H5("Select retrain start date time"),
                                    dcc.Input(
                                        id=ADFPCUI.ID_RET_TIMERANGESTART,
                                        type='datetime-local',
                                    ), ], width="3"
                                ),
                    
                                dbc.Col([
                                    
                                    html.H5("Select retrain end date time"),
                                    
                                    dcc.Input(
                                        id=ADFPCUI.ID_RET_TIMERANGEEND,
                                        type='datetime-local',
                                    ), 
                                
                                ], width="3"),
                    
                                dbc.Col([                                                       
                                        dbc.Progress(value=100, style={"height": "1px"}, className="mb-3"),
                                        collapse,
                                        dbc.Spinner(html.Div(id="loading-output")),
                                                
                                ], width="6"),                        
                ]),

            ], style={"margin-top": "1em", "width": "100%", "border": "solid 0px black"}
        )
        return tab

    def __build_retrain_table(self):
        table = dcc.Loading(id=ADFPCUI.ID_LOADING_TABLE2,
                            children=[
                                html.Div([
                                    dash_table.DataTable(
                                        id=ADFPCUI.ID_TAB_RETRAIN_TABLE,
                                        columns=[{"name": i, "id": i, "selectable": True}
                                                 for i in self.__tabdata.columns],
                                        data=self.__tabdata.to_dict('records'),
                                        fixed_rows={'headers': True},
                                        style_table={'height': 520},
                                        sort_action='native',
                                        editable=True,
                                        filter_action="native",
                                        sort_mode="multi",
                                        row_selectable="multi",
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action="native",
                                        page_current= 0,
                                        page_size= 20,
                                        style_header={
                                            'color': 'black',
                                            'fontWeight': 'bold'
                                        },
                                        
                                    ),  # end of table
                                ])],
                            type=ADFPCUI.LOADIND_TYPE,
                            )
        return table

        
