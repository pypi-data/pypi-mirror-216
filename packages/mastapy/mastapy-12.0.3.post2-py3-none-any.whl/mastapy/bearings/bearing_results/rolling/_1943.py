"""_1943.py

ISOTR1417922001Results
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1942
from mastapy._internal.python_net import python_net_import

_ISOTR1417922001_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'ISOTR1417922001Results')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOTR1417922001Results',)


class ISOTR1417922001Results(_1942.ISOTR141792001Results):
    """ISOTR1417922001Results

    This is a mastapy class.
    """

    TYPE = _ISOTR1417922001_RESULTS

    def __init__(self, instance_to_wrap: 'ISOTR1417922001Results.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def coefficient_for_no_load_power_loss(self) -> 'float':
        """float: 'CoefficientForNoLoadPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoefficientForNoLoadPowerLoss

        if temp is None:
            return 0.0

        return temp
