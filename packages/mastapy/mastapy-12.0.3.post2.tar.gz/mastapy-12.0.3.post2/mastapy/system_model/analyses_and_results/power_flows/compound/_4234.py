"""_4234.py

TorqueConverterTurbineCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2566
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4105
from mastapy.system_model.analyses_and_results.power_flows.compound import _4153
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'TorqueConverterTurbineCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundPowerFlow',)


class TorqueConverterTurbineCompoundPowerFlow(_4153.CouplingHalfCompoundPowerFlow):
    """TorqueConverterTurbineCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2566.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4105.TorqueConverterTurbinePowerFlow]':
        """List[TorqueConverterTurbinePowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4105.TorqueConverterTurbinePowerFlow]':
        """List[TorqueConverterTurbinePowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
