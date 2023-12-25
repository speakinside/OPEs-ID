from typing import Protocol
from PySide6.QtCore import Signal


class WorkerType(Protocol):
    progressUpdate: Signal


class ProgressAdaptor:
    def __init__(self, worker: WorkerType, progress_id: str, start: int, end: int):
        self.worker = worker
        self.progress_id = progress_id
        self.start = start
        self.end = end

    def __call__(self, iterable, total=None):
        if total is None:
            try:
                total = len(iterable)
            except:
                pass
        length = self.end - self.start
        for idx, obj in enumerate(iterable):
            if total is not None:
                self.worker.progressUpdate.emit(
                    self.progress_id, round((idx + 1) / total * length + self.start)
                )
            yield obj
        else:
            self.worker.progressUpdate.emit(self.progress_id, self.end)
