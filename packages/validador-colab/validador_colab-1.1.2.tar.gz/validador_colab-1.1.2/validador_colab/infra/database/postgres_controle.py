from sqlalchemy import pool
from validador_colab.infra.configs import CONFIGS
import psycopg2
import os
import sshtunnel


class DBConnectionHandlerPostgresControle:

    @staticmethod
    def getconn_colab():
        c = psycopg2.connect(
            user=CONFIGS.COLAB_PROD_USERNAME,
            password=CONFIGS.COLAB_PROD_PASSWORD,
            host=CONFIGS.COLAB_PROD_HOST,
            database=CONFIGS.COLAB_PROD_NAME,
            port=CONFIGS.COLAB_PROD_PORT
        )
        return c

    def __init__(self):
        # pool_colab = pool.QueuePool(
        #     self.getconn_colab, max_overflow=0, pool_size=2)
        # self.conn_colab = pool_colab.connect()
        # self.cursor_colab = self.conn_colab.cursor()
        pass

    # def get(self, sql):
    #     conn_colab = self.getconn_colab()
    #     with conn_colab.cursor() as colab_curs:
    #         try:
    #             colab_curs.execute(sql)
    #         except Exception as e:
    #             colab_curs.execute("rollback")
    #         finally:
    #             colab_curs.execute("commit")
    #     conn_colab.close()

    def insert(self, sql, mode='COLAB'):
        if mode.upper() == "COLAB":
            conn_colab = self.getconn_colab()
            with conn_colab.cursor() as colab_curs:
                try:
                    colab_curs.execute(sql)
                except Exception as e:
                    print(e)
                    colab_curs.execute('rollback')
                finally:
                    colab_curs.execute('commit')
                conn_colab.close()