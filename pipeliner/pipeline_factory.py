from pipeliner import Pipeline, StepFactory


class PipelineFactory:
    def __init__(self, step_factory: StepFactory):
        self._step_factory = step_factory

    def create(self, pipeline_config: dict) -> Pipeline:
        return Pipeline(
            pipeline_config["name"],
            pipeline_config["schedule"],
            self._step_factory.create(pipeline_config["steps"])
        )
