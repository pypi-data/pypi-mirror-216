from .typer import Typer

def typerify(code: dict) -> str:
    return Typer().typerify('Root', code)