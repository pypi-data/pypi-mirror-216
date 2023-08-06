"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""
import getopt
import logging.config
import os
import pathlib
import sys
import json

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State, callback_context
from packaging import version

sys.path.insert(0, '/repos/MQIT_DIA_ADFPRO')

from diaadfpro.adfpro_ui.ui_components import UIBuilder
from diaadfpro.adfpro.configuration import ConfigurationManager

logger = logging.getLogger(__name__)

DASH_VER = dcc.__version__
assert (version.parse(DASH_VER) >= version.parse("1.0.0"))

external_stylesheets = [dbc.themes.MATERIA]


def is_domino():
    isd = True
    try:
        os.environ["DOMINO_USER_HOST"]
    except KeyError as e:
        isd = False
    return isd


def parse_options(argv):
    options, remainder = getopt.getopt(argv, 'e:l:', ['env-config=', 'log-config='])
    logger.info("Options: {}".format(options))
    env_file_path = ""
    log_file_path = ""

    for opt, arg in options:
        if opt in ('-e', '--env-config'):
            env_file_path = arg
        if opt in ('-l', '--log-config'):
            log_file_path = arg
    return [env_file_path, log_file_path]


def get_assets_path():
    assets_path = "/"
    if is_domino():
        assets_path = 'https://domino.am.lilly.com/' + os.environ.get("DOMINO_PROJECT_OWNER") + '/' + os.environ.get(
            "DOMINO_PROJECT_NAME") + '/r/notebookSession/' + os.environ.get("DOMINO_RUN_ID") + '/assets/'
    return assets_path


def create_app():
    app = Dash(__name__, external_stylesheets=external_stylesheets, assets_external_path=get_assets_path(),
               routes_pathname_prefix='/',
               requests_pathname_prefix='/{}/{}/r/notebookSession/{}/'.format(
        os.environ.get("DOMINO_PROJECT_OWNER"),
        os.environ.get("DOMINO_PROJECT_NAME"),
        os.environ.get("DOMINO_RUN_ID")))
    del app.config._read_only["requests_pathname_prefix"]

    #auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

    # if is_domino():
    # app.config.update({
    #     'routes_pathname_prefix': '',
    #     'requests_pathname_prefix': '/{}/{}/r/notebookSession/{}/'.format(
    #         os.environ.get("DOMINO_PROJECT_OWNER"),
    #         os.environ.get("DOMINO_PROJECT_NAME"),
    #         os.environ.get("DOMINO_RUN_ID"))
    # })

    ui_builder = UIBuilder()

    app.layout = ui_builder.get_layout()
    return app, ui_builder


def run_dash_server():
    app, ui_builder = create_app()
    setup_callbacks(app, ui_builder)

    if is_domino():
        if ConfigurationManager.instance().get_ui_debug():
            app.run_server(host=ConfigurationManager.instance().get_ui_host(),
                           port=ConfigurationManager.instance().get_ui_port(),
                           debug=ConfigurationManager.instance().get_ui_debug(),
                           dev_tools_props_check=False)
        else:
            app.run_server(host=ConfigurationManager.instance().get_ui_host(),
                           port=ConfigurationManager.instance().get_ui_port(),
                           debug=ConfigurationManager.instance().get_ui_debug())
    else:
        app.run_server(debug=ConfigurationManager.instance().get_ui_debug(),
                       port=ConfigurationManager.instance().get_ui_port())


