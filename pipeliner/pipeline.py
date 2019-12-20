from pipeliner.steps.step import Step


class Pipeline:
    def __init__(self, name: str, schedule: str, beginning_step: Step):
        self._name = name
        self._schedule = schedule
        self._beginning_step = beginning_step

    def run(self) -> None:
        self._beginning_step.perform(None)

    @property
    def name(self) -> str:
        return self._name

    @property
    def schedule(self) -> str:
        return self._schedule
