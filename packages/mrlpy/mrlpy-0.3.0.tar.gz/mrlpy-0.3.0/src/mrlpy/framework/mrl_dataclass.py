from dataclasses import dataclass, fields


def mrl_dataclass(name: str):
    """
    This decorator marks the decorated class as a dataclass.
    It also adds the class to mrlpy's json deserializer class cache.
    This means it will be automatically deserialized from json into a new instance
    of a decorated class. Serializing is much easier and doesn't require the cache.
    """

    def wrapped_dataclass(cls):
        global cache
        global classes_to_names
        c = dataclass(cls)
        c_fields = fields(c)
        field_names = frozenset(f.name for f in c_fields)
        cache[field_names] = c
        classes[name] = c
        classes_to_names.update({cls.__name__: name})
        return c

    return wrapped_dataclass


cache = {}
classes = dict()
classes_to_names = dict()
