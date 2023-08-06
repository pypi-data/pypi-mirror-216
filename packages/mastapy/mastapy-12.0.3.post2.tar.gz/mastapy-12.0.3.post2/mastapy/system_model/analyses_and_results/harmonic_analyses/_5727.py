"""_5727.py

PeriodicExcitationWithReferenceShaft
"""


from mastapy.system_model.analyses_and_results.harmonic_analyses import _5620
from mastapy._internal.python_net import python_net_import

_PERIODIC_EXCITATION_WITH_REFERENCE_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'PeriodicExcitationWithReferenceShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('PeriodicExcitationWithReferenceShaft',)


class PeriodicExcitationWithReferenceShaft(_5620.AbstractPeriodicExcitationDetail):
    """PeriodicExcitationWithReferenceShaft

    This is a mastapy class.
    """

    TYPE = _PERIODIC_EXCITATION_WITH_REFERENCE_SHAFT

    def __init__(self, instance_to_wrap: 'PeriodicExcitationWithReferenceShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
