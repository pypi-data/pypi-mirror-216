"""_1594.py

CurrentPerLength
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_CURRENT_PER_LENGTH = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'CurrentPerLength')


__docformat__ = 'restructuredtext en'
__all__ = ('CurrentPerLength',)


class CurrentPerLength(_1573.MeasurementBase):
    """CurrentPerLength

    This is a mastapy class.
    """

    TYPE = _CURRENT_PER_LENGTH

    def __init__(self, instance_to_wrap: 'CurrentPerLength.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
