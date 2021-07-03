from pathlib import Path

from configparser import (
    ExtendedInterpolation as ExtInterp,
    ConfigParser as ConfigParser
)


cfg = ConfigParser(allow_no_value=True,
                   interpolation=ExtInterp())
cfg.optionxform = str
cfg.read_file(open(Path(__file__).parent.with_name('config.ini')))


fol = Path(cfg.get('Default', 'backup_folder'))

BACKUPS = {fol.joinpath(f'{f}.7z'):
           [Path(p) for p in pth.strip().split('\n')]
           for (f, pth) in cfg.items('Backup Paths')}
IGNORE = [f"-xr!{p}" for p in cfg.options('Ignore')]
