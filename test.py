# -*- coding: utf-8 -*-


import json
from dotdict import DotDict


class Test:

    @staticmethod
    def get_obj():
        with open("test_json.json") as f:
            data = json.load(f)
            return DotDict(**data)


if __name__ == '__main__':
    test = Test.get_obj()
    test.a = set([1, 3, 9, -1])
    test.a = test.dishList
    print(test.to_dict())
