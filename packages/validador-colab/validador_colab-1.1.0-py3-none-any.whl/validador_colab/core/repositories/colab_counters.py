from abc import ABC, abstractmethod


class ColabCountersRepository(ABC):

    @abstractmethod
    def get_data(self, industry_id, date_start, date_end):
        pass