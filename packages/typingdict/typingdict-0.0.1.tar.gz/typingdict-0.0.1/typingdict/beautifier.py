import ast
import astor


def beautify(code: str) -> str:
    return astor.to_source(ast.parse(code))
