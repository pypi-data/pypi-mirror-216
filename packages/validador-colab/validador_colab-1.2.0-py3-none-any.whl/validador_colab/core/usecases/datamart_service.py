from validador_colab.core.entities import DatamartCounter
from validador_colab.core.repositories import DatamartCountersRepository
from validador_colab.core.errors import NoDataFound
from datetime import datetime


class DatamartService:

    def __init__(self, datamart_counters_repository: DatamartCountersRepository):
        self.datamart_counters_repository = datamart_counters_repository

    def get_datamart_counters(self, industry_id, date_start: str = None, date_end: str = None):
        datamart_counters = []
        if date_start is None and date_end is None:
            date_start = datetime.now().strftime("%Y-%m-%d")
            date_end = datetime.now().strftime("%Y-%m-%d")
        else:
            date_start = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y-%m-%d")
            date_end = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y-%m-%d")

        data = self.datamart_counters_repository.get_data(industry_id, date_start, date_end)
        if len(data) > 0:
            for unit in data:
                datamart_counters.append(DatamartCounter(unit[0], unit[1], unit[2], unit[3]))
            return datamart_counters
        else:
            print(f"Sem dados para a industria {industry_id}, na data {date_start} até {date_end}")
            return []
