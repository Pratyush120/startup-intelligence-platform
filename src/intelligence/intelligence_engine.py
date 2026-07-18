"""
Central Intelligence Engine
"""

from src.intelligence.registry import InterpreterRegistry


class IntelligenceEngine:

    def __init__(self):

        self.interpreters = InterpreterRegistry().load()

    def process(self, record):

        events = []

        for interpreter in self.interpreters:

            detected_events = interpreter.interpret(record)

            if detected_events:

                events.extend(detected_events)

        return events

    def process_many(self, records):

        all_events = []

        for record in records:

            all_events.extend(

                self.process(record)

            )

        return all_events