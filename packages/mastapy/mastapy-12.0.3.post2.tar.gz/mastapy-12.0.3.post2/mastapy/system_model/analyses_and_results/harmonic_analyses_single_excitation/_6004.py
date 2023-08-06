"""_6004.py

HarmonicAnalysisOfSingleExcitation
"""


from mastapy.system_model.analyses_and_results.harmonic_analyses import (
    _5620, _5673, _5674, _5675,
    _5676, _5677, _5678, _5679,
    _5680, _5681, _5682, _5683,
    _5693, _5695, _5696, _5698,
    _5727, _5744, _5769
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.analysis_cases import _7479
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'HarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisOfSingleExcitation',)


class HarmonicAnalysisOfSingleExcitation(_7479.StaticLoadAnalysisCase):
    """HarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def excitation_detail(self) -> '_5620.AbstractPeriodicExcitationDetail':
        """AbstractPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5620.AbstractPeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to AbstractPeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_periodic_excitation_detail(self) -> '_5673.ElectricMachinePeriodicExcitationDetail':
        """ElectricMachinePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5673.ElectricMachinePeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachinePeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_x_force_periodic_excitation_detail(self) -> '_5674.ElectricMachineRotorXForcePeriodicExcitationDetail':
        """ElectricMachineRotorXForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5674.ElectricMachineRotorXForcePeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorXForcePeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_x_moment_periodic_excitation_detail(self) -> '_5675.ElectricMachineRotorXMomentPeriodicExcitationDetail':
        """ElectricMachineRotorXMomentPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5675.ElectricMachineRotorXMomentPeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorXMomentPeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_y_force_periodic_excitation_detail(self) -> '_5676.ElectricMachineRotorYForcePeriodicExcitationDetail':
        """ElectricMachineRotorYForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5676.ElectricMachineRotorYForcePeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorYForcePeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_y_moment_periodic_excitation_detail(self) -> '_5677.ElectricMachineRotorYMomentPeriodicExcitationDetail':
        """ElectricMachineRotorYMomentPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5677.ElectricMachineRotorYMomentPeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorYMomentPeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_z_force_periodic_excitation_detail(self) -> '_5678.ElectricMachineRotorZForcePeriodicExcitationDetail':
        """ElectricMachineRotorZForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5678.ElectricMachineRotorZForcePeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorZForcePeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_axial_loads_excitation_detail(self) -> '_5679.ElectricMachineStatorToothAxialLoadsExcitationDetail':
        """ElectricMachineStatorToothAxialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5679.ElectricMachineStatorToothAxialLoadsExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothAxialLoadsExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_loads_excitation_detail(self) -> '_5680.ElectricMachineStatorToothLoadsExcitationDetail':
        """ElectricMachineStatorToothLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5680.ElectricMachineStatorToothLoadsExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothLoadsExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_radial_loads_excitation_detail(self) -> '_5681.ElectricMachineStatorToothRadialLoadsExcitationDetail':
        """ElectricMachineStatorToothRadialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5681.ElectricMachineStatorToothRadialLoadsExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothRadialLoadsExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_tangential_loads_excitation_detail(self) -> '_5682.ElectricMachineStatorToothTangentialLoadsExcitationDetail':
        """ElectricMachineStatorToothTangentialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5682.ElectricMachineStatorToothTangentialLoadsExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothTangentialLoadsExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_electric_machine_torque_ripple_periodic_excitation_detail(self) -> '_5683.ElectricMachineTorqueRipplePeriodicExcitationDetail':
        """ElectricMachineTorqueRipplePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5683.ElectricMachineTorqueRipplePeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineTorqueRipplePeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_gear_mesh_excitation_detail(self) -> '_5693.GearMeshExcitationDetail':
        """GearMeshExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5693.GearMeshExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GearMeshExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_gear_mesh_misalignment_excitation_detail(self) -> '_5695.GearMeshMisalignmentExcitationDetail':
        """GearMeshMisalignmentExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5695.GearMeshMisalignmentExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GearMeshMisalignmentExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_gear_mesh_te_excitation_detail(self) -> '_5696.GearMeshTEExcitationDetail':
        """GearMeshTEExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5696.GearMeshTEExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GearMeshTEExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_general_periodic_excitation_detail(self) -> '_5698.GeneralPeriodicExcitationDetail':
        """GeneralPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5698.GeneralPeriodicExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GeneralPeriodicExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_periodic_excitation_with_reference_shaft(self) -> '_5727.PeriodicExcitationWithReferenceShaft':
        """PeriodicExcitationWithReferenceShaft: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5727.PeriodicExcitationWithReferenceShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to PeriodicExcitationWithReferenceShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_single_node_periodic_excitation_with_reference_shaft(self) -> '_5744.SingleNodePeriodicExcitationWithReferenceShaft':
        """SingleNodePeriodicExcitationWithReferenceShaft: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5744.SingleNodePeriodicExcitationWithReferenceShaft.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to SingleNodePeriodicExcitationWithReferenceShaft. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excitation_detail_of_type_unbalanced_mass_excitation_detail(self) -> '_5769.UnbalancedMassExcitationDetail':
        """UnbalancedMassExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcitationDetail

        if temp is None:
            return None

        if _5769.UnbalancedMassExcitationDetail.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to UnbalancedMassExcitationDetail. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
