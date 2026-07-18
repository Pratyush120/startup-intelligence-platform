from src.intelligence.funding_extractor import FundingExtractor


class BusinessEventEngine:
    def __init__(self):

        self.detectors = [
            FundingExtractor(),
        ]

    def process(self, record):

        events = []

        for detector in self.detectors:
            events.extend(detector.detect(record))

        return events
