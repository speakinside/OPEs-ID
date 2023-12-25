from OPEs_ID.defines import ColumnNames as OriginalColumnNames
from enum import StrEnum
import enum
import types
from typing import TYPE_CHECKING

@enum.unique
class ExtendedColumnNames(StrEnum):
    MetfragResults = "MetfragResults"
    MetfragParams = "MetfragParams"

def update_clsdict(clsdict):
    d = OriginalColumnNames.__members__ | ExtendedColumnNames.__members__

    if len(d) != len(OriginalColumnNames) + len(ExtendedColumnNames):
        raise ValueError()

    for n, v in d.items():
        clsdict[n] = str(v)

    def __repr__(self):
        return repr(str(self))

    clsdict["__repr__"] = str.__repr__
if TYPE_CHECKING:
    class ColumnNames(OriginalColumnNames, ExtendedColumnNames):
        ...

else:
    ColumnNames = enum.unique(
        types.new_class("ExtendedVarName", (StrEnum,), exec_body=update_clsdict)
    )
