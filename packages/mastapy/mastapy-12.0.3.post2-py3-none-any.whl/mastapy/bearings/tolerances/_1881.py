"""_1881.py

RingTolerance
"""


from mastapy.bearings.tolerances import _1882, _1873
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_RING_TOLERANCE = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'RingTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('RingTolerance',)


class RingTolerance(_1873.InterferenceTolerance):
    """RingTolerance

    This is a mastapy class.
    """

    TYPE = _RING_TOLERANCE

    def __init__(self, instance_to_wrap: 'RingTolerance.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def roundness_specification(self) -> '_1882.RoundnessSpecification':
        """RoundnessSpecification: 'RoundnessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoundnessSpecification

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
