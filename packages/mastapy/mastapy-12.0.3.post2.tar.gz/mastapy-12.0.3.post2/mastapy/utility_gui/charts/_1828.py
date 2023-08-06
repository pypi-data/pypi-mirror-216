"""_1828.py

ThreeDChartDefinition
"""


from typing import List

from mastapy.utility.report import _1711
from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1455
from mastapy.math_utility.measured_ranges import _1532
from mastapy._internal.cast_exception import CastException
from mastapy.utility_gui.charts import _1824, _1822
from mastapy._internal.python_net import python_net_import

_THREE_D_CHART_DEFINITION = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'ThreeDChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('ThreeDChartDefinition',)


class ThreeDChartDefinition(_1822.NDChartDefinition):
    """ThreeDChartDefinition

    This is a mastapy class.
    """

    TYPE = _THREE_D_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'ThreeDChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def z_axis(self) -> '_1711.AxisSettings':
        """AxisSettings: 'ZAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZAxis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def x_axis_range(self) -> '_1455.Range':
        """Range: 'XAxisRange' is the original name of this property."""

        temp = self.wrapped.XAxisRange

        if temp is None:
            return None

        if _1455.Range.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast x_axis_range to Range. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @x_axis_range.setter
    def x_axis_range(self, value: '_1455.Range'):
        value = value.wrapped if value else None
        self.wrapped.XAxisRange = value

    @property
    def y_axis_range(self) -> '_1455.Range':
        """Range: 'YAxisRange' is the original name of this property."""

        temp = self.wrapped.YAxisRange

        if temp is None:
            return None

        if _1455.Range.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast y_axis_range to Range. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @y_axis_range.setter
    def y_axis_range(self, value: '_1455.Range'):
        value = value.wrapped if value else None
        self.wrapped.YAxisRange = value

    @property
    def z_axis_range(self) -> '_1455.Range':
        """Range: 'ZAxisRange' is the original name of this property."""

        temp = self.wrapped.ZAxisRange

        if temp is None:
            return None

        if _1455.Range.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast z_axis_range to Range. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @z_axis_range.setter
    def z_axis_range(self, value: '_1455.Range'):
        value = value.wrapped if value else None
        self.wrapped.ZAxisRange = value

    def data_points_for_surfaces(self) -> 'List[_1824.PointsForSurface]':
        """ 'DataPointsForSurfaces' is the original name of this method.

        Returns:
            List[mastapy.utility_gui.charts.PointsForSurface]
        """

        return conversion.pn_to_mp_objects_in_list(self.wrapped.DataPointsForSurfaces())
