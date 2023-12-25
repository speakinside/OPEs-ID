from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import Signal
from pathlib import Path

from ..config import config as CONFIG
from .MetfragConfigDialog_ui import Ui_Dialog as Ui_MetfragConfigDialog

from typing import Any


class MetfragConfigDialog(QDialog):
    def __init__(self, configs: dict[str, Any] = None, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_MetfragConfigDialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Before Metfrag")

        def setJavaPath():
            fpath, _ = QFileDialog.getOpenFileName(
                self, "Select Java exe.", ".", "JAVA exe (*.exe)"
            )
            if fpath:
                self.ui.javaPathEdit.setText(fpath)

        def downloadJava():
            import webbrowser

            webbrowser.open("https://learn.microsoft.com/zh-cn/java/openjdk/download")

        self.ui.selectJavaPathButton.clicked.connect(setJavaPath)
        self.ui.downloadJavaButton.clicked.connect(downloadJava)

        def enableSysTempDir(enable: bool):
            self.ui.tempDirPath.setEnabled(not enable)
            self.ui.tempDirButton.setEnabled(not enable)

        def setTempDir():
            dirpath = QFileDialog.getExistingDirectory(self, "Select Temp Dir")
            if dirpath:
                self.ui.tempDirPath.setText(str(Path(dirpath) / "temp"))

        self.ui.sysTempDirCheckBox.toggled.connect(enableSysTempDir)
        self.ui.tempDirButton.clicked.connect(setTempDir)
        self.ui.sysTempDirCheckBox.setChecked(True)

        # DATABASE
        def showDbExtraInfoWidget(text):
            if text in ["LocalCSV", "LocalSDF"]:
                self.ui.dbExtraInfoWidget.setVisible(True)
            else:
                self.ui.dbExtraInfoWidget.setVisible(False)

        def setDbPath():
            fpath = None
            if self.ui.dbComboBox.currentText() == "LocalSDF":
                fpath, _ = QFileDialog.getOpenFileName(
                    self, "Select SDF File.", ".", "SDF (*.sdf)"
                )
            elif self.ui.dbComboBox.currentText() == "LocalCSV":
                fpath, _ = QFileDialog.getOpenFileName(
                    self, "Select CSV File.", ".", "CSV (*.csv)"
                )
            if fpath:
                self.ui.dbPathEdit.setText(fpath)

        self.ui.dbComboBox.addItems(["LocalCSV", "PubChem", "LocalSDF"])
        self.ui.dbComboBox.currentTextChanged.connect(showDbExtraInfoWidget)
        self.ui.selectDBPathButton.clicked.connect(setDbPath)
        self.ui.dbComboBox.setCurrentText("PubChem")

        # METFRAG CONFIG
        if configs is not None:
            self.set_config(configs)

    def configs(self):
        if self.ui.sysTempDirCheckBox.isChecked():
            tempdir = None
        else:
            tempdir = Path(self.ui.tempDirPath.text())
        return {
            "java_path": Path(self.ui.javaPathEdit.text()),
            "temp_dir": tempdir,
            "db_type": self.ui.dbComboBox.currentText(),
            "db_path": Path(self.ui.dbPathEdit.text()),
            "max_tree_depth": self.ui.maxTreeDepthSpinBox.value(),
            "constraints.fragment": self.ui.filterTargetIonCheckBox.isChecked(),
            "constraints.ester_type": self.ui.filterEsterTypeCheckBox.isChecked(),
            "n_job": self.ui.nJobSpinBox.value(),
        }

    def set_config(self, config: dict):
        self.ui.javaPathEdit.setText(str(config["java_path"]))
        tempdir = config["temp_dir"]
        if tempdir is None:
            self.ui.sysTempDirCheckBox.setChecked(True)
        else:
            self.ui.sysTempDirCheckBox.setChecked(False)
        self.ui.tempDirPath.setText(str(tempdir))
        self.ui.dbComboBox.setCurrentText(
            config.get("db_type", self.ui.dbComboBox.currentText())
        )
        self.ui.dbPathEdit.setText(str(config["db_path"]))
        self.ui.maxTreeDepthSpinBox.setValue(
            config.get("max_tree_depth", self.ui.maxTreeDepthSpinBox.value())
        )
        self.ui.filterTargetIonCheckBox.setChecked(
            config.get(
                "constraints.fragment", self.ui.filterTargetIonCheckBox.isChecked()
            )
        )
        self.ui.filterEsterTypeCheckBox.setChecked(
            config.get(
                "constraints.ester_type", self.ui.filterEsterTypeCheckBox.isChecked()
            )
        )
        self.ui.nJobSpinBox.setValue(config.get("n_job", self.ui.nJobSpinBox.value()))
