from validador_colab.core.repositories import DatamartCountersRepository
from validador_colab.infra.database import DBConnectionHandlerPostgres
from validador_colab.infra.configs import CONFIGS


class DatamartCountersRepositoryPostgres(DatamartCountersRepository):

        def get_data(self, industry_id, date_start, date_end):

            cadastro = ''

            if industry_id == 11:
                cadastro = 'produto_natural_one'
            elif industry_id == 13:
                cadastro = 'produto_sakura'

            sql = f"""
            with cte_produto as (
                select distinct
                                dp.seq_produto,
                                dic.id_cliente
                            from cadastro.{cadastro} pno
                            join dw.dim_produto dp on ( array[pno.ean] <@ dp.eans )
                            join dw.dim_industria_cliente dic on (dp.id_cliente = dic.id_cliente)
                            join dw.dim_industria di on (dic.id_industria = di.id_industria)
                            where dic.id_industria = {industry_id}
            ),
            cte_datamart as (
            SELECT
                            dco.seq_produto as seq_produto,
                            dco.dt_venda as dt_venda,
                            dco.id_cliente as id_cliente,
                            sum(dco.qtd_produto) qtd_datamart,
                            max(dco.dt_hr_carga) as dt_hr_carga
            from datamart.colab dco
            where dco.dt_venda between '{date_start}' and '{date_end}'
            and exists ( select 1 from cte_produto cp where (dco.seq_produto,dco.id_cliente) = (cp.seq_produto,cp.id_cliente))
            group by dco.seq_produto,dco.dt_venda,dco.id_cliente
            )
            select distinct
                            dco.seq_produto as seq_produto,
                            dco.dt_venda as dt_venda,
                            dco.id_cliente as id_cliente,
                            dco.qtd_datamart
            from cte_datamart dco
            order by dco.dt_venda, dco.id_cliente, dco.seq_produto;
            """

            CONFIGS.COLAB_DB = 'dw'
            db = DBConnectionHandlerPostgres()
            data = db.get('COLAB', sql)

            return data
