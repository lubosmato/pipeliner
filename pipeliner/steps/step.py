from abc import ABC, abstractmethod
from typing import Any


class Step(ABC):
    @abstractmethod
    def perform(self, data: Any) -> Any:
        pass
