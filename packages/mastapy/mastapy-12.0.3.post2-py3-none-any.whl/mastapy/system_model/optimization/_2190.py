"""_2190.py

ConicalGearOptimizationStrategyDatabase
"""


from mastapy.utility.databases import _1794
from mastapy.system_model.optimization import _2188
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_OPTIMIZATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'ConicalGearOptimizationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearOptimizationStrategyDatabase',)


class ConicalGearOptimizationStrategyDatabase(_1794.NamedDatabase['_2188.ConicalGearOptimisationStrategy']):
    """ConicalGearOptimizationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_OPTIMIZATION_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'ConicalGearOptimizationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
