"""_1942.py

ISOTR141792001Results
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ISOTR141792001_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'ISOTR141792001Results')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOTR141792001Results',)


class ISOTR141792001Results(_0.APIBase):
    """ISOTR141792001Results

    This is a mastapy class.
    """

    TYPE = _ISOTR141792001_RESULTS

    def __init__(self, instance_to_wrap: 'ISOTR141792001Results.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_load_dependent_moment(self) -> 'float':
        """float: 'AxialLoadDependentMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoadDependentMoment

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_axial_load_factor(self) -> 'float':
        """float: 'DynamicAxialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicAxialLoadFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_equivalent_load(self) -> 'float':
        """float: 'DynamicEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicEquivalentLoad

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_radial_load_factor(self) -> 'float':
        """float: 'DynamicRadialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicRadialLoadFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def load_dependent_torque(self) -> 'float':
        """float: 'LoadDependentTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDependentTorque

        if temp is None:
            return 0.0

        return temp

    @property
    def no_load_bearing_resistive_torque(self) -> 'float':
        """float: 'NoLoadBearingResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NoLoadBearingResistiveTorque

        if temp is None:
            return 0.0

        return temp

    @property
    def power_rating_f0(self) -> 'float':
        """float: 'PowerRatingF0' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerRatingF0

        if temp is None:
            return 0.0

        return temp

    @property
    def power_rating_f1(self) -> 'float':
        """float: 'PowerRatingF1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerRatingF1

        if temp is None:
            return 0.0

        return temp

    @property
    def static_axial_load_factor(self) -> 'float':
        """float: 'StaticAxialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticAxialLoadFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def static_equivalent_load(self) -> 'float':
        """float: 'StaticEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticEquivalentLoad

        if temp is None:
            return 0.0

        return temp

    @property
    def static_radial_load_factor(self) -> 'float':
        """float: 'StaticRadialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticRadialLoadFactor

        if temp is None:
            return 0.0

        return temp

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
