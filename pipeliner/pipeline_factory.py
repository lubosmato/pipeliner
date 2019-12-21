from pipeliner import Pipeline, StepsFactory


class PipelineFactory:
    def __init__(self, steps_factory: StepsFactory):
        self._steps_factory = steps_factory

    def create(self, pipeline_config: dict) -> Pipeline:
        return Pipeline(
            pipeline_config["name"],
            pipeline_config["schedule"],
            self._steps_factory.create(pipeline_config["steps"])
        )
