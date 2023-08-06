from typing import Any
import strinpy
import keyword
import re


class Typer:
    def __init__(self) -> None:
        self.parts: list[Any] = ['from typing import List, Dict, Union, TypedDict, Optional\n\n']
        self.names: set[str] = set()
        self.dicts: dict[str, str] = {}

    def format_name(self, name: str) -> str:
        # convert snakecase to camelcase
        parts = name.split('_')
        name = ''.join([part.capitalize() for part in parts])
        if name not in self.names:
            self.names.add(name)
            return name
        count = 0
        while f'{name}{count}' in self.names:
            count += 1
        name = f'{name}{count}'
        self.names.add(name)
        return name

    def is_invalid_name(self, name: str) -> bool:
        if keyword.iskeyword(name):
            return True
        return not re.match(r'^[\w_][\w_\d]*$', name)

    def is_exists(self, name, attrs: dict) -> tuple[bool, str]:
        key = str(attrs)
        if key in self.dicts:
            return True, self.dicts[key]
        name = self.format_name(name)
        self.dicts[key] = name
        return False, name

    def _typerify(self, key: str, v: Any) -> str:
        # key = self.format_name(key)
        if isinstance(v, str):
            return 'str'
        elif isinstance(v, bool):
            return 'bool'
        elif isinstance(v, int):
            return 'int'
        elif isinstance(v, float):
            return 'float'
        elif v == None:
            return 'None'
        elif isinstance(v, dict):
            if not v.values():
                return 'Dict'
            attrs = {k: self._typerify(k, v) for k, v in v.items()}
            exist, name = self.is_exists(key, attrs)
            if exist:
                return name
            if any(self.is_invalid_name(k) for k in v.keys()):
                self.parts.append(strinpy.build([name, ' = TypedDict("', key, '", {', ', '.join(f'"{k}": "{v}"' for k, v in attrs.items()), '})']))
                return name
            self.parts.append([
                f'class {name}(TypedDict):\n',
                [[f'    {k}:"{v}"\n'] for k, v in attrs.items()],
            ])
            return name
        elif isinstance(v, list):
            types = list(set(self._typerify(f'{key}_item', v) for v in v))
            if types:
                parts = []
                optional = 'None' in types
                if optional:
                    types.remove('None')
                    parts.append('Optional[')
                if len(types) == 1:
                    parts.append(types[0])
                else:
                    parts.append('Union[' + ', '.join(types) + ']')
                if optional:
                    parts.append(']')
                return strinpy.build(['List[', parts, ']'])
            return 'List'
        else:
            return str(v)

    def typerify(self, key: str, root: Any) -> str:
        self._typerify(key, root)
        if isinstance(root, list):
            self.parts.append(f'{key} = {self._typerify(key, root)}')
        return strinpy.build(self.parts)


if __name__ == '__main__':
    import json
    from pathlib import Path
    from .beautifier import beautify

    converter = Typer()
    # data = {
    #     "a": {"value": 1, "b": {"value": 2}},
    #     "b": {"value": 2, "b": {"value": 3}},
    # }
    data = [
        {
            "a": {
                "value": 1,
                "b": {
                    "value": 2
                }
            }
        },
        {
            "a": {
                "value": 1,
                "b": {
                    "value": 24
                }
            }
        }
    ]
    data = json.loads(Path('test.json').read_bytes())
    converter.typerify('Root', data)
    code = strinpy.build(converter.parts)
    # code = json.dumps(converter.parts)
    code = beautify(code)
    Path('output.py').write_text(code)
