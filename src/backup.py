from commandline import RunCmd
from pathlib import Path
from .variables import *


def getPSCmds(fname: str) -> tuple[str, str]:
    conTtl = f'$host.UI.RawUI.WindowTitle = "Updating/Adding to <{fname}>"'
    playSd = '[system.media.systemsounds]::Beep.play()'
    endMsg = 'Read-Host "Press <Return> to exit"'
    start = f'{conTtl}'
    end = f'{playSd}; {endMsg}'
    return (start, end)


def backup(arch_pth: Path):
    if not arch_pth.parent.exists():
        raise FileNotFoundError(f'"{arch_pth}" could not be found.')
    pth_f = Path(f'{arch_pth.stem.replace(" ", "")}.txt')
    pth_f.write_text('\n'.join(BACKUPS.get(arch_pth)))
    cmd = (f'7z u -t7z -mmt{SUBTHREADS}x{COMP_LVL} -up0q0x1z1 '
           f'-xr@"{EXCLUDE}" "{arch_pth}" @"{pth_f}"')
    start, end = getPSCmds(arch_pth.name)
    RunCmd(['powershell', '-command', f'{start}; {cmd}; {end}'],
           console='new').wait()
    pth_f.unlink()


# 7zip command line notes (https://documentation.help/7-Zip/syntax.htm)
# 7z <command> <switches> <base_archive_name> <@{list_filename}>
#
# u         update command
# -t        type of archive switch
#   7z        7z format
# -m        method switch
#   mt[n]       set multithreading to true and try to use n threads
#   x[n]        sets level of compression to n (n = 0|1|3|5|7|9)
# -u        update switch
#   p0        remove archive items that don't match wildcard
#   q0        remove archive items that no longer exist
#   x1        keep archive items that have newer date
#   z1        keep archive items that have same date
# -x        exclude switch
#   r@[f]     recursively exclude files/folders listed in file f
