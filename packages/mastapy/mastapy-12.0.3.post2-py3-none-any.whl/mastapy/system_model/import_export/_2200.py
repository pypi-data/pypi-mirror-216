"""_2200.py

GeometryExportOptions
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEOMETRY_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.ImportExport', 'GeometryExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryExportOptions',)


class GeometryExportOptions(_0.APIBase):
    """GeometryExportOptions

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_EXPORT_OPTIONS

    def __init__(self, instance_to_wrap: 'GeometryExportOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def create_solid(self) -> 'bool':
        """bool: 'CreateSolid' is the original name of this property."""

        temp = self.wrapped.CreateSolid

        if temp is None:
            return False

        return temp

    @create_solid.setter
    def create_solid(self, value: 'bool'):
        self.wrapped.CreateSolid = bool(value) if value else False

    @property
    def draw_fillets(self) -> 'bool':
        """bool: 'DrawFillets' is the original name of this property."""

        temp = self.wrapped.DrawFillets

        if temp is None:
            return False

        return temp

    @draw_fillets.setter
    def draw_fillets(self, value: 'bool'):
        self.wrapped.DrawFillets = bool(value) if value else False

    @property
    def draw_gear_teeth(self) -> 'bool':
        """bool: 'DrawGearTeeth' is the original name of this property."""

        temp = self.wrapped.DrawGearTeeth

        if temp is None:
            return False

        return temp

    @draw_gear_teeth.setter
    def draw_gear_teeth(self, value: 'bool'):
        self.wrapped.DrawGearTeeth = bool(value) if value else False

    @property
    def draw_to_tip_diameter(self) -> 'bool':
        """bool: 'DrawToTipDiameter' is the original name of this property."""

        temp = self.wrapped.DrawToTipDiameter

        if temp is None:
            return False

        return temp

    @draw_to_tip_diameter.setter
    def draw_to_tip_diameter(self, value: 'bool'):
        self.wrapped.DrawToTipDiameter = bool(value) if value else False

    @property
    def include_bearing_cage(self) -> 'bool':
        """bool: 'IncludeBearingCage' is the original name of this property."""

        temp = self.wrapped.IncludeBearingCage

        if temp is None:
            return False

        return temp

    @include_bearing_cage.setter
    def include_bearing_cage(self, value: 'bool'):
        self.wrapped.IncludeBearingCage = bool(value) if value else False

    @property
    def include_bearing_elements(self) -> 'bool':
        """bool: 'IncludeBearingElements' is the original name of this property."""

        temp = self.wrapped.IncludeBearingElements

        if temp is None:
            return False

        return temp

    @include_bearing_elements.setter
    def include_bearing_elements(self, value: 'bool'):
        self.wrapped.IncludeBearingElements = bool(value) if value else False

    @property
    def include_bearing_inner_race(self) -> 'bool':
        """bool: 'IncludeBearingInnerRace' is the original name of this property."""

        temp = self.wrapped.IncludeBearingInnerRace

        if temp is None:
            return False

        return temp

    @include_bearing_inner_race.setter
    def include_bearing_inner_race(self, value: 'bool'):
        self.wrapped.IncludeBearingInnerRace = bool(value) if value else False

    @property
    def include_bearing_outer_race(self) -> 'bool':
        """bool: 'IncludeBearingOuterRace' is the original name of this property."""

        temp = self.wrapped.IncludeBearingOuterRace

        if temp is None:
            return False

        return temp

    @include_bearing_outer_race.setter
    def include_bearing_outer_race(self, value: 'bool'):
        self.wrapped.IncludeBearingOuterRace = bool(value) if value else False

    @property
    def number_of_points_per_cycloidal_disc_half_lobe(self) -> 'int':
        """int: 'NumberOfPointsPerCycloidalDiscHalfLobe' is the original name of this property."""

        temp = self.wrapped.NumberOfPointsPerCycloidalDiscHalfLobe

        if temp is None:
            return 0

        return temp

    @number_of_points_per_cycloidal_disc_half_lobe.setter
    def number_of_points_per_cycloidal_disc_half_lobe(self, value: 'int'):
        self.wrapped.NumberOfPointsPerCycloidalDiscHalfLobe = int(value) if value else 0

    def export_to_stp(self, file_name: 'str'):
        """ 'ExportToSTP' is the original name of this method.

        Args:
            file_name (str)
        """

        file_name = str(file_name)
        self.wrapped.ExportToSTP(file_name if file_name else '')

    def save_stl_to_separate_files(self, directory_path: 'str', save_in_sub_folders: 'bool'):
        """ 'SaveStlToSeparateFiles' is the original name of this method.

        Args:
            directory_path (str)
            save_in_sub_folders (bool)
        """

        directory_path = str(directory_path)
        save_in_sub_folders = bool(save_in_sub_folders)
        self.wrapped.SaveStlToSeparateFiles(directory_path if directory_path else '', save_in_sub_folders if save_in_sub_folders else False)

    def to_stl_code(self) -> 'str':
        """ 'ToSTLCode' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.ToSTLCode()
        return method_result
