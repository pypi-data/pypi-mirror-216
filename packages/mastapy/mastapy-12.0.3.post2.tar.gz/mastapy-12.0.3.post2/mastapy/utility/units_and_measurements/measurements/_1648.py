"""_1648.py

MagneticVectorPotential
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_MAGNETIC_VECTOR_POTENTIAL = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'MagneticVectorPotential')


__docformat__ = 'restructuredtext en'
__all__ = ('MagneticVectorPotential',)


class MagneticVectorPotential(_1573.MeasurementBase):
    """MagneticVectorPotential

    This is a mastapy class.
    """

    TYPE = _MAGNETIC_VECTOR_POTENTIAL

    def __init__(self, instance_to_wrap: 'MagneticVectorPotential.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
