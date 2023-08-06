"""_2382.py

MultiNodeConnectorFELink
"""


from mastapy.system_model.fe.links import _2383
from mastapy._internal.python_net import python_net_import

_MULTI_NODE_CONNECTOR_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.FE.Links', 'MultiNodeConnectorFELink')


__docformat__ = 'restructuredtext en'
__all__ = ('MultiNodeConnectorFELink',)


class MultiNodeConnectorFELink(_2383.MultiNodeFELink):
    """MultiNodeConnectorFELink

    This is a mastapy class.
    """

    TYPE = _MULTI_NODE_CONNECTOR_FE_LINK

    def __init__(self, instance_to_wrap: 'MultiNodeConnectorFELink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
