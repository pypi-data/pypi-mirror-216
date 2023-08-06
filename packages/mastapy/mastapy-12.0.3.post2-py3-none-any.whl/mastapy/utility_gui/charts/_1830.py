"""_1830.py

TwoDChartDefinition
"""


from typing import List

from mastapy.utility_gui.charts import _1817, _1826, _1822
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_TWO_D_CHART_DEFINITION = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'TwoDChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('TwoDChartDefinition',)


class TwoDChartDefinition(_1822.NDChartDefinition):
    """TwoDChartDefinition

    This is a mastapy class.
    """

    TYPE = _TWO_D_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'TwoDChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def const_lines(self) -> 'List[_1817.ConstantLine]':
        """List[ConstantLine]: 'ConstLines' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConstLines

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def series_list(self) -> 'List[_1826.Series2D]':
        """List[Series2D]: 'SeriesList' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SeriesList

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
