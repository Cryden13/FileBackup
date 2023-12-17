from win32process import GetWindowThreadProcessId
from pathlib import Path
from time import sleep

from win32gui import (
    GetWindowRect,
    FindWindowEx,
    MoveWindow
)

from commandline import RunCmd

from .variables import *


def getPSCmds(ttl: str) -> tuple[str, str]:
    start = f'$host.UI.RawUI.WindowTitle = "{ttl}"'
    playSd = "[system.media.systemsounds]::Beep.play()"
    endMsg = ('Write-Host "Closing in 30 secs, or press <Return> to exit immediately"; '
              '$counter = 0; '
              'while(!$Host.UI.RawUI.KeyAvailable -and ($counter++ -lt 30)) { [Threading.Thread]::Sleep(1000) }')
    end = f"{playSd}; {endMsg}"
    return (start, end)


def backup(arch_pth: Path, tot_ct: int, cur_ct: int):
    if not arch_pth.parent.exists():
        raise FileNotFoundError(f'"{arch_pth}" could not be found.')
    pth_f = Path(__file__).with_name(f'{arch_pth.stem.replace(" ", "")}.txt')
    pth_f.write_text("\n".join(BACKUPS.get(arch_pth)))
    cmd = (f'7z {"u" if arch_pth.exists() else "a"} -slp -t7z -mx{COMP_LVL} '
           f'{"-up0q0" if arch_pth.exists() else ""} -i@"{pth_f}" -xr@"{EXCLUDE}" "{arch_pth}"')
    win_ttl = (f"({cur_ct+1} of {tot_ct}) "
               f"Updating/Adding to <{arch_pth.name}>")
    start, end = getPSCmds(win_ttl)
    shell = RunCmd(
        ["powershell", "-command", f"{start}; {cmd}; {end}"],
        console="new",
        cwd="C:\\Windows\\System32",
    )
    # move powershell window
    loop = 0
    pid = 0
    while loop < 50 and pid != shell.pid:
        sleep(0.1)
        hwnd = FindWindowEx(None, None, None, win_ttl)
        pid = GetWindowThreadProcessId(hwnd)[1]
        loop += 1
    if loop < 50:
        # if win was found, move it
        x, y, xw, yh = GetWindowRect(hwnd)
        dx = x + MOVE_BY
        w = xw - x
        h = yh - y
        MoveWindow(hwnd, dx, y, w, h, True)
    # wait then close
    shell.wait()
    pth_f.unlink()


# 7zip command line notes (https://documentation.help/7-Zip/syntax.htm)
# 7z <command> <switches> <base_archive_name> <@{list_filename}>
#
# u         update command
# a         add command
# -slp      enables large pages mode
# -t        type of archive switch
#   7z        7z format
# -m        method switch
#   x[n]      sets level of compression to n (n = 0|1|3|5|7|9)
# -u        update switch
#   p0        don't copy archive items that don't match wildcard
#   q0        don't copy archive items that no longer exist
# -x        exclude switch
#   r@[f]     recursively exclude files/folders listed in file f
# -i        include switch
#   @[f]      include files/folders listed in file f
