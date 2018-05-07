import time
import types
from functools import wraps


class timer:
    def __init__(self, desc):
        self.desc = desc

    def __enter__(self):
        print(self.desc, 'started')
        self.start = time.clock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.desc, 'finished in', time.clock() - self.start, 's')


def profile(obj):
    def wrap_fun(fn):
        @wraps(fn)
        def fun(*args):
            with timer(fn.__name__):
                output = fn(*args)
            return output

        return fun

    def wrap_class(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, wrap_fun(getattr(cls, attr)))
        return cls

    if type(obj) is types.FunctionType:
        return wrap_fun(obj)
    else:
        return wrap_class(obj)


@profile
class Foo:
    def __init__(self):
        pass

    def method_a(self):
        return 1

    def method_b(self):
        return 2


@profile
def fun_a():
    return 3


fun_a()
f = Foo()
f.method_a()

f.method_b()
