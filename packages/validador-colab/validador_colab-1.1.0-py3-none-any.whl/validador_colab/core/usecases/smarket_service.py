from validador_colab.core.entities import SmarketCounter
from validador_colab.core.repositories import SmarketAnalyticsRepository
from validador_colab.core.errors import NoDataFound
from datetime import datetime


class SmarketService:

    def __init__(self, smarket_analytics_repository: SmarketAnalyticsRepository):
        self.smarket_analytics_repository = smarket_analytics_repository

    def get_smarket_counters(self, industry, date_start: str = None, date_end: str = None):
        smarket_counters = []
        if date_start is None or date_end is None:
            date_start = datetime.now().strftime("%Y-%m-%d")
            date_end = datetime.now().strftime("%Y-%m-%d")
        else:
            date_start = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y-%m-%d")
            date_end = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y-%m-%d")
        #data = []
        for client_id in industry.clients:
            data = self.smarket_analytics_repository.get_data(industry, date_start, date_end, client_id)
            if len(data) > 0:
                for unit in data:
                    smarket_counters.append(SmarketCounter(unit[0], unit[1], unit[2], unit[3], unit[4], client_id))

        if len(smarket_counters) > 0:

            return smarket_counters
        else:
            return []


