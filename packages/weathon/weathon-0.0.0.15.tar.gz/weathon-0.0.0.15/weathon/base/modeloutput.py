from collections import OrderedDict
from dataclasses import fields


class BaseModelOutput(list):

    def __post_init__(self):
        self.reconstruct()
        self.post_init = True

    def reconstruct(self):
        # Low performance, but low frequency.
        self.clear()
        for idx, key in enumerate(self.keys()):
            self.append(getattr(self, key))

    def __getitem__(self, item):
        if isinstance(item, str):
            if hasattr(self, item):
                return getattr(self, item)
        elif isinstance(item, (int, slice)):
            return super().__getitem__(item)
        raise IndexError(f'No Index {item} found in the dataclass.')

    def __setitem__(self, key, value):
        if isinstance(key, str):
            if key in [f.name for f in fields(self)]:
                if key not in self.keys():
                    super().__setattr__(key, value)
                    self.reconstruct()
                elif id(getattr(self, key)) != id(value):
                    super().__setattr__(key, value)
                    super().__setitem__(self.keys().index(key), value)
            else:
                super().__setattr__(key, value)
        elif isinstance(key, int):
            super().__setitem__(key, value)
            key_name = self.keys()[key]
            super().__setattr__(key_name, value)

    def __setattr__(self, key, value):
        if getattr(self, 'post_init', False):
            return self.__setitem__(key, value)
        else:
            return super().__setattr__(key, value)

    def keys(self):
        return [ f.name for f in fields(self) if getattr(self, f.name) is not None ]

    def items(self):
        return self.to_dict().items()

    def to_dict(self):
        output = OrderedDict()
        for key in self.keys():
            output[key] = getattr(self, key)
        return output
