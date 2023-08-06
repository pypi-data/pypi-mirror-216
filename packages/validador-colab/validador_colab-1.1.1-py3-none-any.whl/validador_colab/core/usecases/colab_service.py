from validador_colab.core.entities import ColabCounter
from validador_colab.core.repositories import ColabCountersRepository
from validador_colab.core.errors import NoDataFound
from datetime import datetime


class ColabService:

    def __init__(self, colab_counters_repository: ColabCountersRepository):
        self.colab_counters_repository = colab_counters_repository

    def get_colab_counters(self, industry_id, date_start: str = None, date_end: str = None):
        colab_counters = []
        if date_start is None and date_end is None:
            date_start = datetime.now().strftime("%Y-%m-%d")
            date_end = datetime.now().strftime("%Y-%m-%d")
        else:
            date_start = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y-%m-%d")
            date_end = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y-%m-%d")

        data = self.colab_counters_repository.get_data(industry_id, date_start, date_end)
        if len(data) > 0:
            for unit in data:
                colab_counters.append(ColabCounter(unit[0], unit[1], unit[2], unit[3]))
            return colab_counters
        else:
            print(f"Sem dados para a industria {industry_id}, na data {date_start} até {date_end}")
            return []
