from pathlib import Path

from PySide6.QtCore import QRegularExpression, Qt, Signal
from PySide6.QtGui import QDoubleValidator, QRegularExpressionValidator, QIntValidator
from PySide6.QtWidgets import QWidget, QFileDialog, QDialog, QDialogButtonBox, QLineEdit, QLabel, QGridLayout

from .ConfigPage_ui import Ui_ConfigPage
from ..config import config as CONFIG


class ConfigPage(QWidget):
    startCalculation = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConfigPage()
        self.ui.setupUi(self)

        # set init
        self.ui.ms2FilterAccLineEdit.setText(str(CONFIG["target_ion.mass_acc"]))
        self.ui.ROIAccLineEdit.setText(str(CONFIG["ROI.mass_acc"]))
        self.ui.IsoClRangeLineEdit.setText(str(CONFIG["formula.isotope.Cl"]))
        self.ui.IsoTopNLineEdit.setText(str(CONFIG["formula.top_n"]))
        self.ui.IsoMassAccLineEdit.setText(str(CONFIG["formula.mass_acc"]))
        # set init end

        self.connect_config()

        self.ui.ms2FilterAccLineEdit.setValidator(QDoubleValidator(self))
        self.ui.ROIAccLineEdit.setValidator(QDoubleValidator(self))
        validator = QRegularExpressionValidator(QRegularExpression(r"\d+-\d+"), self)
        self.ui.IsoClRangeLineEdit.setValidator(validator)
        self.ui.IsoTopNLineEdit.setValidator(QIntValidator(1, 1000, self))
        self.ui.IsoMassAccLineEdit.setValidator(QDoubleValidator(0, 1, 100, self))

        self.ui.selectPosPath.clicked.connect(self.selectPosPath)
        self.ui.selectNegPath.clicked.connect(self.selectNegPath)

        self.ui.formulaConfigButton.clicked.connect(self.showFormulaConfig)

        from ..dataframe_table import DataclassModel, ExtraProperty
        self.target_ion_model = DataclassModel(CONFIG["target_ion.ions"],
                                               extra_prop={"formula": ExtraProperty.ChemicalFormula})
        self.ui.targetIonTableView.setModel(self.target_ion_model)
        self.ui.targetIonTableView.resizeToDefault()

        self.ui.calButton.clicked.connect(lambda: self.startCalculation.emit())

    def connect_config(self):

        CONFIG.valueChanged("path.pos_file").connect(lambda s: self.ui.posFilePath.setText(str(s)))
        CONFIG.valueChanged("path.neg_file").connect(lambda s: self.ui.negFilePath.setText(str(s)))

        CONFIG.valueChanged("target_ion.mass_acc").connect(lambda s: self.ui.ms2FilterAccLineEdit.setText(str(s)))
        CONFIG.valueChanged("ROI.mass_acc").connect(lambda s: self.ui.ROIAccLineEdit.setText(str(s)))

        CONFIG.valueChanged("formula.isotope.Cl").connect(lambda s: self.ui.IsoClRangeLineEdit.setText(str(s)))
        CONFIG.valueChanged("formula.top_n").connect(lambda s: self.ui.IsoTopNLineEdit.setText(str(s)))

        CONFIG.valueChanged("formula.mass_acc").connect(lambda s: self.ui.IsoMassAccLineEdit.setText(str(s)))

        def setValueWrapper(dic, name):
            def func(v):
                dic[name] = v

            return func

        self.ui.posFilePath.textChanged.connect(setValueWrapper(CONFIG, "path.pos_file"))
        self.ui.negFilePath.textChanged.connect(setValueWrapper(CONFIG, "path.neg_file"))

        self.ui.ms2FilterAccLineEdit.textChanged.connect(setValueWrapper(CONFIG, "target_ion.mass_acc"))
        self.ui.ROIAccLineEdit.textChanged.connect(setValueWrapper(CONFIG, "ROI.mass_acc"))

        self.ui.IsoClRangeLineEdit.textChanged.connect(setValueWrapper(CONFIG, "formula.isotope.Cl"))
        self.ui.IsoTopNLineEdit.textChanged.connect(setValueWrapper(CONFIG, "formula.top_n"))

        self.ui.IsoMassAccLineEdit.textChanged.connect(setValueWrapper(CONFIG, "formula.mass_acc"))

    def selectPosPath(self):
        fileName, _ = QFileDialog.getOpenFileName(self, self.tr("Select Pos File"), ".", "MZml (*.MZml)")
        if fileName:
            CONFIG["path.pos_file"] = Path(fileName)

    def selectNegPath(self):
        fileName, _ = QFileDialog.getOpenFileName(self, self.tr("Select Neg File"), ".", "MZml (*.MZml)")
        if fileName:
            CONFIG["path.neg_file"] = Path(fileName)

    def showFormulaConfig(self):
        global CONFIG

        prefix = "formula.element"
        dialog = FormulaConfigDialog(CONFIG[prefix], self)

        def onAccepted():
            for k, v in dialog.getConfig().items():
                CONFIG[f"{prefix}.{k}"] = v

        dialog.accepted.connect(onAccepted)
        dialog.open()


class FormulaConfigDialog(QDialog):

    def __init__(self, config: dict[str, str], parent=None, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.config = config

        self.buttonGroups = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        self.buttonGroups.accepted.connect(self.accept)
        self.buttonGroups.rejected.connect(self.reject)
        layout = QGridLayout()
        self.lineEdits: dict[str, QLineEdit] = {}
        idx = 0
        for idx, (name, value) in enumerate(config.items()):
            layout.addWidget(QLabel(name + ":"), idx, 0)
            lineEdit = QLineEdit(value, self)
            self.lineEdits[name] = lineEdit
            layout.addWidget(lineEdit, idx, 1)
        layout.addWidget(self.buttonGroups, idx + 1, 0, 1, 2)
        self.setLayout(layout)

    def getConfig(self):
        return {name: edit.text() for name, edit in self.lineEdits.items()}
