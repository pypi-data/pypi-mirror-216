import inspect
import sys


def get_loopback_call(module):
    stack = inspect.stack()
    mod = inspect.getmodule(stack[0][0])
    package = mod.__package__
    name = f'{package}.{module}'
    wraparound = [sys.executable, '-m', name]
    return wraparound
