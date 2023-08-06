"""_1737.py

CustomReportMultiPropertyItem
"""


from typing import Generic, TypeVar

from mastapy.utility.report import _1738, _1741
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportMultiPropertyItem')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportMultiPropertyItem',)


TItem = TypeVar('TItem', bound='_1741.CustomReportPropertyItem')


class CustomReportMultiPropertyItem(_1738.CustomReportMultiPropertyItemBase, Generic[TItem]):
    """CustomReportMultiPropertyItem

    This is a mastapy class.

    Generic Types:
        TItem
    """

    TYPE = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM

    def __init__(self, instance_to_wrap: 'CustomReportMultiPropertyItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
