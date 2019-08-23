import os

from .exceptions import RequiredArgumentMissed


class ConfigField:

    def __init__(self, name, required=False, transform=None, default=None):
        self.name = name
        self.required = required
        self.transform = transform or (lambda x: x)
        self.default = default
        self._sentinel = object()

    def __get__(self, instance, owner):
        val = os.getenv(self.name, self._sentinel)
        if val is self._sentinel:
            if self.required:
                raise RequiredArgumentMissed(argname=self.name)
            else:
                return self.default
        return self.transform(val)

    def __set__(self, instance, value):
        raise NotImplementedError


class _EnvConfigMeta(type):

    def __new__(mcs, name, bases, namespace):
        if '_config_fields' not in namespace:
            namespace['_config_fields'] = []
        for attr, val in namespace.items():
            if isinstance(val, ConfigField):
                namespace['_config_fields'].append(attr)
        return super().__new__(mcs, name, bases, namespace)


class EnvConfig(metaclass=_EnvConfigMeta):

    _config_fields = []

    def to_dict(self):
        as_dict = {}
        for attr in type(self).__dict__:
            if attr.startswith('__'):
                continue
            val = getattr(self, attr)
            if isinstance(val, EnvConfig):
                as_dict[attr] = val.to_dict()
        for attr in self._config_fields:
            as_dict[attr] = getattr(self, attr)
        return as_dict


__all__ = ('ConfigField', 'EnvConfig')
