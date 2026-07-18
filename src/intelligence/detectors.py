from abc import ABC, abstractmethod

from src.models.events.business_event import BusinessEvent


class EventDetector(ABC):
    @abstractmethod
    def detect(self, record) -> list[BusinessEvent]:
        pass
