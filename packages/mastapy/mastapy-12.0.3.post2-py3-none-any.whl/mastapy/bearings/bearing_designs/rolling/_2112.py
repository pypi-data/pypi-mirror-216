"""_2112.py

DeepGrooveBallBearing
"""


from mastapy.bearings.bearing_designs.rolling import _2102
from mastapy._internal.python_net import python_net_import

_DEEP_GROOVE_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'DeepGrooveBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('DeepGrooveBallBearing',)


class DeepGrooveBallBearing(_2102.BallBearing):
    """DeepGrooveBallBearing

    This is a mastapy class.
    """

    TYPE = _DEEP_GROOVE_BALL_BEARING

    def __init__(self, instance_to_wrap: 'DeepGrooveBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
