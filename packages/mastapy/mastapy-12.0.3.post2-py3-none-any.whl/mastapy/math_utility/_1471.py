"""_1471.py

DynamicsResponseScalarResult
"""


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DYNAMICS_RESPONSE_SCALAR_RESULT = python_net_import('SMT.MastaAPI.MathUtility', 'DynamicsResponseScalarResult')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicsResponseScalarResult',)


class DynamicsResponseScalarResult(Enum):
    """DynamicsResponseScalarResult

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls):
        return _DYNAMICS_RESPONSE_SCALAR_RESULT

    X = 0
    Y = 1
    Z = 2
    ΘX = 3
    ΘY = 4
    ΘZ = 5
    MAGNITUDE_XYZ = 6
    MAGNITUDE_XY = 7
    MAGNITUDE_ΘXΘYΘZ = 8
    MAGNITUDE_ΘX_ΘY = 9


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


DynamicsResponseScalarResult.__setattr__ = __enum_setattr
DynamicsResponseScalarResult.__delattr__ = __enum_delattr
