"""_165.py

FEExportFormat
"""


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FE_EXPORT_FORMAT = python_net_import('SMT.MastaAPI.NodalAnalysis.FeExportUtility', 'FEExportFormat')


__docformat__ = 'restructuredtext en'
__all__ = ('FEExportFormat',)


class FEExportFormat(Enum):
    """FEExportFormat

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls):
        return _FE_EXPORT_FORMAT

    ANSYS_APDL_INPUT_FILE = 0
    ANSYS_WORKBENCH_COMMANDS = 1
    ANSYS_APDL_INPUT_FILE_OUTPUT_SUB = 2
    MSC_NASTRAN_BULK_DATA_FILE_OUTPUT_PCH = 3
    SIMCENTER_NASTRAN_BULK_DATA_FILE_OUTPUT_PCH = 4
    MSC_NASTRAN_BULK_DATA_FILE_OUTPUT_OP4_AND_PCH = 5
    SIMCENTER_NASTRAN_BULK_DATA_FILE_OUTPUT_OP4_AND_PCH = 6
    ABAQUS_INPUT_FILE_OUTPUT_MTX = 7
    ABAQUS_INPUT_FILE_OUTPUT_FIL = 8


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


FEExportFormat.__setattr__ = __enum_setattr
FEExportFormat.__delattr__ = __enum_delattr
