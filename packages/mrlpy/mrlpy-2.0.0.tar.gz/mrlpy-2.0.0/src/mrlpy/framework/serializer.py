import json
from json import JSONEncoder
from typing import Any

from mrlpy.framework.mrl_dataclass import classes, classes_to_names


class PolymorphicEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        d = dict(**o.__dict__)
        d["class"] = classes_to_names[type(o).__name__]
        return d


class DefaultEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def encode(o: object) -> str:
    return json.dumps(o, cls=PolymorphicEncoder)
