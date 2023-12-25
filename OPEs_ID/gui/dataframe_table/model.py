import contextlib
import copy
import enum
from collections.abc import Mapping
from dataclasses import fields
from typing import Annotated, Any
from typing import Optional

import numpy as np
import pandas as pd
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt
from rdkit import Chem

from OPEs_ID.expr import ChemFormula


class ExtraProperty(enum.IntEnum):
    Normal = enum.auto()
    ChemicalFormula = enum.auto()
    MolSVG = enum.auto()
    MetfragResult = enum.auto()


class MyRole(enum.IntEnum):
    ExtraPropertyRole = Qt.UserRole + 1000
    ChemicalFormulaRole = enum.auto()
    RDkitMolRole = enum.auto()
    MetfragResultRole = enum.auto()


def is_same_dataclass(data: list[object]):
    return len(set(d.__class__.__qualname__ for d in data)) == 1


class DataFrameModel(QAbstractTableModel):
    def __init__(
        self,
        data: pd.DataFrame,
        extra_prop: Optional[dict[str, ExtraProperty]] = None,
        hide_columns: Optional[list[str]] = None,
        only_show_columns: Optional[list[str]] = None,
        column_rename: Mapping = None,
        deepcopy: bool = True,
        parent=None,
    ) -> None:
        if hide_columns is not None and only_show_columns is not None:
            raise ValueError()
        if deepcopy:
            self._data = data.copy(deep=True)
        else:
            self._data = data.copy(deep=False)

        self._hide_columns = hide_columns
        self._only_show_columns = only_show_columns
        self._column_rename = column_rename if column_rename else {}
        self._extra_prop = extra_prop if extra_prop else {}

        super().__init__(parent=parent)

    @property
    def columns_visible(self) -> list[str]:
        if self._only_show_columns is not None:
            return self._only_show_columns
        else:
            sel = np.isin(self._data.columns, self._hide_columns)
            return self._data.columns[~sel].tolist()

    def index2colName(self, idx):
        return self.columns_visible[idx]

    def colName2index(self, name):
        return self.columns_visible.index(name)

    def headerData(self, section, orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                label = self.index2colName(section)
                if self._column_rename is not None:
                    label = self._column_rename.get(label, label)
                return label
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=QModelIndex()):
        return self._data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns_visible)

    def _get_data(self, rowNum: int, colNum: int):
        return self._data.at[self._data.index[rowNum], self.index2colName(colNum)]

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.DisplayRole
    ):
        if index.isValid():
            row, col = index.row(), index.column()
            match role:
                case Qt.DisplayRole:
                    if index.data(MyRole.ExtraPropertyRole) == ExtraProperty.MetfragResult:
                        return index.data(MyRole.MetfragResultRole)
                    return str(self._get_data(row, col))
                case MyRole.ExtraPropertyRole:
                    return self._extra_prop.get(
                        self.index2colName(col), ExtraProperty.Normal
                    )
                case MyRole.ChemicalFormulaRole:
                    data = self._get_data(row, col)
                    if isinstance(data, ChemFormula):
                        return data
                    else:
                        return None
                case MyRole.RDkitMolRole:
                    mol_source: str = self._get_data(row, col)
                    if mol_source.startswith("InChI"):
                        return Chem.MolFromInchi(mol_source)
                    else:
                        return Chem.MolFromSmiles(mol_source)
                case MyRole.MetfragResultRole:
                    data = self._get_data(row, col)
                    if isinstance(data, pd.DataFrame):
                        return str(data.shape[0])
                    else:
                        return "error"
                case _:
                    pass
        return None

    @contextlib.contextmanager
    def resetModelContext(self):
        self.beginResetModel()
        yield self
        self.endResetModel()

    def add_column(
        self,
        col_name: str,
        value,
        extra_property: ExtraProperty = None,
        column_rename: str = None,
        hide=False,
    ):
        with self.resetModelContext():
            if col_name in self._data.columns:
                self._data[col_name] = value
            else:
                self._data.insert(self._data.columns.size, col_name, value)
            if extra_property is not None:
                self._extra_prop[col_name] = extra_property
            if column_rename is not None:
                self._column_rename[col_name] = column_rename
            if hide:
                if self._hide_columns is None:
                    self._hide_columns = [col_name]
                else:
                    self._hide_columns.append(col_name)


class DataclassModel(QAbstractTableModel):
    def __init__(
        self,
        data: list[Annotated[Any, "dataclass"]],
        extra_prop: Optional[dict[str, ExtraProperty]] = None,
        hide_columns: Optional[list[str]] = None,
        show_columns: Optional[list[str]] = None,
        fields_rename: Mapping = None,
        deepcopy: bool = True,
        parent=None,
    ) -> None:
        super().__init__(parent=parent)
        if not is_same_dataclass(data):
            raise ValueError()

        if deepcopy:
            self._data = copy.deepcopy(data)
        else:
            self._data = data
        self._fields = [f.name for f in fields(self._data[0])]
        self._hide_columns = hide_columns  # TODO
        self._show_columns = show_columns  # TODO
        self._fields_rename = fields_rename
        self._extra_prop = extra_prop if extra_prop else {}

    def headerData(self, section, orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                label = self._fields[section]
                if self._fields_rename is not None:
                    label = self._fields_rename.get(label, label)
                return label
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._fields)

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.DisplayRole
    ):
        if index.isValid():
            row, col = index.row(), index.column()
            match role:
                case Qt.DisplayRole:
                    return str(getattr(self._data[row], self._fields[col]))
                case MyRole.ExtraPropertyRole:
                    return self._extra_prop.get(self._fields[col], ExtraProperty.Normal)
                case MyRole.ChemicalFormulaRole:
                    data = getattr(self._data[row], self._fields[col])
                    if isinstance(data, ChemFormula):
                        return data
                    else:
                        return None
                case MyRole.RDkitMolRole:
                    mol_source: str = getattr(self._data[row], self._fields[col])
                    if mol_source.startswith("InChI"):
                        return Chem.MolFromInchi(mol_source)
                    else:
                        return Chem.MolFromSmiles(mol_source)
                case _:
                    pass
        return None
