from pathlib import Path

from configparser import (
    ExtendedInterpolation as ExtInterp,
    ConfigParser
)


cfg = ConfigParser(allow_no_value=True,
                   interpolation=ExtInterp())
cfg.optionxform = str
cfg.read_file(open(Path(__file__).parent.with_name('config.ini')))


COMP_LVL = cfg.getint('Default', 'compression_lvl', fallback=5)
fol = Path(cfg.get('Default', 'backup_parent_folder'))
MOVE_BY = cfg.getint('Default', 'move_window_right', fallback=0)

BACKUPS = {fol.joinpath(f'{f}.7z'):
           [str(p) for p in pth.strip().split('\n')]
           for (f, pth) in cfg.items('Backup Paths')}

EXCLUDE = Path(__file__).with_name('exclude.txt')
EXCLUDE.write_text('\n'.join(s for s in cfg.options('Exclude') if s))

__all__ = ['COMP_LVL',
           'MOVE_BY',
           'BACKUPS',
           'EXCLUDE']
