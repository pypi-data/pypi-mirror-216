"""_6250.py

CVTBeltConnectionDynamicAnalysis
"""


from mastapy.system_model.connections_and_sockets import _2232
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6219
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'CVTBeltConnectionDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionDynamicAnalysis',)


class CVTBeltConnectionDynamicAnalysis(_6219.BeltConnectionDynamicAnalysis):
    """CVTBeltConnectionDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_BELT_CONNECTION_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2232.CVTBeltConnection':
        """CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
