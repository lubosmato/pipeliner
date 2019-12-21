from typing import Any

from pipeliner.steps import Step


class DoNothing(Step):
    def perform(self, data: Any) -> Any:
        return data
