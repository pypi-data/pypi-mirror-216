"""_2524.py

CycloidalAssembly
"""


from typing import List

from mastapy.cycloidal import _1419
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.cycloidal import _2526, _2525
from mastapy.system_model.part_model import _2433
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalAssembly')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssembly',)


class CycloidalAssembly(_2433.SpecialisedAssembly):
    """CycloidalAssembly

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_ASSEMBLY

    def __init__(self, instance_to_wrap: 'CycloidalAssembly.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cycloidal_assembly_design(self) -> '_1419.CycloidalAssemblyDesign':
        """CycloidalAssemblyDesign: 'CycloidalAssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalAssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def ring_pins(self) -> '_2526.RingPins':
        """RingPins: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPins

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def known_designs(self) -> 'List[_1419.CycloidalAssemblyDesign]':
        """List[CycloidalAssemblyDesign]: 'KnownDesigns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KnownDesigns

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def add_disc(self) -> '_2525.CycloidalDisc':
        """ 'AddDisc' is the original name of this method.

        Returns:
            mastapy.system_model.part_model.cycloidal.CycloidalDisc
        """

        method_result = self.wrapped.AddDisc()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def design_named(self, name: 'str') -> '_1419.CycloidalAssemblyDesign':
        """ 'DesignNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.cycloidal.CycloidalAssemblyDesign
        """

        name = str(name)
        method_result = self.wrapped.DesignNamed(name if name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def remove_disc_from_designs(self, disc_id: 'int'):
        """ 'RemoveDiscFromDesigns' is the original name of this method.

        Args:
            disc_id (int)
        """

        disc_id = int(disc_id)
        self.wrapped.RemoveDiscFromDesigns(disc_id if disc_id else 0)

    def set_active_cycloidal_assembly_design(self, cycloidal_assembly_design: '_1419.CycloidalAssemblyDesign'):
        """ 'SetActiveCycloidalAssemblyDesign' is the original name of this method.

        Args:
            cycloidal_assembly_design (mastapy.cycloidal.CycloidalAssemblyDesign)
        """

        self.wrapped.SetActiveCycloidalAssemblyDesign(cycloidal_assembly_design.wrapped if cycloidal_assembly_design else None)

    def try_remove_design(self, design: '_1419.CycloidalAssemblyDesign') -> 'bool':
        """ 'TryRemoveDesign' is the original name of this method.

        Args:
            design (mastapy.cycloidal.CycloidalAssemblyDesign)

        Returns:
            bool
        """

        method_result = self.wrapped.TryRemoveDesign(design.wrapped if design else None)
        return method_result
