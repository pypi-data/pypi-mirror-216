from validador_colab.core.repositories import SmarketAnalyticsRepository
from validador_colab.infra.configs import CONFIGS
from validador_colab.infra.database import DBConnectionHandlerPostgres


def client(client_id):
    if client_id == 20:
        return 'IMPERATRIZ'
    elif client_id == 30:
        return 'SUPERNOSSO'
    elif client_id == 70:
        return 'BRASILATACADISTA'


class SmarketAnalyticsRepositoryPostgres(SmarketAnalyticsRepository):

    def get_data(self, industry, date_start: str, date_end: str, client_id: int = None):

        sql = f"""
        with cte_produto as (
        select 	cast(sp.seqproduto as int) seqproduto,
                sp.descricao,
                spe.ean,
                sf.seqfornecedor,
                sf.fornecedor
        from smarket_produto sp
        join smarket_produto_ean spe on spe.seqproduto=sp.seqproduto
        join smarket_fornecedor sf on sf.seqfornecedor=sp.seqfornecedor
        where cast(sp.seqproduto as int) in ({','.join([str(x) for x in industry.products])}) /*NATURAL ONE*/
        ),
        cte_analytics as (
        SELECT dt,
               cast(seqproduto as int) seqproduto,
               sum(quantidade) analytics
        from public.smarket_analytics sa
        where dt between '{date_start}' and '{date_end}'
        group by 1, 2
        order by 1, 3
        )
        select
                ca.seqproduto,
                ca.dt,
                cp.descricao,
                cp.ean,
                ca.analytics
        from cte_analytics ca
        join cte_produto cp on cp.seqproduto=ca.seqproduto
        order by dt, seqproduto
        """

        data = []

        CONFIGS.CLIENT_ID = f"db_{client(client_id).lower()}"
        db = DBConnectionHandlerPostgres()
        data.extend(db.get('SMARKET', sql))

        return data
