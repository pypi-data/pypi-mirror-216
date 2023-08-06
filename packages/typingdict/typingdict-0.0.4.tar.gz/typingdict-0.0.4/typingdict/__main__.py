import sys
from pathlib import Path
import json
from . import typerify
from .beautifier import beautify

if __name__ == '__main__':
    data = json.loads(Path(sys.argv[1]).read_bytes())
    code = typerify(data)
    code = beautify(code)
    print(code)
