"""
Input validation utils
"""
from typing import Dict, Any, Set
import pprint


class DictAsObject:
    """
    A class that allows to access a dictionary as if it were an object.
    """
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, DictAsObject(value))
            elif isinstance(value, list):
                setattr(self, key, [DictAsObject(item) if isinstance(item, dict) else item for item in value])
            else:
                setattr(self, key, value)
    
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, DictAsObject):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [item.to_dict() if isinstance(item, DictAsObject) else item for item in value]
            else:
                result[key] = value
        return result
    
    def __getattr__(self, key):
        return None
    
    def __getitem__(self, key):
        return self.__dict__.get(key, None)
    
    def __repr__(self):
        return pprint.pformat(
                self.to_dict(),
                compact=True,
                indent=1,
                width = 80
                )
    