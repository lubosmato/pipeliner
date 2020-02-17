from pathlib import Path
from typing import Any

import pytest

from pipeliner import Pipeline, PipelineFactory, StepsFactoryWithCustomSteps
from pipeliner.schedule import Schedule
from pipeliner.steps import DoNothing, ProduceText, Step


def test_pipeline_factory():
    steps_factory = StepsFactoryWithCustomSteps(Path("./custom_steps/"))
    factory = PipelineFactory(steps_factory)
    pipeline_config = {
        "name": "Say hello",
        "schedule": "* * * * *",
        "steps": [
            {
                "class": "ProduceText",
                "params": {
                    "text": "Hello test!"
                }
            },
            {
                "class": "DoNothing"
            },
            {
                "class": "DoNothing"
            }
        ]
    }
    pipeline = factory.create(pipeline_config)

    assert pipeline.name == "Say hello"
    assert len(pipeline._steps) == 3
    assert pipeline._steps[0]._text == "Hello test!"


def test_pipeline(mocker):
    steps = [ProduceText("Hello test!"), DoNothing(), DoNothing()]
    mock_steps = [
        mocker.spy(step, "perform")
        for step in steps
    ]

    pipeline = Pipeline("Test pipeline", "* * * * *", steps)
    assert pipeline.name == "Test pipeline"
    assert type(pipeline.schedule) is Schedule
    pipeline.run()

    mock_steps[0].assert_called_once_with(None)
    mock_steps[1].assert_called_once_with("Hello test!")
    mock_steps[2].assert_called_once_with("Hello test!")


def test_pipeline_step_fails(mocker):
    class FailingStep(Step):
        def perform(self, data: Any) -> Any:
            raise RuntimeError("This step just fails")

    steps = [ProduceText("Hello test!"), FailingStep(), DoNothing()]
    mock_steps = [
        mocker.spy(step, "perform")
        for step in steps
    ]

    pipeline = Pipeline("Test pipeline", "* * * * *", steps)
    assert pipeline.name == "Test pipeline"
    assert type(pipeline.schedule) is Schedule

    with pytest.raises(Exception):
        pipeline.run()

    mock_steps[0].assert_has_calls([mocker.call(None)])
    mock_steps[1].assert_has_calls(
        [
            mocker.call("Hello test!")
        ] * Pipeline.STEP_REPEAT_TRY_COUNT
    )
    mock_steps[2].assert_not_called()
