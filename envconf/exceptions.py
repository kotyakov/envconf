class EnvConfException(Exception):
    """Base error class for envconf"""


class RequiredArgumentMissed(EnvConfException):
    """Raises when required variable not found in process environment."""

    def __init__(self, argname, *args):
        super().__init__(*args)
        self.argname = argname

    def __repr__(self):
        return '{}: missed required env var {}'.format(
            self.__class__.__name__, self.argname
        )

    def __str__(self):
        return 'Configuration variable "{}" does not found in environment'.format(
            self.argname
        )
