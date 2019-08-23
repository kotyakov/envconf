import os
import pytest
import contextlib

from envconf import (
    ConfigField,
    EnvConfig,
    RequiredArgumentMissed
)


@contextlib.contextmanager
def env(env_vars):
    for k, v in env_vars.items():
        os.environ[k] = str(v)
    yield
    for k in env_vars:
        del os.environ[k]


class TestConfigField:

    def test_required_arguments_ok(self):
        a = ConfigField('A', required=True, transform=int)
        with env({'A': 100}):
            assert a.__get__(None, None) == 100

    def test_required_arguments_error(self):
        a = ConfigField('AAA', required=True)
        with pytest.raises(
            RequiredArgumentMissed,
            match='Configuration variable "AAA" does not found in environment'
        ):
            a.__get__(None, None)

    def test_with_custom_transformer(self):
        a = ConfigField('A', transform=lambda x: int(x) + 100)
        with env({'A': 100}):
            assert a.__get__(None, None) == 200

    def test_with_custom_transformer_and_default(self):
        a = ConfigField('A', default=888, transform=lambda x: int(x) + 100)
        assert a.__get__(None, None) == 888


class TestEnvConfig:

    @pytest.fixture
    def classes(self):
        class A(EnvConfig):
            a = ConfigField('A_FOO', default=1)
            b = ConfigField('A_BAR', required=True, transform=float)
            c = ConfigField('A_BAZ', default=10, transform=int)

        class B(EnvConfig):
            a = ConfigField('B_FOO')

        class C(EnvConfig):
            a = A()
            b = B()
            c = ConfigField('C_FOO', required=True)

        return A, B, C

    def test_class_generation_ok(self, classes):
        a, b, c = classes
        assert a._config_fields == ['a', 'b', 'c']
        assert b._config_fields == ['a']
        assert c._config_fields == ['c']

    def test_with_nested_configs_ok(self, classes):
        a, b, c = classes
        with env({'A_BAR': 5, 'C_FOO': 'KEK'}):
            expected = {
                'a': {'a': 1, 'b': 5.0, 'c': 10},
                'b': {'a': None},
                'c': 'KEK'
            }
            assert c().to_dict() == expected

    def test_with_nested_configs_error(self, classes):
        a, b, c = classes
        with pytest.raises(
            RequiredArgumentMissed,
            match='Configuration variable "A_BAR" does not found in environment'
        ):
            c().to_dict()

    def test_without_nested_configs_ok(self, classes):
        a, _, __ = classes
        with env({'A_BAR': 10.5}):
            expected = {'a': 1, 'b': 10.5, 'c': 10}
            assert a().to_dict() == expected

    def test_without_nested_configs_error(self, classes):
        a, _, __ = classes
        with pytest.raises(
            RequiredArgumentMissed,
            match='Configuration variable "A_BAR" does not found in environment'
        ):
            a().to_dict()
