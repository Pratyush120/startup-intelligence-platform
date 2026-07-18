"""
Interpreter Registry

Registers all available business interpreters.
"""

from src.intelligence.interpreters.funding import FundingInterpreter
from src.intelligence.interpreters.hiring import HiringInterpreter
from src.intelligence.interpreters.layoff import LayoffInterpreter
from src.intelligence.interpreters.expansion import ExpansionInterpreter
from src.intelligence.interpreters.acquisition import AcquisitionInterpreter


class InterpreterRegistry:

    def load(self):

        return [

            FundingInterpreter(),

            HiringInterpreter(),

            LayoffInterpreter(),

            ExpansionInterpreter(),

            AcquisitionInterpreter()

        ]