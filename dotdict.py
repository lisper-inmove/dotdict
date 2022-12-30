# -*- coding: utf-8 -*-

from .exception import DKeyErrorException
from .exception import DValueTypeException


class DotDict:

    __key = "___1__47d6__1___"

    @property
    def ___param_key(self):
        return self.__dict__[self.__key]

    def __init__(self, **kargs):
        if self.__key in kargs:
            raise DKeyErrorException(f"{self.__key} cannot be set")
        self.__dict__[self.__key] = kargs

    def __setattr__(self, key, value):
        self.__check_value_type(value)
        self.___param_key[key] = value

    def __getattr__(self, key):
        if key not in self.___param_key:
            self.___param_key[key] = DotDict()
        value = self.___param_key.get(key)
        if isinstance(value, DotDict):
            return value
        self.___param_key[key] = self.__set_value(value)
        value = self.___param_key.get(key)
        return value

    def __set_value(self, value):
        if isinstance(value, dict):
            return self.__set_dict(value)
        elif self.__is_list(value):
            return self.__set_list(value)
        else:
            return value

    def __set_dict(self, value):
        obj = DotDict(**value)
        return obj

    def __set_list(self, value):
        result = []
        for v in value:
            result.append(self.__set_value(v))
        return result

    def __check_value_type(self, value):
        _valid_types = [
            list.__name__, dict.__name__, str.__name__,
            int.__name__, float.__name__, bool.__name__,
            DotDict.__name__, tuple.__name__, set.__name__
        ]
        if type(value).__name__ not in _valid_types:
            msg = f"""
            {value.__class__} type error
            {*_valid_types,} allowed
            """
            raise DValueTypeException(msg)

    def __to_dict_list(self, value):
        result = []
        for v in value:
            if isinstance(v, DotDict):
                v = v.to_dict()
            elif self.__is_list(v):
                v = self.__to_dict_list(v)
            result.append(v)
        return result

    def __is_list(self, value):
        if isinstance(value, list):
            return True
        if isinstance(value, set):
            return True
        if isinstance(value, tuple):
            return True
        return False

    def to_dict(self):
        result = {}
        params = self.__dict__.get(self.__key)
        for key, value in params.items():
            if isinstance(value, DotDict):
                value = value.to_dict()
            if self.__is_list(value):
                value = self.__to_dict_list(value)
            result.update({key: value})
        return result
