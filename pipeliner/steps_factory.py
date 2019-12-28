import importlib
import sys
from abc import abstractmethod, ABC
from pathlib import Path
from typing import List

from pipeliner.steps import Step


class StepsFactory(ABC):
    @abstractmethod
    def create(self, steps_config: list) -> List[Step]:
        pass

    @abstractmethod
    def create_step(self, step_config: dict) -> Step:
        pass


class HasStepsFactoryMixin:
    def __init__(self, factory: StepsFactory):
        self._steps_factory = factory


class StepsFactoryWithCustomSteps(StepsFactory):
    def __init__(self, custom_steps_path: Path):
        self._custom_steps_path = custom_steps_path
        self._import_steps_modules()

    def create(self, steps_config: list) -> List[Step]:
        return [
            self.create_step(step_config)
            for step_config in steps_config
        ]

    def _import_steps_modules(self) -> None:
        self._import_steps_module(self._custom_steps_path)
        steps_path = Path(__file__).resolve().parent / "steps"
        self._import_steps_module(steps_path)

    def _import_steps_module(self, module_path: Path) -> None:
        sys.path.append(str(module_path.parent))
        custom_steps_module = importlib.import_module(str(module_path.name))
        if "__all__" in custom_steps_module.__dict__:
            custom_steps = custom_steps_module.__dict__["__all__"]
        else:
            custom_steps = (
                custom_step
                for custom_step in custom_steps_module.__dict__
                if not custom_step.startswith("_")
            )
        globals().update({
            key: getattr(custom_steps_module, key)
            for key in custom_steps
        })

    def create_step(self, step_config: dict) -> Step:
        if step_config["class"] not in globals():
            raise ModuleNotFoundError(f"could not find step class: {step_config['class']}")
        StepType = globals()[step_config["class"]]
        params = step_config.get("params", dict())

        if issubclass(StepType, HasStepsFactoryMixin):
            return StepType(self, **params)

        return StepType(**params)
