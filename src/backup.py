from commandline import RunCmd
from pathlib import Path
from .variables import *


def getPSCmds(fname: str) -> tuple[str, str]:
    conTtl = f'$host.UI.RawUI.WindowTitle = "Adding to <{fname}>"'
    playSd = '[system.media.systemsounds]::Beep.play()'
    endMsg = 'Read-Host "Press <Return> to exit"'
    start = f'{conTtl}; '
    end = '; '.join([playSd, endMsg])
    return (start, end)


def backup(bck_to: Path):
    if not bck_to.parent.exists():
        raise FileNotFoundError(f'"{bck_to}" could not be found.')
    pth_f = Path(f'{bck_to.stem.replace(" ", "")}.txt')
    pth_f.write_text('\n'.join(BACKUPS.get(bck_to)))
    cmd = (f'7z a -t7z -mmt2 -mx7 -up0 -uq0 -ux1 -uz1 '
           f'"{bck_to}" \'@{pth_f}\' \'-xr@{EXCLUDE}\'; ')
    start, end = getPSCmds(bck_to.name)
    RunCmd(['powershell', '-command', start + cmd + end],
           console='new').wait()
    pth_f.unlink()


# 7zip command line notes (https://sevenzip.osdn.jp/chm/cmdline/)
#
# a         add
# -t7z      7z format
# -mmt2     2 threads
# -mx7      compression 7 (1|3|5|7|9, def=5)
# -up0      remove archive items that don't match wildcard
# -uq0      remove archive items that no longer exist
# -ux1      keep archive items that have newer date
# -uz1      keep archive items that have same date
# -xr@      recursively exclude files/folders listed in {Path}
