from typing import Optional
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from typing import cast, Optional
from ..dataframe_table import DataFrameModel, DataFrameView, ExtraProperty
import numpy as np
import pandas as pd
from collections.abc import Mapping


class MetfragResultDialog(QDialog):
    def __init__(
        self, model: DataFrameModel, parent: Optional[QWidget] = None, **kwargs
    ) -> None:
        super().__init__(parent, **kwargs)
        self.setWindowTitle("Metfrag Results")
        layout = QVBoxLayout()

        view = DataFrameView()
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)

        layout.addWidget(view)
        layout.addWidget(buttons)

        self.setLayout(layout)

        buttons.accepted.connect(self.accept)
        view.setModel(model)

    @staticmethod
    def fromDataFrame(
        data: pd.DataFrame,
        extra_prop: Optional[dict[str, ExtraProperty]] = None,
        hide_columns: Optional[list[str]] = None,
        only_show_columns: Optional[list[str]] = None,
        column_rename: Mapping[str, str] = None,
        deepcopy: bool = True,
        parent=None,
    ):
        return MetfragResultDialog(
            DataFrameModel(
                data=data,
                extra_prop=extra_prop,
                hide_columns=hide_columns,
                only_show_columns=only_show_columns,
                column_rename=column_rename,
                deepcopy=deepcopy,
            ),
            parent=parent,
        )
