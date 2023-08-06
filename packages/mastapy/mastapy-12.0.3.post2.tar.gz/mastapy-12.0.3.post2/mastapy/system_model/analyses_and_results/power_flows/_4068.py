"""_4068.py

PointLoadPowerFlow
"""


from mastapy.system_model.part_model import _2428
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6869
from mastapy.system_model.analyses_and_results.power_flows import _4107
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PointLoadPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadPowerFlow',)


class PointLoadPowerFlow(_4107.VirtualComponentPowerFlow):
    """PointLoadPowerFlow

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_POWER_FLOW

    def __init__(self, instance_to_wrap: 'PointLoadPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2428.PointLoad':
        """PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6869.PointLoadLoadCase':
        """PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
