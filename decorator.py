import time


class timer:
    def __init__(self, desc):
        self.desc = desc

    def __enter__(self):
        print(self.desc, 'started')
        self.start = time.clock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.desc, 'finished in', time.clock() - self.start, 's')


def decorator(fn):
    def wrap(*args):
        with timer(str(fn).split(' ')[1]):
            fn(*args)

    return wrap


def profile(decorator):
    def decorate(cls):
        if str(type(cls)) == "<class 'function'>":
            cls = decorator(cls)
        else:
            for attr in cls.__dict__:
                if callable(getattr(cls, attr)):
                    setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


@profile(decorator)
class Foo:
    def __init__(self):
        pass

    def method_a(self):
        return 1

    def method_b(self):
        return 2


@profile(decorator)
def fun_a():
    return 3


fun_a()
f = Foo()
f.method_a()

# f.method_b()
