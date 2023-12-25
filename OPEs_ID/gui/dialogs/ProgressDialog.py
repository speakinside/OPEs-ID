from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QDialog, QWidget, QProgressBar, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLabel


class SingleProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.descriptionLabel = QLabel("Progress 1", self)
        self.progressBar = QProgressBar(self)

        # self.descriptionLabel.setAlignment(Qt.AlignHCenter)
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)

        layout = QHBoxLayout()
        layout.addWidget(self.descriptionLabel)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)

    def sizeHint(self):
        return super().sizeHint() + QSize(150, 0)

    @property
    def description(self):
        return self.descriptionLabel.text()

    @description.setter
    def description(self, text: str):
        self.descriptionLabel.setText(text)

    @property
    def value(self):
        return self.progressBar.value()

    @value.setter
    def value(self, v: int):
        self.progressBar.setValue(v)


class ProgressDialog(QDialog):
    cancelClicked = Signal()

    def __init__(
            self, n_prog: int | list, parent: QWidget | None = None, f: Qt.WindowType = Qt.WindowFlags()
    ) -> None:
        super().__init__(parent, f)
        self.setWindowTitle("Calculation Running")
        layout = QVBoxLayout()
        if isinstance(n_prog, int):
            n_prog = range(n_prog)
        self.progressBars = {id_: SingleProgressBar(self) for id_ in n_prog}
        self.dialogButtons = QDialogButtonBox(
            QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        self.dialogButtons.setCenterButtons(True)

        for p in self.progressBars.values():
            layout.addWidget(p)
        layout.addWidget(self.dialogButtons)
        self.setLayout(layout)

        self.dialogButtons.rejected.connect(self.cancel)

    def updateProgress(self, id_, progress_value: int):
        self.progressBars[id_].value = progress_value

    def updateDescription(self, id_, description: str):
        self.progressBars[id_].description = description

    def cancel(self):
        self.cancelClicked.emit()

    def closeEvent(self, event) -> None:
        self.cancelClicked.emit()
        return super().closeEvent(event)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    sys.excepthook = exception_hook
    qApp = QApplication(sys.argv)
    win = ProgressDialog(5)
    win.show()
    sys.exit(qApp.exec())
