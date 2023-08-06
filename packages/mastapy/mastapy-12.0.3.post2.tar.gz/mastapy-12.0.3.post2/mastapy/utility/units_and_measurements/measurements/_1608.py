"""_1608.py

Enum
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_ENUM = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Enum')


__docformat__ = 'restructuredtext en'
__all__ = ('Enum',)


class Enum(_1573.MeasurementBase):
    """Enum

    This is a mastapy class.
    """

    TYPE = _ENUM

    def __init__(self, instance_to_wrap: 'Enum.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
