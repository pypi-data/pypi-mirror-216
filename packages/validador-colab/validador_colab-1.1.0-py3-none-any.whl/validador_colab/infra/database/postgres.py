from validador_colab.infra.configs import CONFIGS
import psycopg2


class DBConnectionHandlerPostgres:

    # def start_smarket_tunnel(self):
    #     """Somente utilizar em caso de dev"""
    #     self.ssh_tunnel = sshtunnel.SSHTunnelForwarder(
    #         ('20.0.1.66', 22),
    #         ssh_username='davi_araujo',
    #         ssh_pkey=os.path.join('home', 'davi', '.ssh', 'id_ed25519'),
    #         ssh_private_key_password='',
    #         remote_bind_address=('20.0.1.66', 22)
    #     )
    #
    #     self.ssh_tunnel.start()
    #
    # def stop_smarket_tunnel(self):
    #     "Implementar para fazer este treco parar de rodar no final da execução"
    #     self.ssh_tunnel.stop()

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

    @staticmethod
    def getconn_smarket():
        c = psycopg2.connect(
            user=CONFIGS.SMARKET_PROD_USERNAME,
            password=CONFIGS.SMARKET_PROD_PASSWORD,
            host=CONFIGS.SMARKET_PROD_HOST,
            port=CONFIGS.COLAB_PROD_PORT,
            database=CONFIGS.CLIENT_ID)
        return c

    def __init__(self):
        # self.ssh_tunnel = None
        # if CONFIGS.MODE == 'DEV':
        #     self.start_smarket_tunnel()
        # pool_colab = pool.QueuePool(
        #     self.getconn_colab, max_overflow=0, pool_size=2)
        # pool_smarket = pool.QueuePool(
        #     self.getconn_smarket, max_overflow=0, pool_size=2)
        # self.conn_colab = pool_colab.connect()
        # self.conn_smarket = pool_smarket.connect()
        # self.cursor_colab = self.conn_colab.cursor()
        # self.cursor_smarket = self.conn_smarket.cursor()
        pass

    def get(self, mode: str, sql: str):

        values = [()]

        if mode.upper() == 'COLAB':
            conn_clb = self.getconn_colab()
            with conn_clb.cursor() as colab_curs:
                colab_curs.execute(sql)
                try:
                    values = colab_curs.fetchall()
                except Exception as e:
                    colab_curs.execute('rollback')
                finally:
                    colab_curs.execute('commit')
                conn_clb.close()
                return values

        elif mode.upper() == 'SMARKET':
            conn_smkt = self.getconn_smarket()
            with conn_smkt.cursor() as smkt_curs:
                smkt_curs.execute(sql)
                try:
                    values = smkt_curs.fetchall()
                except Exception as e:
                    smkt_curs.execute('rollback')
                finally:
                    smkt_curs.execute('commit')
                conn_smkt.close()
                return values

    def insert(self, sql, mode='COLAB'):
        if mode.upper() == "COLAB":
            conn_clb = self.conn_colab()
            with conn_clb.cursor() as colab_curs:
                try:
                    colab_curs.execute(sql)
                except Exception as e:
                    colab_curs.execute('rollback')
                finally:
                    colab_curs.execute('commit')
                conn_clb.close()



if __name__ == "__main__":

    db = DBConnectionHandlerPostgres()
    print(db.get('smarket', 'select now();'))
    #db.stop_smarket_tunnel()
    print(db.get('smarket', 'select now();'))
