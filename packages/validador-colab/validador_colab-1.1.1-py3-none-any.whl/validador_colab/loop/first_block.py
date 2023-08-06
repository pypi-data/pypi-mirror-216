from validador_colab.infra.repositories import SmarketAnalyticsRepositoryPostgres, ColabCountersRepositoryPostgres
from validador_colab.core.usecases import SmarketService, ColabService
from validador_colab.core.entities import Sakura, NaturalOne, ValidationDetail
from validador_colab.core.errors import NoDataFound
from validador_colab.infra.database import DBConnectionHandlerPostgres, DBConnectionHandlerPostgresControle, DB_CONTROLE
from validador_colab.infra.utils import break_no_data_found
import pickle
import os
import asyncio
import datetime

temp_data_folder = os.path.join(os.getcwd(), 'temp_data')

db = DBConnectionHandlerPostgresControle()


async def first_block(industry_id: int, date_start, date_end, print_corretos=True, pickle_use=False):
    if not os.path.exists(temp_data_folder):
        os.makedirs(temp_data_folder)

    if industry_id == 11: #Natural One
        industry = NaturalOne()
    elif industry_id == 13: #Sakura
        industry = Sakura()

    pickle_colab_name = "colab_data_" + industry.__repr__() + "_" + date_start + "_" + date_end + ".pkl"
    pickle_smarket_name = "smarket_data_" + industry.__repr__() + "_" + date_start + "_" + date_end + ".pkl"

    if pickle_use:

        try:
            if not os.path.exists(os.path.join(temp_data_folder, pickle_smarket_name)):
                print("Getting data from smarket")
                smarket_data = SmarketService(SmarketAnalyticsRepositoryPostgres()).get_smarket_counters(industry, date_start, date_end)
                with open(os.path.join(temp_data_folder, pickle_smarket_name), 'wb') as f:
                    pickle.dump(smarket_data, f)
                print("Data saved")
            else:
                print("Loading data from smarket")
                with open(os.path.join(temp_data_folder, pickle_smarket_name), 'rb') as f:
                    smarket_data = pickle.load(f)
                print("Data loaded")

            if not os.path.exists(os.path.join(temp_data_folder, pickle_colab_name)):
                print("Getting data from colab")
                colab_data = ColabService(ColabCountersRepositoryPostgres()).get_colab_counters(industry_id, date_start, date_end)
                with open(os.path.join(temp_data_folder, pickle_colab_name), 'wb') as f:
                    pickle.dump(colab_data, f)
                print("Data saved")
            else:
                print("Loading data from colab")
                with open(os.path.join(temp_data_folder, pickle_colab_name), 'rb') as f:
                    colab_data = pickle.load(f)
                print("Data loaded")
        except NoDataFound:
            print(f"Sem dados cadastrados para a industria no dia {date_start} até o dia {date_end}")

    else:
        print("Getting data from smarket")
        smarket_data = SmarketService(SmarketAnalyticsRepositoryPostgres()).get_smarket_counters(industry, date_start,
                                                                                                 date_end)
        print("Getting data from colab")
        colab_data = ColabService(ColabCountersRepositoryPostgres()).get_colab_counters(industry_id, date_start,
                                                                                        date_end)


    if len(smarket_data) == 0 or len(colab_data) == 0:
        print("Erro na execução:")
        print(f"Data de consulta: {date_start} - {date_end}")
        print(f"len(smarket_data) = {len(smarket_data)}")
        print(f"len(colab_data) = {len(colab_data)}")
        print("Classificando dias como não aptos a atualização")

        DB_CONTROLE.insert(break_no_data_found(industry, date_start, date_end))
        print("Finalizando processo")
        return 0

    #esta merda aqui vai ficar troncha, loop dentro de loop, mas é o que tem pra hoje
    print('Iniciando processamento')
    count_produtos_certos = {}
    count_produtos_errados = {}
    validation_intel = []


    # Primeira validação: Se o produto está com os quantitativos iguais na fat_cupom e no Analytics
    for colab_unit in colab_data:
        for smarket_unit in smarket_data:
            if colab_unit.id_cliente == smarket_unit.client_id:
                if colab_unit.date == smarket_unit.date:
                    if int(colab_unit.seqproduto) == int(smarket_unit.seqproduto):
                        if colab_unit.seqproduto == 164059:
                            print("Me gusta lá conchita")
                        if int(colab_unit.qtd_fatcupom) == int(smarket_unit.analytics):
                            if print_corretos:
                                print('-------------------')
                                print(f'Cliente {smarket_unit.client_id}')
                                print(f"Data {smarket_unit.date}")
                                print(f'Tudo certo no produto: {smarket_unit.seqproduto} - {smarket_unit.description}')
                                print(f'Quantitativo no analytics: {smarket_unit.analytics}')
                                print(f'Quantitativo na fatcupom colab: {colab_unit.qtd_fatcupom}')
                                print('-------------------')
                            if smarket_unit.client_id not in count_produtos_certos:
                                count_produtos_certos[smarket_unit.client_id] = {}

                            if smarket_unit.date not in count_produtos_certos[smarket_unit.client_id]:
                                count_produtos_certos[smarket_unit.client_id][smarket_unit.date] = 0

                            count_produtos_certos[smarket_unit.client_id][smarket_unit.date] += 1

                        else:
                            print('-------------------')
                            print(f'Cliente {smarket_unit.client_id}')
                            print(f"Data {smarket_unit.date}")
                            print(f'ERRO no produto: {smarket_unit.seqproduto} - {smarket_unit.description}')
                            print(f'Quantitativo no analytics: {smarket_unit.analytics}')
                            print(f'Quantitativo na fatcupom colab: {colab_unit.qtd_fatcupom}')
                            print('-------------------')
                            if smarket_unit.client_id not in count_produtos_errados:
                                count_produtos_errados[smarket_unit.client_id] = {}

                            if smarket_unit.date not in count_produtos_errados[smarket_unit.client_id]:
                                count_produtos_errados[smarket_unit.client_id][smarket_unit.date] = 0

                            count_produtos_errados[smarket_unit.client_id][smarket_unit.date] += 1

    # Segunda validação - Produtos presentes nas tabelas:
    prod_cliente_data = {}
    colab_cliente_data = {}
    produtos_ausentes_analytics = {}
    produtos_ausentes_colab = {}
    datas_para_nao_subir = {}

    for colab_unit in colab_data:
        if colab_unit.id_cliente not in colab_cliente_data:
            colab_cliente_data[colab_unit.id_cliente] = {}
        if colab_unit.date not in colab_cliente_data[colab_unit.id_cliente]:
            colab_cliente_data[colab_unit.id_cliente][colab_unit.date] = []
        if colab_unit.seqproduto not in colab_cliente_data[colab_unit.id_cliente][colab_unit.date]:
            colab_cliente_data[colab_unit.id_cliente][colab_unit.date].append(colab_unit.seqproduto)

    for smarket_unit in smarket_data:
        if smarket_unit.client_id not in prod_cliente_data:
            prod_cliente_data[smarket_unit.client_id] = {}
        if smarket_unit.date not in prod_cliente_data[smarket_unit.client_id]:
            prod_cliente_data[smarket_unit.client_id][smarket_unit.date] = []
        if smarket_unit.seqproduto not in prod_cliente_data[smarket_unit.client_id][smarket_unit.date]:
            prod_cliente_data[smarket_unit.client_id][smarket_unit.date].append(smarket_unit.seqproduto)

    #Gerador produtos ausentes colab
    for client_id, date_counter in prod_cliente_data.items():
        for date, prod_list in date_counter.items():
            for prod in prod_list:
                if client_id in colab_cliente_data:
                    if date in colab_cliente_data[client_id]:
                        if prod not in colab_cliente_data[client_id][date]:
                            if client_id not in produtos_ausentes_colab:
                                produtos_ausentes_colab[client_id] = {}
                            if date not in produtos_ausentes_colab[client_id]:
                                produtos_ausentes_colab[client_id][date] = []
                            print(f"Produto {prod} não encontrado na base do colab para cliente: {client_id} na data: {date}, para a industria {industry_id}")
                            produtos_ausentes_colab[client_id][date].append(prod)
                    else:
                        print(f"Data: {date} não encontrada na base do colab para cliente: {client_id} para a industria {industry_id}")
                        if client_id not in datas_para_nao_subir:
                            datas_para_nao_subir[client_id] = []
                        if date not in datas_para_nao_subir[client_id]:
                            validation_intel.append(ValidationDetail(
                                exec_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                industry_id=industry_id,
                                client_id=client_id,
                                sale_date=date,
                                validation_status=False
                            ))
                            datas_para_nao_subir[client_id].append(date)

                        break

                else:
                    print(f"Cliente {client_id} não encontrado na base do colab para industria: {industry_id}")

        # Gerador produtos ausentes analitycs
        for client_id, date_counter in colab_cliente_data.items():
            for date, prod_list in date_counter.items():
                for prod in prod_list:
                    if client_id in prod_cliente_data:
                        if date in prod_cliente_data[client_id]:
                            if prod not in prod_cliente_data[client_id][date]:
                                if client_id not in produtos_ausentes_analytics:
                                    produtos_ausentes_analytics[client_id] = {}
                                if date not in produtos_ausentes_analytics[client_id]:
                                    produtos_ausentes_analytics[client_id][date] = []
                                produtos_ausentes_analytics[client_id][date].append(prod)
                                print(f"Produto {prod} não encontrado na base do analytics para cliente: {client_id} na data: {date} para a industria {industry_id}")

                        else:
                            print(f"Data: {date} não encontrada na base do analytics para cliente: {client_id} para a industria {industry_id}")
                            if client_id not in datas_para_nao_subir:
                                datas_para_nao_subir[client_id] = []
                            if date not in datas_para_nao_subir[client_id]:
                                validation_intel.append(ValidationDetail(
                                    exec_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    industry_id=industry_id,
                                    client_id=client_id,
                                    sale_date=date,
                                    validation_status=False
                                ))
                                datas_para_nao_subir[client_id].append(date)
                            break

                    else:
                        print(f"Cliente {client_id} não encontrado na base do colab para industria: {industry_id}")

    # Geração da primeira tabela com base nos valores errados
    if len(count_produtos_errados) > 0:
        for client_id, counter in count_produtos_errados.items():
            for date, count in counter.items():
                if client_id in datas_para_nao_subir:
                    if date.strftime("%Y-%m-%d") not in [x.strftime("%Y-%m-%d") for x in datas_para_nao_subir[client_id]]:
                        if count > 0:
                            validation_intel.append(
                                ValidationDetail(
                                    exec_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    industry_id=industry_id,
                                    client_id=client_id,
                                    sale_date=date,
                                    validation_status=False
                                )
                            )
                        else:
                            validation_intel.append(
                                ValidationDetail(
                                    exec_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    industry_id=industry_id,
                                    client_id=client_id,
                                    sale_date=date,
                                    validation_status=True
                                )
                            )
                else:
                    validation_intel.append(
                        ValidationDetail(
                            exec_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            industry_id=industry_id,
                            client_id=client_id,
                            sale_date=date,
                            validation_status=False
                        )
                    )
                    if client_id not in datas_para_nao_subir:
                        datas_para_nao_subir[client_id] = []
                    if date not in datas_para_nao_subir[client_id]:
                        datas_para_nao_subir[client_id].append(date)



    if len(count_produtos_certos) > 0:
        for client_id, counter in count_produtos_certos.items():
            for date, count in counter.items():
                if client_id in datas_para_nao_subir:
                    if date.strftime("%Y-%m-%d") not in [x.strftime("%Y-%m-%d") for x in datas_para_nao_subir[client_id]]:
                        if count > 0:
                            validation_intel.append(
                                ValidationDetail(
                                    exec_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    industry_id=industry_id,
                                    client_id=client_id,
                                    sale_date=date,
                                    validation_status=True
                                )
                            )
                else:
                    validation_intel.append(
                        ValidationDetail(
                            exec_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            industry_id=industry_id,
                            client_id=client_id,
                            sale_date=date,
                            validation_status=True
                        )
                    )

    # Inserindo os dados no banco de validation:
    sql_insert = """INSERT INTO
        PUBLIC.CONTROLE(id_industria, id_cliente, dt_venda, status_validacao, etapa)
        VALUES
    """
    for validation in validation_intel:
        sql_insert += f""" ({int(validation.industry_id)}, {int(validation.client_id)}, '{validation.sale_date}', {bool(validation.validation_status)}, 'fat_cupom'),"""

    sql_insert = sql_insert[:-1]
    print(sql_insert)

    DB_CONTROLE.insert(sql_insert)

if __name__ == "__main__":
    asyncio.run(first_block(11, '2023-06-23', '2023-06-23', False, True))
