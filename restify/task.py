# coding: utf-8

from typing import Callable


def fullname(cls: type):
    return cls.__module__ + '.' + cls.__qualname__


class NameConflict(Exception):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class TaskRegistry:
    def __init__(self):
        self._registry = {}

    def add(self, f: Callable, name: str=None):
        if name is None:
            name = fullname(f)
        elif not isinstance(name, str):
            raise ValueError('name must be a str, got {0!r} instead'.format(type(name)))

        if name in self._registry:
            raise NameConflict(name)
        else:
            self._registry[name] = f

    def remove(self, f: Callable):
        name = fullname(f)

        del self._registry[name]

    def remove_by_name(self, name: str):
        del self._registry[name]

    def call(self, name: str, *args, **kwargs):
        try:
            f = self._registry[name]
        except KeyError:
            raise KeyError(name)
        else:
            try:
                return f(*args, **kwargs)
            except TypeError as e:
                raise TypeError('Failed to call {0}()'.format(name)) from e

    def __call__(self, *args, **kwargs):
        def decorator(f, *a, **k):
            self.add(f, *a, **k)
            return f

        if args:
            return decorator(args[0])
        else:
            return decorator


api_task = TaskRegistry()
