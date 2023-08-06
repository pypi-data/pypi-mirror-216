"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""

class ADFPCUI:
    REPORT_VERSION = "1.6.7 (2023-06-30)"

    #use for html id's
    ID_REFRESH = "btn-refresh"                                       #Refresh tab1
    ID_LATESTFETCH = "lbl-latestfetch"                               # latestfetch tab1
    ID_SUMMARY_TBL_CONTAINER = "div-summary-tbl-container"
    
    RETRAIN_YML = "/mnt/py/cfg.jobs/temp_retrain_job.yml"

    ID_TABS = "id-tabs"
    ID_TAB_SUMMARY_TABLE = "id-tab-smm-tbl"                          # table tab1
    ID_TAB_PLOTS = "id-tab-plots"
    ID_TAB_ABOUT = "id-tab-about"
    ID_TAB_SETTINGS = "id-tab-settings"
    ID_TAB_MISC = "id-tab-misc"
    ID_TAB_RETRAIN = "id-tab-retrain"
    
    ID_RET_TIMERANGESTART = "id-retrain-start-time"
    ID_RET_TIMERANGEEND = "id-retrain-end-time"
    ID_TAB_RETRAIN_TABLE = "id-retrain_table-selector"
    ID_BTN_RETRAIN = "id-btn-retrain"
    

    ID_DRP_EQUIPMENT = "id-drp-equipment"
    ID_DTP_TIMERANGESTART = "id-dtp-timerangestart"
    ID_DTP_TIMERANGEEND = "id-dtp-timerangeend"
    ID_BTN_REFRESHPLOT = "id-btn-refresh-plots"
    ID_ANOMPLOT_START = "id-anomplot-start"
    ID_ANOMPLOT_END = "id-anomplot-end"
    ID_SHAPPLOT_START = "id-shapplot-start"
    ID_SHAPPLOT_END = "id-shapplot-end"
    ID_BOXPLOT_START_TRAIN = "id-boxplot-start-train"
    ID_BOXPLOT_END_TRAIN = "id-boxplot-end-train"
    ID_BOXPLOT_START = "id-boxplot-start"
    ID_BOXPLOT_END = "id-boxplot-end"

    ID_LOADING_TABLE = "id-loading_table"
    ID_LOADING_TABLE2 = "id-loading_table2"
    ID_LOADING_STATUS = "id-loading-status"
    ID_INSPECT = "id-switch"                                           #tab1
    ID_NO_CELL_SELECTED = "id-no-cell_select"

    ID_DESC_SITE_LINE = "id-site-line"
    ID_DESC_EQUIP = "id-eqip-detail"
    ID_DESC_DATES = "id-testdates"
    ID_DESC_SECS = "id-w-sec"
    ID_DESC_GRAPH_DISPLAYED = "id-graphs-displayed"

    ID_PLOT_ANOMALY = "id-anomaly-graph"
    ID_PLOT_SHAP = "id-shap-graph"
    ID_PLOT_BOX = "id-box-graph"

    ID_LOADING_ANOMALY = "id-loading-anomaly"
    ID_LOADING_SHAP = "id-loading-shap"
    ID_LOADING_BOX = "id-loading-box"
    ID_LOADING_RETRAIN_STATUS = "id-loading-retrain-status"
    

    ID_RESET_THEME = "id-reset"
    ID_THEME = "id-themes"
    ID_GRAPH_THEME = "id-graphthemes"

    #use for html components
    #overall
    LBL_REPORT_DESCRIPTION = "Anomaly Detection and Classification Dashboards"

    #summary table
    LBL_TAB_SUMMARY_TABLE = "Equipment Status Report"
    LBL_ST_TBL_TITLE = "Mean anomaly scores for each component"
    LBL_ST_LATEST_REFRESH = "Latest refresh: "
    LBL_ST_TBLHDR_COMPNAME = "Equipment"
    LBL_ST_TBLHDR_COMPID = "Id"
    LBL_ST_TBLHDR_LAST4H = "Last 4h"
    LBL_ST_TBLHDR_LASTSHIFT = "Last shift"
    LBL_ST_TBLHDR_TODAY = "Today"
    LBL_ST_TBLHDR_LAST24H = "Last 24h"
    LBL_ST_TBLHDR_LASTWEEK = "Last week"
    BTN_ST_INSPECT = "Inspect"

    #anomaly plots
    LBL_TAB_ANOM_PLOTS = "Anomaly plot and explanations"
    LBL_AP_TITLE = "Trend of anomalies and explanations"
    BTN_AP_REFRESHPLOT = "Load"
    LBL_AP_PLOT_ANOMALYTRENDS = "Trend of anomalies (10min interval averages)"
    LBL_AP_PLOT_ROOTCAUSE = "Root cause explanations"
    LBL_AP_START = "Start: [start date]"
    LBL_AP_END = "End: [end date]"
    LBL_AP_START_TRAIN = "Start (training set): [start date]"
    LBL_AP_END_TRAIN = "End (training set): [end date]"
    LBL_AP_PLOT_BOXPLOT = "Distributions: training set vs selected time window"

    LBL_START = "Start: "
    LBL_END = "End: "
    LBL_TRAIN_START = "Start (training set): "
    LBL_TRAIN_END = "End (training set): "

    LOADIND_TYPE  = "circle"

    BTN_ST_REFRESH_TABLE = "Refresh table"
