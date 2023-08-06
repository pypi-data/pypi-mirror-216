"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2511 import BoostPressureInputOptions
    from ._2512 import InputPowerInputOptions
    from ._2513 import PressureRatioInputOptions
    from ._2514 import RotorSetDataInputFileOptions
    from ._2515 import RotorSetMeasuredPoint
    from ._2516 import RotorSpeedInputOptions
    from ._2517 import SuperchargerMap
    from ._2518 import SuperchargerMaps
    from ._2519 import SuperchargerRotorSet
    from ._2520 import SuperchargerRotorSetDatabase
    from ._2521 import YVariableForImportedData
