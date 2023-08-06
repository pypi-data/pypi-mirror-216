"""_1421.py

CycloidalDiscDesignExporter
"""


from typing import List

from mastapy.cycloidal import _1426
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._math.vector_2d import Vector2D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_DESIGN_EXPORTER = python_net_import('SMT.MastaAPI.Cycloidal', 'CycloidalDiscDesignExporter')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscDesignExporter',)


class CycloidalDiscDesignExporter(_0.APIBase):
    """CycloidalDiscDesignExporter

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_DESIGN_EXPORTER

    def __init__(self, instance_to_wrap: 'CycloidalDiscDesignExporter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def geometry_to_export(self) -> '_1426.GeometryToExport':
        """GeometryToExport: 'GeometryToExport' is the original name of this property."""

        temp = self.wrapped.GeometryToExport

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1426.GeometryToExport)(value) if value is not None else None

    @geometry_to_export.setter
    def geometry_to_export(self, value: '_1426.GeometryToExport'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GeometryToExport = value

    @property
    def include_modifications(self) -> 'bool':
        """bool: 'IncludeModifications' is the original name of this property."""

        temp = self.wrapped.IncludeModifications

        if temp is None:
            return False

        return temp

    @include_modifications.setter
    def include_modifications(self, value: 'bool'):
        self.wrapped.IncludeModifications = bool(value) if value else False

    @property
    def number_of_half_lobe_points_for_export(self) -> 'int':
        """int: 'NumberOfHalfLobePointsForExport' is the original name of this property."""

        temp = self.wrapped.NumberOfHalfLobePointsForExport

        if temp is None:
            return 0

        return temp

    @number_of_half_lobe_points_for_export.setter
    def number_of_half_lobe_points_for_export(self, value: 'int'):
        self.wrapped.NumberOfHalfLobePointsForExport = int(value) if value else 0

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def profile_points(self, geometry_to_export: '_1426.GeometryToExport', include_modifications_in_export: 'bool', number_of_half_lobe_points_for_export: 'int') -> 'List[Vector2D]':
        """ 'ProfilePoints' is the original name of this method.

        Args:
            geometry_to_export (mastapy.cycloidal.GeometryToExport)
            include_modifications_in_export (bool)
            number_of_half_lobe_points_for_export (int)

        Returns:
            List[Vector2D]
        """

        geometry_to_export = conversion.mp_to_pn_enum(geometry_to_export)
        include_modifications_in_export = bool(include_modifications_in_export)
        number_of_half_lobe_points_for_export = int(number_of_half_lobe_points_for_export)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.ProfilePoints(geometry_to_export, include_modifications_in_export if include_modifications_in_export else False, number_of_half_lobe_points_for_export if number_of_half_lobe_points_for_export else 0), Vector2D)

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
