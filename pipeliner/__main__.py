import json
import logging
import logging.config
import os
import time
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
from pathlib import Path
from typing import List

from pipeliner.pipeline_runner import PipelineRunner
from . import config

from pipeliner import StepsFactory, PipelineFactory, Pipeline

logger = logging.getLogger(__name__)


class Pipeliner:
    runners: List[PipelineRunner]
    pipelines: List[Pipeline]

    def __init__(self):
        self.load_logger_config()
        self.parser = ArgumentParser(
            description=r"""
    ____  _            ___                
   / __ \(_)___  ___  / (_)___  ___  _____
  / /_/ / / __ \/ _ \/ / / __ \/ _ \/ ___/
 / ____/ / /_/ /  __/ / / / / /  __/ /    
/_/   /_/ .___/\___/_/_/_/ /_/\___/_/     
       /_/                                
Get rid of repetitive tasks. Make yourself happier.
""",
            formatter_class=RawTextHelpFormatter,
            add_help=True
        )
        self.parser.add_argument(
            "config",
            type=self.load_config,
            metavar="config",
            help="path to a config JSON file"
        )
        args = self.parser.parse_args()
        config.config = args.config

        custom_steps_path = Path(config.config.get("custom_steps", "")).resolve()
        self.steps_factory = StepsFactory(custom_steps_path)
        self.pipeline_factory = PipelineFactory(self.steps_factory)
        self.pipelines = []
        self.runners = []

    @staticmethod
    def load_logger_config():
        log_config_path = str(Path(__file__).resolve().parent / "log_config.json")
        with open(log_config_path, "r") as log_config_file:
            log_config = json.load(log_config_file)
            logging.config.dictConfig(log_config)

    @staticmethod
    def load_config(path: str) -> dict:
        try:
            path = Path(path).resolve()
            if path.suffix.lower() != ".json":
                raise ArgumentTypeError(f"Given config path {path} is not a valid JSON file")

            if not path.is_file():
                cwd = Path(os.getcwd()).resolve()
                path = cwd / path

            if path.is_file():
                with open(str(path), encoding="utf8", mode="r") as config_file:
                    return json.load(config_file)

            raise FileNotFoundError(f"{path} is not a valid file")

        except Exception as e:
            raise ArgumentTypeError(f"Could not parse config {path} because {e}")

    def run(self):
        self.pipelines = [
            self.pipeline_factory.create(pipeline_config)
            for pipeline_config in config.config.get("pipelines", [])
        ]
        if not self.pipelines:
            logger.warning("No pipelines were found. Add a pipeline into configuration to run Pipeliner.")
        else:
            logger.info(f"Found {len(self.pipelines)} pipelines. Creating and starting runners...")

        self.runners = [
            PipelineRunner(pipeline)
            for pipeline in self.pipelines
        ]
        for runner in self.runners:
            runner.start()

        try:
            logger.info("Running!")
            while True:
                time.sleep(10)
        except (KeyboardInterrupt, SystemExit):
            pass
        logger.info("Stopping runners.")
        self.stop()
        logger.info("I hope I helped you. Have a nice day! :)")

    def stop(self):
        for runner in self.runners:
            runner.stop()
        self.runners = []


if __name__ == '__main__':
    pipeliner = Pipeliner()
    pipeliner.run()
