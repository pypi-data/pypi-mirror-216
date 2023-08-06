import os
from functools import lru_cache
import dotenv


class Configs:

    def __init__(self):

        dotenv.load_dotenv()
        self.SMARKET_PROD_HOST = os.getenv('SMARKET_PROD_HOST', 'rds-smarket-next-pg.cf6ldthil3ep.sa-east-1.rds.amazonaws.com')
        self.SMARKET_PROD_PORT = os.getenv('SMARKET_PROD_PORT', '5432')
        self.SMARKET_PROD_NAME = os.getenv('SMARKET_PROD_NAME', 'db_supernosso')
        self.SMARKET_PROD_USERNAME = os.getenv('SMARKET_PROD_USERNAME', 'davi_araujo')
        self.SMARKET_PROD_PASSWORD = os.getenv('SMARKET_PROD_PASSWORD', 'DVAJPG@2021*')
        self.COLAB_PROD_HOST = os.getenv('COLAB_PROD_HOST', '172.32.0.9')
        self.COLAB_PROD_PORT = os.getenv('COLAB_PROD_PORT', '5432')
        self.COLAB_PROD_NAME = os.getenv('COLAB_PROD_NAME', 'dw')
        self.COLAB_PROD_USERNAME = os.getenv('COLAB_PROD_USERNAME', 'gabriel_borges')
        self.COLAB_PROD_PASSWORD = os.getenv('COLAB_PROD_PASSWORD', ')_Gabriel!3076!Borges,(')
        self.CLIENT_ID = ''
        self.COLAB_DB = 'dw'
        self.MODE = 'DEV'


@lru_cache()
def get_configs():
    return Configs()
