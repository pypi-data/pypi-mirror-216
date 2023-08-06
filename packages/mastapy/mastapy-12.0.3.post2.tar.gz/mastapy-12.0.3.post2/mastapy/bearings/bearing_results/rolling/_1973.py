"""_1973.py

LoadedCylindricalRollerBearingRow
"""


from mastapy.bearings.bearing_results.rolling import _1972, _1984, _1988
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_CYLINDRICAL_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCylindricalRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCylindricalRollerBearingRow',)


class LoadedCylindricalRollerBearingRow(_1988.LoadedNonBarrelRollerBearingRow):
    """LoadedCylindricalRollerBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_CYLINDRICAL_ROLLER_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedCylindricalRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1972.LoadedCylindricalRollerBearingResults':
        """LoadedCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1972.LoadedCylindricalRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedCylindricalRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
