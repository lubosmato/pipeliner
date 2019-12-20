import importlib
import sys
from pathlib import Path

from pipeliner.steps import *


class StepFactory:
    def __init__(self, custom_steps_path: Path):
        self._custom_steps_path = custom_steps_path

    def create(self, steps_config: dict) -> Step:
        self._import_custom_steps()

        for step_config in steps_config:
            if step_config["class"] not in globals():
                raise ModuleNotFoundError(f"could not find step class: {step_config['class']}")

        steps = [
            globals()[step_config["class"]](**step_config.get("params", dict()))
            for step_config in steps_config
        ]
        for i, step in enumerate(steps[0:-1]):
            step.set_next_step(steps[i + 1])

        return steps[0]

    def _import_custom_steps(self):
        sys.path.append(str(self._custom_steps_path.parent))
        custom_steps_module = importlib.import_module(str(self._custom_steps_path.name))
        if "__all__" in custom_steps_module.__dict__:
            custom_steps = custom_steps_module.__dict__["__all__"]
        else:
            custom_steps = [
                custom_step
                for custom_step in custom_steps_module.__dict__
                if not custom_step.startswith("_")
            ]
        globals().update({
            key: getattr(custom_steps_module, key)
            for key in custom_steps
        })
