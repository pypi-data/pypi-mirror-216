import json
from types import FunctionType

import numpy as np


class EnhancedEncoder(json.JSONEncoder):
    """ Enhanced json encoder for not supported types """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



class JSONIteratorEncoder(json.JSONEncoder):
    """Implement this method in order that supporting arbitrary iterators, it returns
        a serializable object for ``obj``, or calls the base implementation
        (to raise a ``TypeError``).

    """

    def default(self, obj):
        if isinstance(obj, FunctionType):
            return None
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return json.JSONEncoder.default(self, obj)