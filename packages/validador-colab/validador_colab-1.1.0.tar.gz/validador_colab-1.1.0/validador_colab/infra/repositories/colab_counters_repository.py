from validador_colab.core.repositories import ColabCountersRepository
from validador_colab.infra.database import DBConnectionHandlerPostgres
from validador_colab.infra.configs import CONFIGS


class ColabCountersRepositoryPostgres(ColabCountersRepository):

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
            cte_fatcupom as (
            SELECT
                            dp.seq_produto as seq_produto,
                            fc.dt_venda as dt_venda,
                            fc.id_cliente as id_cliente,
                            sum(fc.qtd_produto) as qtd_fatcupom,
                            max(fc.dt_hr_carga) as dt_hr_carga
            from cte_produto cp
            join dw.dim_produto dp on (cp.seq_produto,cp.id_cliente) = (dp.seq_produto,dp.id_cliente)
            join dw.fat_cupom fc on dp.id_produto = fc.id_produto
            where fc.dt_venda between '{date_start}' and '{date_end}'
            group by dp.seq_produto, fc.dt_venda,fc.id_cliente
            )
            select distinct
                            cfc.seq_produto as seq_produto,
                            cfc.dt_venda as dt_venda,
                            cfc.id_cliente as id_cliente,
                            cfc.qtd_fatcupom
            from cte_fatcupom cfc
            order by cfc.dt_venda, cfc.id_cliente, cfc.seq_produto;
            """

            CONFIGS.COLAB_DB = 'dw'
            db = DBConnectionHandlerPostgres()
            data = db.get('COLAB', sql)

            return data
