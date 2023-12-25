from types import MappingProxyType
from typing import Any

from PySide6.QtCore import QObject, Signal, SignalInstance

from OPEs_ID.expr import ChemFormula
from OPEs_ID.metfrag import Config as MetfragConfig
from OPEs_ID.tools import TargetIon

_global_default_config: dict[str, Any] = {
    "path.pos_file": "",
    "path.neg_file": "",
    "target_ion.ions": [  # TODO: move to a file
        TargetIon(ChemFormula("PO4H4+"), "P(=O)(-O)(-O)-O", "Alkyl"),
        TargetIon(ChemFormula("C6H8O4P+"), "P(=O)(-O)(-O)-O-c1ccccc1", "Aryl"),
        TargetIon(
            ChemFormula("C12H12O4P+"), "P(=O)(-O)(-O-c1ccccc1)-O-c1ccccc1", "Aryl"
        ),
        TargetIon(
            ChemFormula("C7H10O4P+"),
            "[$(P(=O)(-O)(-O)-O-[$(c1c(-[CH3])cccc1),$(c1cc(-[CH3])ccc1),$(c1ccc(-[CH3])cc1)]),$(P(=O)(-O)(-O-[CH3])-O-c1ccccc1)]",
            "Aryl",
        ),
        TargetIon(
            ChemFormula("C14H16O4P+"),
            "P(=O)(-O)(-O-[$(c1c(-[CH3])cccc1),$(c1cc(-[CH3])ccc1),$(c1ccc(-[CH3])cc1)])-O-[$(c1c(-[CH3])cccc1),$(c1cc(-[CH3])ccc1),$(c1ccc(-[CH3])cc1)]",
            "Aryl",
        ),
        TargetIon(ChemFormula("CH6O4P+"), "P(=O)(-O)(-O)-O-[CH3]", "Alkyl"),
    ],
    "target_ion.mass_acc": 20e-6,
    "ROI.mass_acc": 20e-6,
    "formula.isotope.Cl": "0-10",
    "formula.top_n": 5,
    "formula.mass_acc": 5e-6,
    "formula.element.C12": "0-100",
    "formula.element.H1": "0-200",
    "formula.element.O16": "0-50",
    "formula.element.P31": "1, 2",
    "formula.element.N14": "0",
    "formula.element.DoU": "0-50",
    "app.debug.on": False,
    "app.debug.ui_recompile": False,  # recompile ui file on running
    "metfrag.java_path": MetfragConfig.JAVA_EXE,
    "metfrag.temp_dir": None,
    "metfrag.db_path": "",
    "metfrag.db_type": "PubChem",
    "metfrag.max_tree_depth": 2,
    "metfrag.constraints.fragment": True,
    "metfrag.constraints.ester_type": True,
    "metfrag.n_job": 1,
}

_global_config: dict[str, Any] = _global_default_config.copy()


class UnknownConfigError(KeyError):
    pass


class DictWatcher(QObject):
    opt_names = _global_default_config.keys()
    name_lookup = MappingProxyType(
        {k: v for k, v in zip(opt_names, range(len(opt_names)))}
    )
    loc = locals()
    for i in range(len(_global_default_config)):
        loc[f"__signal_{i}"] = Signal(object)
    del loc, opt_names

    def __init__(self, d: dict[str, Any], parent=None):
        super().__init__(parent=parent)
        self.d = d

    def valueChanged(self, name: str) -> SignalInstance:
        i = self.name_lookup[name]
        return getattr(self, f"__signal_{i}")

    def __getitem__(self, key: str) -> Any:
        try:
            return self.d[key]
        except KeyError:
            collects = {}
            for k, v in self.d.items():
                if k.startswith(key):
                    k = k.removeprefix(key)
                    if k[0] == ".":
                        collects[k[1:]] = v
            if len(collects) == 0:
                raise UnknownConfigError()
            else:
                return collects

    def __setitem__(self, key: str, value: Any) -> Any:
        try:
            v = self.d[key]
            if v != value:
                self.d[key] = value
                self.valueChanged(key).emit(value)
        except KeyError as e:
            if isinstance(value, dict):
                if all((f"{key}.{k}" in self.d) for k in value.keys()):
                    for k, v in value.items():
                        self[f"{key}.{k}"] = v
                    return
            raise

    def infoEveryone(self):
        for name, value in self.d.items():
            self.valueChanged(name).emit(value)


config = DictWatcher(_global_config)
