try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    raise ImportError("GUI needs PySide6 installed.")

from .config import config

if config["app.debug.on"] and config["app.debug.ui_recompile"]:
    from pathlib import Path
    import subprocess

    dirpath = Path(__file__).parent
    ui_files = []
    for root, _, files in dirpath.walk(on_error=print, follow_symlinks=False):
        for file in files:
            if file.endswith(".ui"):
                ui_files.append(root / file)

    for p in ui_files:
        subprocess.run(["pyside6-uic.exe", p, "-o", p.with_name(f"{p.stem}_ui.py")])

from .app_mainwindow import AppMainWindow


def main():
    import sys
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook
    qApp = QApplication(sys.argv)
    win = AppMainWindow()

    win.show()
    sys.exit(qApp.exec())
