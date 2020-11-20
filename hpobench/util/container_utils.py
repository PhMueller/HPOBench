import os
import importlib
import json
import numpy as np
import enum


class BenchmarkEncoder(json.JSONEncoder):
    """ Json Encoder to save tuple and or numpy arrays | numpy floats / integer.
    from: https://stackoverflow.com/questions/15721363/preserve-python-tuples-with-json

    Serializing tuple/numpy array may not work. We need to annotate those types, to reconstruct them correctly.
    """
    def encode(self, obj):
        def hint(item):
            # Annotate the different item types
            if isinstance(item, tuple):
                return {'__tuple__': True, 'items': [hint(e) for e in item]}
            if isinstance(item, np.ndarray):
                return {'__np.ndarray__': True, 'items': item}
            if isinstance(item, np.float):
                return {'__np.float__': True, 'items': item}
            if isinstance(item, np.ndarray):
                return {'__np.int__': True, 'items': item}
            if isinstance(item, enum.Enum):
                return str(obj)

            # If it is a container data structure, go also through the items.
            if isinstance(item, list):
                return [hint(e) for e in item]
            if isinstance(item, dict):
                return {key: hint(value) for key, value in item.items()}

            return item

        return super(BenchmarkEncoder, self).encode(hint(obj))


def decode_hinted_object(obj):
    if '__tuple__' in obj:
        return tuple(obj['items'])
    if '__np.ndarray__' in obj:
        return tuple(obj['items'])
    if '__np.float__' in obj:
        return tuple(obj['items'])
    if '__np.int__' in obj:
        return tuple(obj['items'])

    return obj


def __reload_module():
    """
    The env variable which enables the debug level is read in during the import of the client module.
    Reloading the module, re-reads the env variable and therefore changes the level.
    """
    import hpobench.container.client_abstract_benchmark as client
    importlib.reload(client)


def enable_container_debug():
    """ Sets the environment variable "HPOBENCH_DEBUG" to true. The container checks this variable and if set to true,
        enables debugging on the container side. """
    os.environ['HPOBENCH_DEBUG'] = 'true'
    __reload_module()


def disable_container_debug():
    os.environ['HPOBENCH_DEBUG'] = 'false'
    __reload_module()