"""_1560.py

MKLVersion
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MKL_VERSION = python_net_import('SMT.MastaAPI.Utility', 'MKLVersion')


__docformat__ = 'restructuredtext en'
__all__ = ('MKLVersion',)


class MKLVersion(_0.APIBase):
    """MKLVersion

    This is a mastapy class.
    """

    TYPE = _MKL_VERSION

    def __init__(self, instance_to_wrap: 'MKLVersion.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def build(self) -> 'str':
        """str: 'Build' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Build

        if temp is None:
            return ''

        return temp

    @property
    def platform(self) -> 'str':
        """str: 'Platform' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Platform

        if temp is None:
            return ''

        return temp

    @property
    def processor(self) -> 'str':
        """str: 'Processor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Processor

        if temp is None:
            return ''

        return temp

    @property
    def product_status(self) -> 'str':
        """str: 'ProductStatus' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProductStatus

        if temp is None:
            return ''

        return temp

    @property
    def version(self) -> 'str':
        """str: 'Version' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Version

        if temp is None:
            return ''

        return temp
