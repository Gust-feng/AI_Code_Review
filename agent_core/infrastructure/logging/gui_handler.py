"""GUI logging handler for live log viewer."""

from __future__ import annotations

import logging
from queue import Queue
from typing import Optional

from .logger import JsonFormatter


class GuiLogHandler(logging.Handler):
    """Logging handler that pushes JSON-formatted records to a queue."""

    def __init__(self) -> None:
        super().__init__(level=logging.INFO)
        self.queue: "Queue[str]" = Queue()
        self.setFormatter(JsonFormatter(pretty=True))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = self.format(record)
        except Exception:  # pragma: no cover - defensive
            self.handleError(record)
            return
        self.queue.put(message)

    def get_queue(self) -> "Queue[str]":
        return self.queue
