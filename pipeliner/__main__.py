import json
import logging
import logging.config
import os
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
from pathlib import Path

from pipeliner import StepFactory, PipelineFactory, Pipeline

logger = logging.getLogger(__name__)


def load_config(path: str) -> dict:
    try:
        path = Path(path).resolve()
        if path.suffix.lower() != ".json":
            raise ArgumentTypeError(f"Given config path {path} is not a valid JSON file")

        if not path.is_file():
            cwd = Path(os.getcwd()).resolve()
            path = cwd / path

        if path.is_file():
            with open(str(path), "r") as config_file:
                return json.load(config_file)

        raise FileNotFoundError(f"{path} is not a valid file")

    except Exception as e:
        raise ArgumentTypeError(f"Could not parse config {path} because {e}")


def main():
    load_logger_config()

    parser = ArgumentParser(
        description=r"""
    ____  _            ___                
   / __ \(_)___  ___  / (_)___  ___  _____
  / /_/ / / __ \/ _ \/ / / __ \/ _ \/ ___/
 / ____/ / /_/ /  __/ / / / / /  __/ /    
/_/   /_/ .___/\___/_/_/_/ /_/\___/_/     
       /_/                                
Get rid of repetitive tasks. Make yourself more happy.
""",
        formatter_class=RawTextHelpFormatter,
        add_help=True
    )
    parser.add_argument(
        "config",
        type=load_config,
        metavar="config",
        help="path to a config JSON file"
    )
    args = parser.parse_args()
    config = args.config

    custom_steps_path = Path(config.get("custom_steps", "")).resolve()
    step_factory = StepFactory(custom_steps_path)
    pipeline_factory = PipelineFactory(step_factory)

    pipelines = [
        pipeline_factory.create(pipeline_config)
        for pipeline_config in config.get("pipelines", [])
    ]

    # for pipeline in pipelines:
    #     pipeline.run()
    # 
    # print(pipelines)


def load_logger_config():
    log_config_path = str(Path(__file__).resolve().parent / "log_config.json")
    with open(log_config_path, "r") as log_config_file:
        log_config = json.load(log_config_file)
        logging.config.dictConfig(log_config)


if __name__ == '__main__':
    main()
