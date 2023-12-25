from PySide6.QtCore import QThread, Signal
import io
import traceback
from OPEs_ID.metfrag import MetFragParameter, AsyncMetFragPool
from .progress_adaptor import ProgressAdaptor


class MetfragThread(QThread):

    calculationFinished = Signal(bool, arguments=["isSuccess"])
    progressUpdate = Signal(str, int, arguments=["id", "value"])

    def __init__(self, params:list[MetFragParameter], n_jobs=1, parent = None) -> None:
        super().__init__(parent)
        self.results = None
        self.params = params
        self.n_jobs = n_jobs

    def run(self) -> None:
        try:
            pool = AsyncMetFragPool(self.n_jobs, progress=ProgressAdaptor(self, "metfrag", 0, 100))
            self.results = pool(self.params)
            self.calculationFinished.emit(True)
        except:
            error_msg = io.StringIO()
            traceback.print_exc()
            traceback.print_exc(file=error_msg)
            self.calculationFinished.emit(False)