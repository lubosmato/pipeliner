from abc import ABC, abstractmethod
from typing import Any


class Step(ABC):
    @abstractmethod
    def perform(self, data: Any) -> None:
        pass

    @abstractmethod
    def set_next_step(self, step: "Step") -> None:
        pass


class BasicStep(Step):
    _next_step: None or Step

    def __init__(self):
        self._next_step = None

    def set_next_step(self, step: "Step") -> None:
        self._next_step = step

    def perform(self, data: Any) -> None:
        if self._next_step is not None:
            self._next_step.perform(data)
