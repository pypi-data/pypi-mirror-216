"""_1666.py

PowerSmallPerVolume
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_POWER_SMALL_PER_VOLUME = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'PowerSmallPerVolume')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerSmallPerVolume',)


class PowerSmallPerVolume(_1573.MeasurementBase):
    """PowerSmallPerVolume

    This is a mastapy class.
    """

    TYPE = _POWER_SMALL_PER_VOLUME

    def __init__(self, instance_to_wrap: 'PowerSmallPerVolume.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
