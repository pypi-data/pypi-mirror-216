import json

import mrlpy.framework.mrl_dataclass
from mrlpy.framework.mrl_dataclass import classes


def decode(d: dict):
    # Fix double encoding
    if 'data' in d:
        new_data = []
        for obj in d['data']:
            o = loads(obj)
            if isinstance(o, str):
                try:
                    o = loads(o)
                except ValueError:
                    pass
            new_data.append(o)
        d['data'] = new_data
    if "class" in d:
        clazz = d["class"]
        del d["class"]
        if clazz in classes:
            return classes[clazz](**d)

    f_names = frozenset(d)
    if f_names in mrlpy.framework.mrl_dataclass.cache:
        return mrlpy.framework.mrl_dataclass.cache[f_names](**d)
    return d


def loads(s: str):
    return json.loads(s, object_hook=decode)
