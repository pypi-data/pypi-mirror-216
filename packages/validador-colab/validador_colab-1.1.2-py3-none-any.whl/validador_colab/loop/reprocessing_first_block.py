from validador_colab.loop import first_block
import pickle
import os
import asyncio
import datetime
from validador_colab.core.entities import Sakura, NaturalOne
from validador_colab.infra.utils import clean_old_data
from validador_colab.infra.database import DB_CONTROLE


temp_data_folder = os.path.join(os.getcwd(), 'temp_data')


async def reprocessing_first_block(industry_id: int, date_start, date_end, print_corretos=True):

    if industry_id == 11: #Natural One
        industry = NaturalOne()
    elif industry_id == 13: #Sakura
        industry = Sakura()

    sqls = clean_old_data(industry, date_start, date_end)
    print(f"Limpado dado já cadastrados para a industria {industry.id} no periodo de {date_start} a {date_end}")
    for sql in sqls:
        DB_CONTROLE.insert(sql)

    await first_block(industry_id, date_start, date_end, print_corretos)

if __name__ == "__main__":
    from validador_colab.core.entities import NaturalOne
    asyncio.run(reprocessing_first_block(11, '2023-06-22', '2023-06-22'))


