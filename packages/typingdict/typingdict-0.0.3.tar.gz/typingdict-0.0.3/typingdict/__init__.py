from .typer import Typer

def typerify(code: dict) -> str:
    return Typer().typerify('Root', code)

__version__ = '0.0.3'