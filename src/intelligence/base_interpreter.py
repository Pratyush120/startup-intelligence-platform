"""
Base Interpreter

Every interpreter must inherit this class.
"""

from abc import ABC, abstractmethod

from src.models.events.business_event import BusinessEvent


class BaseInterpreter(ABC):

    @abstractmethod
    def interpret(self, record) -> list[BusinessEvent]:
        """
        Returns one or more business events.
        """
        pass