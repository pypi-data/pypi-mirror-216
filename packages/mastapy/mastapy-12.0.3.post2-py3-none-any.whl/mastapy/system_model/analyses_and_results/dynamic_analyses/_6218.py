"""_6218.py

BearingDynamicAnalysis
"""


from typing import List

from mastapy.system_model.part_model import _2397
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6751
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6246
from mastapy._internal.python_net import python_net_import

_BEARING_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'BearingDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDynamicAnalysis',)


class BearingDynamicAnalysis(_6246.ConnectorDynamicAnalysis):
    """BearingDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _BEARING_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'BearingDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2397.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6751.BearingLoadCase':
        """BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[BearingDynamicAnalysis]':
        """List[BearingDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
