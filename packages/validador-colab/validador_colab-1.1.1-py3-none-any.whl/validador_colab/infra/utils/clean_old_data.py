def clean_old_data(industry, date_start, date_end):

    sql_base = "DELETE FROM PUBLIC.CONTROLE "

    sqls = []

    # date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    # date_finish = datetime.datetime.strptime(date_end, "%Y-%m-%d")
    # numdays = date_finish - date_start
    #
    # date_list = [date_finish - datetime.timedelta(days=x) for x in range(numdays.days + 1)]

    for client in industry.clients:
        sql_client = sql_base
        sql_client += f"""where id_cliente = {client} and dt_venda between '{date_start}' and '{date_end}'"""
        sqls.append(sql_client)

    print(sqls)
    return sqls

if __name__ == "__main__":
    from validador_colab.core.entities import Sakura
    clean_old_data(Sakura(), '2023-06-20', '2023-06-21')