def setup_callbacks(app, ui_builder):
    from diaadfpro.adfpro_ui.constants import ADFPCUI

    # 1. Refresh report callback (tab1)   prevent_initial_call=True
    @app.callback(
        Output(ADFPCUI.ID_LATESTFETCH, 'children'),
        Output(ADFPCUI.ID_TAB_SUMMARY_TABLE, 'data'),
        Input(ADFPCUI.ID_REFRESH, 'n_clicks'),
    )
    def callback_a(n):
        logger.info("1. Callback triggered..")
        tabdata, ct = ui_builder.callback_tab1_refresh()
        logger.info("1.a Callback triggered")
        data = tabdata.to_dict('records')
        fetchtime = "Last updated: " + ct.strftime('%Y-%m-%d %H:%M:%S %Z')
        return fetchtime, data

    # # 2. Theme selector callback (Settings tab4)
    # app.clientside_callback(
    #     """
    #     function(theme) {
    #         var stylesheet = document.querySelector('link[rel=stylesheet][href^="https://stackpath"]')
    #         var name = theme.toLowerCase()
    #         if (name === 'bootstrap') {
    #             var link = 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css'
    #           } else {
    #             var link = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/" + name + "/bootstrap.min.css"
    #         }
    #         stylesheet.href = link
    #     }
    #     """,
    #     Output("blank_output", "children"),
    #     Input(ADFPCUI.ID_THEME, "value"),
    # )

    # 3. callback Generate Anomaly graph, shap, switching tab (tab1 and tab2)
    @app.callback(
        Output(ADFPCUI.ID_TABS, 'active_tab'),
        Output(ADFPCUI.ID_NO_CELL_SELECTED, 'children'),
        Output(ADFPCUI.ID_DESC_SITE_LINE, 'children'),
        Output(ADFPCUI.ID_DESC_EQUIP, 'children'),

        Output(ADFPCUI.ID_PLOT_ANOMALY, 'figure'),
        Output(ADFPCUI.ID_PLOT_SHAP, 'figure'),
        Output(ADFPCUI.ID_DTP_TIMERANGESTART, 'value'),
        Output(ADFPCUI.ID_DTP_TIMERANGEEND, 'value'),
        Output(ADFPCUI.ID_DRP_EQUIPMENT, 'value'),
        Output(ADFPCUI.ID_LOADING_BOX, 'children'),

        Output(ADFPCUI.ID_ANOMPLOT_START, 'children'),
        Output(ADFPCUI.ID_ANOMPLOT_END, 'children'),
        Output(ADFPCUI.ID_SHAPPLOT_START, 'children'),
        Output(ADFPCUI.ID_SHAPPLOT_END, 'children'),
        Output(ADFPCUI.ID_BOXPLOT_START_TRAIN, 'children'),
        Output(ADFPCUI.ID_BOXPLOT_END_TRAIN, 'children'),
        Output(ADFPCUI.ID_BOXPLOT_START, 'children'),
        Output(ADFPCUI.ID_BOXPLOT_END, 'children'),

        Input(ADFPCUI.ID_BTN_REFRESHPLOT, 'n_clicks'),
        Input(ADFPCUI.ID_PLOT_ANOMALY, 'clickData'),
        Input(ADFPCUI.ID_INSPECT, 'n_clicks'),
        State(ADFPCUI.ID_DTP_TIMERANGESTART, 'value'),
        State(ADFPCUI.ID_DTP_TIMERANGEEND, 'value'),
        State(ADFPCUI.ID_DRP_EQUIPMENT, 'value'),
        State(ADFPCUI.ID_TAB_SUMMARY_TABLE, 'active_cell'),
        prevent_initial_call=True
    )
    def callback_datetest(n1, clickData, n2, start_time, end_time, dv, active_cell):
        ctx = callback_context
        changed_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # out_1, out_2, out_3, out_4, out_5, out_6, out_7, out_8, out_9, out_10, out_11, out_12, out_13, out_14, out_15, out_16, out_17, out_18 = ui_builder.callback_dynamic_changes(
        #   n1, clickData, n2, start_time, end_time, dv, active_cell, changed_id)

        result = ui_builder.callback_dynamic_changes(
            n1, clickData, n2, start_time, end_time, dv, active_cell, changed_id)

        # return out_1, out_2, out_3, out_4, out_5, out_6, out_7, out_8, out_9, out_10, out_11, out_12, out_13, out_14, out_15, out_16, out_17, out_18
        return result['TABS'], result['CELL_SELECTED'], result['DESC_SITE_LINE'], result['DESC_EQUIP'], result['PLOT_ANOMALY'], result['PLOT_SHAP'], result['DTP_TIMERANGESTART'], result['DTP_TIMERANGEEND'], result['DRP_EQUIPMENT'], result['LOADING_BOX'], result['ANOMPLOT_START'], result['ANOMPLOT_END'], result['SHAPPLOT_START'], result['SHAPPLOT_END'], result['BOXPLOT_START_TRAIN'], result['BOXPLOT_END_TRAIN'], result['BOXPLOT_START'], result['BOXPLOT_END']

    # # 4. Graph theme setter (Settings tab4)
    # @app.callback(
    #     Output('gt', 'children'),
    #     Input(ADFPCUI.ID_GRAPH_THEME, 'value'),
    #     prevent_initial_call=True
    # )
    # def callback_graph_themeselector(th):
    #     ui_builder.callback_set_graph_theme(th)
    #     gst = "Graph Theme selected : " + th
    #     return gst

    # MISC

    @app.callback(
        Output('misc_tag', 'options'),
        Output('misc_ohlc_graph', 'figure'),
        Input('misc_eq', 'value'),
        Input('misc_click', 'n_clicks'),
        State('misc_tag', 'value'),
        State('misc_sd', 'value'),
        State('misc_ed', 'value'),
        State('misc_tf', 'value'),
        prevent_initial_call=True
    )
    def callback_dynamic_dropdown(dv, n, st, sd, ed, tf):
        ctx = dash.callback_context
        cid = ctx.triggered[0]['prop_id'].split('.')[0]

        out1, out2 = ui_builder.callback_misc_dynamic_dropdown(
            dv, n, st, cid, sd, ed, tf)
        return out1, out2


    @app.callback(
        Output("loading-output", "children"),
        Output(ADFPCUI.ID_TAB_RETRAIN_TABLE, 'data'),
        [Input("auth-retrain", "n_clicks")],
        [State("example-username-row", "value"),
         State("example-password-row", "value"),
         State(ADFPCUI.ID_RET_TIMERANGESTART, 'value'),
         State(ADFPCUI.ID_RET_TIMERANGEEND, 'value'),
         State(ADFPCUI.ID_TAB_RETRAIN_TABLE, 'selected_rows'),
        ],
        prevent_initial_call=True
    )
    def toggle_collapse_retrain(n, uname, pwd, retrain_start_time, retrain_end_time, selected_rows):
        logger.info(uname)
        uname = uname.lower()
        authentication = False
        authentication = ui_builder.validate_user(uname, pwd)

        if authentication == True:
            ConfigurationManager.instance().set_current_user(uname)
            ConfigurationManager.instance().set_current_user_id(ui_builder.get_user_id(uname))
            
            updated_retrain_table = ui_builder.retrain_components(retrain_start_time, retrain_end_time, selected_rows, uname)
            updated_retrain_table = updated_retrain_table.to_dict('records')
            return "Successfully trained .(for click {})".format(n), updated_retrain_table
        else:
            return "Authentication failed", dash.no_update


    @app.callback(
        Output("collapse", "is_open"),
        [Input("collapse-button", "n_clicks")],
        [State("collapse", "is_open")],
        prevent_initial_call=True
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    

def main(argv):
    if len(argv) < 3:
        logger.error("Not enough input arguments")
        sys.exit("Not enough input arguments")

    [mastercfg_file_path, logcfg_file_path] = parse_options(argv)

    if pathlib.Path(mastercfg_file_path).is_file():
        logger.warning("Using master configuration file at {}".format(mastercfg_file_path))
    else:
        logger.error("{} does not seem to be a valid master configuration file...".format(mastercfg_file_path))
        logger.error("Application will exit immediately")
        sys.exit("Invalid master configuration file")

    if pathlib.Path(logcfg_file_path).is_file():
        logger.warning("Using log configuration file at {}".format(logcfg_file_path))
        logging.config.fileConfig(logcfg_file_path, disable_existing_loggers=False)
    else:
        logger.error("{} does not seem to be a valid log configuration file...".format(logcfg_file_path))
        logger.error("Application will exit immediately")
        sys.exit("Invalid log configuration file")

    ConfigurationManager.initialize(
        pathlib.Path(mastercfg_file_path).resolve())

    run_dash_server()


if __name__ == '__main__':
    main(sys.argv[1:])
