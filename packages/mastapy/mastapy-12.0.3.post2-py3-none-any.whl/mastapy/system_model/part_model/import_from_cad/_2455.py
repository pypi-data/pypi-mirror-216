"""_2455.py

CylindricalGearInPlanetarySetFromCAD
"""


from mastapy.system_model.part_model.import_from_cad import _2454
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_IN_PLANETARY_SET_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'CylindricalGearInPlanetarySetFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearInPlanetarySetFromCAD',)


class CylindricalGearInPlanetarySetFromCAD(_2454.CylindricalGearFromCAD):
    """CylindricalGearInPlanetarySetFromCAD

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_IN_PLANETARY_SET_FROM_CAD

    def __init__(self, instance_to_wrap: 'CylindricalGearInPlanetarySetFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
