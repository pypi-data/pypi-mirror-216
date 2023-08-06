"""_2199.py

OptimizationStrategyDatabase
"""


from mastapy.utility.databases import _1794
from mastapy.system_model.optimization import _2191
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'OptimizationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationStrategyDatabase',)


class OptimizationStrategyDatabase(_1794.NamedDatabase['_2191.CylindricalGearOptimisationStrategy']):
    """OptimizationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _OPTIMIZATION_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'OptimizationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
