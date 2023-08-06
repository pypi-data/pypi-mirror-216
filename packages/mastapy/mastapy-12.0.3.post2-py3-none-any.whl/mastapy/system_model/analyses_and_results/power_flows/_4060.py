"""_4060.py

OilSealPowerFlow
"""


from mastapy.system_model.part_model import _2423
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6857
from mastapy.system_model.analyses_and_results.power_flows import _4017
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'OilSealPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealPowerFlow',)


class OilSealPowerFlow(_4017.ConnectorPowerFlow):
    """OilSealPowerFlow

    This is a mastapy class.
    """

    TYPE = _OIL_SEAL_POWER_FLOW

    def __init__(self, instance_to_wrap: 'OilSealPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2423.OilSeal':
        """OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6857.OilSealLoadCase':
        """OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
