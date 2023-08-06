"""_1426.py

GeometryToExport
"""


from enum import Enum

from mastapy._internal.python_net import python_net_import

_GEOMETRY_TO_EXPORT = python_net_import('SMT.MastaAPI.Cycloidal', 'GeometryToExport')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryToExport',)


class GeometryToExport(Enum):
    """GeometryToExport

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls):
        return _GEOMETRY_TO_EXPORT

    SINGLE_LOBE = 0
    WHOLE_DISC = 1


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


GeometryToExport.__setattr__ = __enum_setattr
GeometryToExport.__delattr__ = __enum_delattr
