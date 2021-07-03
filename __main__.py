from subprocess import run

try:
    from .src import *
except ImportError:
    from pathlib import Path
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)


def main():
    pths = Path('files.txt')
    for bck_to, bck_from in BACKUPS.items():
        if not bck_to.parent.exists():
            raise FileNotFoundError(f'"{bck_to}" could not be found.')
        for pth in bck_from:
            if not pth.exists():
                raise FileNotFoundError(f'"{pth}" could not be found.')
        pths.write_text('\n'.join([str(p) for p in bck_from]))
        run(['7z', 'a', '-t7z', '-uz0',
             str(bck_to), f'@{pths}', *IGNORE])
        print(f'\n{"="*50}\n')
    pths.unlink()


if __name__ == "__main__":
    main()
