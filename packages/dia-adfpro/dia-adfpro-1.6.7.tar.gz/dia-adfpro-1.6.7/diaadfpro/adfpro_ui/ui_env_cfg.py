import sys
import os

sys.path.insert(0, 'D:/Projects/Python/MQIT_DIA_AIML_Toolkit')

class Env():
    def __init__(self):
        self.HOST = '0.0.0.0'
        self.PORT = 8888
        self.DOMINO = False
        self.DEBUG = True
        self.DB_USER = 'dia_aas_user'
        self.DB_PASS = 'Naubtresjh#8753'
        self.ARTIFACTS_PATH = "D:/Projects/Python/MQIT_DIA_ADFPRO//examples/out"
        self.EQM_CFG_PATH = "D:/Projects/Python/MQIT_DIA_ADFPRO/examples"
        self.SSL_CERT = os.path.join('D:/Projects/PythonBatch/certificates/rds-dia_aas_db_prd.pem')
        self.LOG_CFG_PATH = "D:/Projects/Python/MQIT_DIA_ADFPRO/diaadfpro/adfpro_ui/ui_log.cfg"
        self.LAUNCH_CFG_PATH = "D:/Projects/Python/MQIT_DIA_ADFPRO/examples/launch_cfg.yml"

    def describe(self):
        return  "Host: {}, Port: {}, Domino: {}, Debug: {}, DB User: {}, Artifacts path: {}, Equipment cfg path: {}, SSL cert path: {}, Log cfg path: {}".\
            format(self.HOST, self.PORT, self.DOMINO, self.DEBUG, self.DB_USER, self.ARTIFACTS_PATH, self.EQM_CFG_PATH, self.SSL_CERT, self.LOG_CFG_PATH)

    def __str__(self):
        return self.describe()