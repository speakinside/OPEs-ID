import shutil
from pathlib import Path
from typing import Optional


FILE_DIR = Path(__file__).parent
DEFAULT_JAVA = FILE_DIR / "jdk" / "bin" / "java.exe"


class JavaNotFound(RuntimeError):
    pass


def _init_java_path() -> Optional[Path]:
    if DEFAULT_JAVA.exists():
        return DEFAULT_JAVA
    elif (java_path := shutil.which("java")) is not None:
        return Path(java_path)
    else:
        return None


class RuntimeConfig:
    METFRAG_EXE: Path = Path(__file__).parent / "MetFragCommandLine-2.5.0_comma.jar"
    JAVA_EXE: Optional[Path] = _init_java_path()

    @classmethod
    def set_java_exe(cls, path):
        cls.JAVA_EXE = Path(path)

    @classmethod
    def get_java_exe(cls):
        if cls.JAVA_EXE is None:
            raise JavaNotFound(
                f"Metfrag needs java to run. You can use `OPEs_ID.metfrag.Config.set_java_exe` to manually set the `java.exe` path."
            )
        return cls.JAVA_EXE

    @classmethod
    def get_metfrag_path(cls):
        return cls.METFRAG_EXE
