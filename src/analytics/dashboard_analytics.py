"""
Dashboard Analytics

Transforms raw data into business-ready dashboard insights.
"""

from src.services.data_service import DataService


class DashboardAnalytics:

    def __init__(self):

        self.service = DataService()

    # -----------------------------------------------------

    def overview(self):

        summary = self.service.get_dashboard_summary()

        return {

            "summary": summary,

            "companies": self.service.get_top_companies_df(10),

            "events": self.service.get_recent_events_df(15),

            "distribution": self.service.get_event_breakdown_df(),

            "funding": self.service.get_top_funding_df(10)

        }

    # -----------------------------------------------------

    def close(self):

        self.service.close()