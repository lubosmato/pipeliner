import logging
from datetime import datetime
import time
from threading import Thread

from pipeliner import Pipeline

logger = logging.getLogger(__name__)


class PipelineRunner(Thread):
    _reading_worker: None or Thread

    def __init__(self, pipeline: Pipeline):
        super().__init__()
        self._running = False
        self._pipeline = pipeline

    def start(self) -> None:
        self._running = True
        super().start()

    def stop(self):
        self._running = False
        self.join()

    def run(self) -> None:
        before_minute = datetime.now().minute
        should_retry = False

        while self._running:
            now = datetime.now()
            is_minute_passing = now.minute != before_minute
            should_run = is_minute_passing and self._pipeline.schedule.should_run(now)

            if should_run or should_retry:
                try:
                    self._pipeline.run()
                    should_retry = False
                except Exception:
                    should_retry = True
                    logger.info(f"Pipeline \"{self._pipeline.name}\" has failed. Scheduling to next minute.")

            before_minute = now.minute
            time.sleep(1)
        self._running = False
