from abc import abstractmethod
from datetime import date
from typing import List, Optional


class CurrencyChecker:
    def __init__(self, base: str, currency: str) -> None:
        self._base = base
        self._currency = currency

    @abstractmethod
    def get_exchange_rate(self, date: Optional[date] = None) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_time_series(self, start: date, end: date) -> List[float]:
        raise NotImplementedError
