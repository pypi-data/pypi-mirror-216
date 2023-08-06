from abc import ABC, abstractmethod


class SmarketAnalyticsRepository(ABC):

    @abstractmethod
    def get_data(self, industry, date_start: str, date_end: str):
        pass
