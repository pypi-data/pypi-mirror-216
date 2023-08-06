"""_2021.py

LoadedToroidalRollerBearingRow
"""


from mastapy.bearings.bearing_results.rolling import _2020, _1993
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_TOROIDAL_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedToroidalRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedToroidalRollerBearingRow',)


class LoadedToroidalRollerBearingRow(_1993.LoadedRollerBearingRow):
    """LoadedToroidalRollerBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_TOROIDAL_ROLLER_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedToroidalRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_2020.LoadedToroidalRollerBearingResults':
        """LoadedToroidalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
