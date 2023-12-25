import typing

from PySide6.QtWidgets import (
    QHeaderView,
    QTableView,
)

if typing.TYPE_CHECKING: # silence type check
    QHeaderView.ScrollPerPixel = QTableView.ScrollMode.ScrollPerPixel
    QHeaderView.Interactive = QHeaderView.ResizeMode.Interactive


class DataFrameView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        from .delegate import ChemicalDelegate
        self.delegate = ChemicalDelegate(self)
        self.setItemDelegate(self.delegate)
        self.setWordWrap(True)
        self.setVerticalScrollMode(QHeaderView.ScrollPerPixel)
        self.setHorizontalScrollMode(QHeaderView.ScrollPerPixel)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

    def setModel(self, model):
        super().setModel(model)
        self.resizeToDefault()

    def resizeToDefault(self, row=True, column=True):
        if row:
            self.resizeRowsToContents()
        if column:
            self.resizeColumnsToContents()
