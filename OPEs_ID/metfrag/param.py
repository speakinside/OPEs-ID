import dataclasses
import enum
import io
import types
from collections.abc import Sequence, Collection
from pathlib import Path
from typing import Optional
from typing import Union, Literal, TypeAlias

try:
    from enum import StrEnum
except ImportError:

    class StrEnum(str, enum.Enum):
        def __str__(self) -> str:
            return self.value.__str__()

        def __format__(self, format_spec: str) -> str:
            return self.value.__format__(format_spec)


class MetfragParameterError(ValueError):
    pass

MetFragDatabaseTypeEnum: TypeAlias = Literal["PubChem", "LocalCSV", "LocalSDF"]

MetFragCandidateWriter: TypeAlias = Literal[
    "SDF", "XLS", "CSV", "ExtendedXLS", "ExtendedFragmentsXLS"
]


class MetFragPreProcessingCandidateFilter(StrEnum):
    UnconnectedCompoundFilter = "UnconnectedCompoundFilter"
    SmartsSubstructureInclusionFilter = "SmartsSubstructureInclusionFilter"
    SmartsSubstructureExclusionFilter = "SmartsSubstructureExclusionFilter"


class MetFragPostProcessingCandidateFilter(StrEnum):
    InChIKeyFilter = "InChIKeyFilter"


_PrecursorIonMode = {
    # positive (IsPositiveIonMode = True)
    "[M+H]+": 1,
    "[M+NH4]+": 18,
    "[M+Na]+": 23,
    "[M+K]+": 39,
    "[M+CH3OH+H]+": 33,
    "[M+ACN+H]+": 42,
    "[M+ACN+Na]+": 64,
    "[M+2ACN+H]+": 83,
    # negative (IsPositiveIonMode = False)
    "[M-H]-": -1,
    "[M+Cl]-": 35,
    "[M+HCOO]-": 45,
    "[M+CH3COO]-": 59,
    # no adduct (IsPositiveIonMode = True/False)
    "[M]+/-": 0,
}

PrecursorIonMode = types.MappingProxyType(_PrecursorIonMode)


@dataclasses.dataclass(slots=True)
class MetFragParameter:
    _: dataclasses.KW_ONLY  # Everything is Keyword Only

    # data file containing mz intensity peak pairs (one per line)
    PeakListPath: str = None
    PeakListString: str = None
    MetFragPeakListReader: str = (
        "de.ipbhalle.metfraglib.peaklistreader.FilteredStringTandemMassPeakListReader"
    )
    # database parameters -> how to retrieve candidates
    MetFragDatabaseType: MetFragDatabaseTypeEnum | str = "PubChem"  # LocalSDF
    LocalDatabasePath: Optional[Path | str] = None
    NeutralPrecursorMolecularFormula: str = None
    DatabaseSearchRelativeMassDeviation: float = None
    NeutralPrecursorMass: Optional[float] = None
    IonizedPrecursorMass: Optional[float] = None

    # peak matching parameters
    FragmentPeakMatchAbsoluteMassDeviation: float = 0.001
    FragmentPeakMatchRelativeMassDeviation: float = 5  # ppm
    PrecursorIonMode: int | str = 1  # [M+H]+:1 [M-H]-:-1
    IsPositiveIonMode: bool | None = True

    # scoring parameters
    MetFragScoreTypes: str = "FragmenterScore"
    MetFragScoreWeights: Sequence[float] | float = 1.0

    # output SDF, XLS, CSV, ExtendedXLS, ExtendedFragmentsXLS
    MetFragCandidateWriter: Union[MetFragCandidateWriter, str] = "CSV"
    SampleName: str = None
    ResultsPath: str = None

    # following parameteres can be kept as they are
    MaximumTreeDepth: int = 2
    FilterSmartsInclusionList: Optional[Sequence[str] | str] = None
    FilterSmartsExclusionList: Optional[Sequence[str] | str] = None

    MetFragPreProcessingCandidateFilter: Sequence[
                                             str
                                         ] | str = "UnconnectedCompoundFilter"
    MetFragPostProcessingCandidateFilter: Sequence[str] | str = "InChIKeyFilter"
    NumberThreads: int | None = None
    BondEnergyFilePath: str = None
    # internal param
    m_ParamSavePath: Optional[str] = None  # TODO
    # dfidjjfs

    m_ExtraAttrs: dict = dataclasses.field(default_factory=dict)

    def dumps(self, cmd=False):
        entries = []
        for field in dataclasses.fields(self):
            name = field.name
            if name.startswith("m"):  # internal param
                continue  # jump
            value = getattr(self, name)
            match name:
                case "IsPositiveIonMode":
                    if value is None:
                        value = "True/False"
                    else:
                        value = str(value)
                case "PeakListString":
                    if (value is not None) and (self.PeakListPath is not None):
                        raise ValueError(
                            "PeakListString and PeakListPath are both set."
                        )
                case "PrecursorIonMode":
                    if isinstance(value, int):
                        if value not in PrecursorIonMode.values():
                            raise ValueError()
                    elif isinstance(value, str):
                        value = PrecursorIonMode[value]
                case _:
                    if value is None:
                        continue
            if isinstance(value, Collection) and not isinstance(value, str):
                value = ",".join(value)

            if cmd:
                entries.append(f"{name}={value}")
            else:
                entries.append(f"{name} = {value}")
        join_str = " " if cmd else "\n"
        return join_str.join(entries)

    def dump(self, fp):
        if isinstance(fp, io.TextIOBase):
            fp.write(self.dumps())
        else:
            fp = Path(fp)
            fp.parent.mkdir(parents=True, exist_ok=True)
            with open(fp, "w") as f:
                f.write(self.dumps())

    def validate(self):
        pass

    def copy(self):
        import copy

        return copy.deepcopy(self)
