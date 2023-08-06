"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5599 import AbstractDesignStateLoadCaseGroup
    from ._5600 import AbstractLoadCaseGroup
    from ._5601 import AbstractStaticLoadCaseGroup
    from ._5602 import ClutchEngagementStatus
    from ._5603 import ConceptSynchroGearEngagementStatus
    from ._5604 import DesignState
    from ._5605 import DutyCycle
    from ._5606 import GenericClutchEngagementStatus
    from ._5607 import LoadCaseGroupHistograms
    from ._5608 import SubGroupInSingleDesignState
    from ._5609 import SystemOptimisationGearSet
    from ._5610 import SystemOptimiserGearSetOptimisation
    from ._5611 import SystemOptimiserTargets
    from ._5612 import TimeSeriesLoadCaseGroup
