from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QTabWidget, QDialog

from .ConfigPage import ConfigPage
from .ResultPage import ResultPage
from ..calc.worker import CalcWorker


class AppMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("OPEs-ID")
        
        self.worker = CalcWorker()
        self.resize(720, 600)

        self.tabWidget = QTabWidget(parent)
        self.setCentralWidget(self.tabWidget)

        self.topMenuBar = self.menuBar()
        self.bottomStatusBar = self.statusBar()

        self.configPage = ConfigPage(self)
        self.resultPage = ResultPage(self)

        self.tabWidget.addTab(self.configPage, self.tr("Configuration"))
        self.tabWidget.addTab(self.resultPage, self.tr("Result"))

        self.configPage.startCalculation.connect(self.startCal)

    def startCal(self):
        from ..dialogs.ProgressDialog import ProgressDialog

        prog_dialog = ProgressDialog(["data_load", "ms2_screen", "roi", "cl", "formula", "tri-ester"], self)
        prog_dialog.updateDescription("data_load", "Load Data")
        prog_dialog.updateDescription("ms2_screen", "Search OPE fragments ")
        prog_dialog.updateDescription("roi", "Group ROI")
        prog_dialog.updateDescription("cl", "Identify Cl isotopes")
        prog_dialog.updateDescription("formula", "Predict chemical formula")
        prog_dialog.updateDescription("tri-ester", "Compare neg & pos EIC")

        self.worker.progressUpdate.connect(prog_dialog.updateProgress)

        thread = QThread(self)
        self.worker.moveToThread(thread)
        thread.started.connect(self.worker.startCalc)
        #thread.finished.connect(thread.deleteLater)
        thread.start()

        self.worker.calculationFinished.connect(prog_dialog.accept)
        if prog_dialog.exec() == QDialog.Accepted:
            self.resultPage.setGeneralResult(self.worker.output1_results)
            self.tabWidget.setCurrentIndex(1)
