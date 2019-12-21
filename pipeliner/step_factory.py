import importlib
import sys
from pathlib import Path

from pipeliner.steps import Step


class StepFactory:
    def __init__(self, custom_steps_path: Path):
        self._custom_steps_path = custom_steps_path

    def create(self, steps_config: list) -> Step:
        self._import_steps_modules()

        steps = [
            self.create_step(step_config)
            for step_config in steps_config
        ]
        for i, step in enumerate(steps[0:-1]):
            step.set_next_step(steps[i + 1])

        return steps[0]

    def _import_steps_modules(self) -> None:
        self._import_steps_module(self._custom_steps_path)
        steps_path = Path(__file__).resolve().parent / "steps"
        self._import_steps_module(steps_path)

    def _import_steps_module(self, module_path: Path):
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

    def create_step(self, step_config: dict):
        if step_config["class"] not in globals():
            raise ModuleNotFoundError(f"could not find step class: {step_config['class']}")
        return globals()[step_config["class"]](**step_config.get("params", dict()))
