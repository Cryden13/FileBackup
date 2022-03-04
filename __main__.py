from winnotify import InputDialog as InDlg
from concurrent.futures import ThreadPoolExecutor

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
    ans = InDlg.multiinput(
        title="Running Backup",
        message="Select archives to update:",
        input_fields=[(f.stem, InDlg.ChWgt.checkbox(default=True))
                      for f in all_files]
    )
    if ans:
        files = [f for f in all_files if ans.get(f.stem)]
        with ThreadPoolExecutor(max_workers=THREADS) as ex:
            ex.map(backup, files)
    EXCLUDE.unlink()


if __name__ == "__main__":
    main()
