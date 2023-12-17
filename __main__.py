from PyQt5.QtWidgets import QApplication
from sys import argv

try:
    from .src import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit


def main():
    all_files = list(BACKUPS.keys())
    _ = QApplication(argv)
    ans = InputDialog(all_files).out
    files = [f for f in all_files if f in ans]
    for i, file in enumerate(files):
        backup(file, len(files), i)
    EXCLUDE.unlink()


if __name__ == "__main__":
    main()
