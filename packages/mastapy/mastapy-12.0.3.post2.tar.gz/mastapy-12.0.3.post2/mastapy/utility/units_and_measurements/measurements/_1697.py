"""_1697.py

TorquePerSquareRootOfPower
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_TORQUE_PER_SQUARE_ROOT_OF_POWER = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'TorquePerSquareRootOfPower')


__docformat__ = 'restructuredtext en'
__all__ = ('TorquePerSquareRootOfPower',)


class TorquePerSquareRootOfPower(_1573.MeasurementBase):
    """TorquePerSquareRootOfPower

    This is a mastapy class.
    """

    TYPE = _TORQUE_PER_SQUARE_ROOT_OF_POWER

    def __init__(self, instance_to_wrap: 'TorquePerSquareRootOfPower.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
