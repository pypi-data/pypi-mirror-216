import datetime

def break_no_data_found(industry, date_start, date_end):

    sql_base = "INSERT INTO PUBLIC.CONTROLE(id_industria, id_cliente, dt_venda, status_validacao) VALUES "

    date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    date_finish = datetime.datetime.strptime(date_end, "%Y-%m-%d")
    numdays = date_finish - date_start

    date_list = [date_finish - datetime.timedelta(days=x) for x in range(numdays.days + 1)]

    for date in date_list:
        for client in industry.clients:
            sql_base += f"""({industry.id},{client},'{date.strftime("%Y-%m-%d")}', false),"""

    sql_base = sql_base[:-1]
    return sql_base

if __name__ == "__main__":
    from validador_colab.core.entities import Sakura
    break_no_data_found(Sakura(), '2023-06-20', '2023-06-21')