"""
Dashboard Data Service

Provides business-ready data for the dashboard.

The UI NEVER talks to SQLite directly.
"""

import pandas as pd

from src.database.db import Database


class DataService:
    def __init__(self):

        self.db = Database()

    # =====================================================
    # DASHBOARD SUMMARY
    # =====================================================

    def get_dashboard_summary(self):

        summary = {}

        # --------------------
        # Total Events
        # --------------------

        self.db.execute("""

            SELECT COUNT(*) AS total

            FROM events

        """)

        summary["total_events"] = self.db.fetchone()["total"]

        # --------------------
        # Companies
        # --------------------

        self.db.execute("""

            SELECT COUNT(*) AS total

            FROM companies

        """)

        summary["total_companies"] = self.db.fetchone()["total"]

        # --------------------
        # Funding
        # --------------------

        self.db.execute("""

            SELECT

                COALESCE(SUM(amount),0) AS funding

            FROM events

            WHERE event_type='Funding'

        """)

        summary["total_funding"] = self.db.fetchone()["funding"]

        # --------------------
        # Average Confidence
        # --------------------

        self.db.execute("""

            SELECT

                ROUND(AVG(confidence),2) AS confidence

            FROM events

        """)

        row = self.db.fetchone()

        summary["avg_confidence"] = row["confidence"] if row["confidence"] else 0

        # --------------------
        # Top Source
        # --------------------

        self.db.execute("""

            SELECT

                source,

                COUNT(*) total

            FROM events

            GROUP BY source

            ORDER BY total DESC

            LIMIT 1

        """)

        row = self.db.fetchone()

        if row:
            summary["top_source"] = row["source"]

        else:
            summary["top_source"] = "N/A"

        return summary

    # =====================================================
    # TOP COMPANIES
    # =====================================================

    def get_top_companies_df(self, limit=10):

        self.db.execute(
            """

            SELECT

                company_name,

                momentum_score,

                latest_funding,

                funding_events,

                hiring_events,

                layoff_events,

                expansion_events,

                acquisition_events

            FROM companies

            ORDER BY momentum_score DESC

            LIMIT ?

        """,
            (limit,),
        )

        rows = self.db.fetchall()

        return pd.DataFrame([dict(x) for x in rows])

    # =====================================================
    # RECENT EVENTS
    # =====================================================

    def get_recent_events_df(self, limit=20):

        self.db.execute(
            """

            SELECT

                company_name,

                event_type,

                title,

                source,

                confidence,

                impact_score,

                published_at

            FROM events

            ORDER BY event_id DESC

            LIMIT ?

        """,
            (limit,),
        )

        rows = self.db.fetchall()

        return pd.DataFrame([dict(x) for x in rows])

    # =====================================================
    # EVENT BREAKDOWN
    # =====================================================

    def get_event_breakdown_df(self):

        self.db.execute("""

            SELECT

                event_type,

                COUNT(*) AS total

            FROM events

            GROUP BY event_type

            ORDER BY total DESC

        """)

        rows = self.db.fetchall()

        return pd.DataFrame([dict(x) for x in rows])

    # =====================================================
    # FUNDING LEADERBOARD
    # =====================================================

    def get_top_funding_df(self, limit=10):

        self.db.execute(
            """

            SELECT

                company_name,

                amount,

                currency,

                funding_round

            FROM events

            WHERE event_type='Funding'

            ORDER BY amount DESC

            LIMIT ?

        """,
            (limit,),
        )

        rows = self.db.fetchall()

        return pd.DataFrame([dict(x) for x in rows])

    # =====================================================
    # COMPANY PROFILE
    # =====================================================

    def get_company_profile(self, company):

        self.db.execute(
            """

            SELECT *

            FROM companies

            WHERE company_name=?

        """,
            (company,),
        )

        row = self.db.fetchone()

        if row:
            return dict(row)

        return None

    # =====================================================
    # COMPANY EVENTS
    # =====================================================

    def get_company_events_df(self, company):

        self.db.execute(
            """

            SELECT

                event_type,

                title,

                source,

                confidence,

                impact_score,

                published_at

            FROM events

            WHERE company_name=?

            ORDER BY published_at DESC

        """,
            (company,),
        )

        rows = self.db.fetchall()

        return pd.DataFrame([dict(x) for x in rows])

    # =====================================================
    # ALL COMPANIES
    # =====================================================

    def get_company_list(self):

        self.db.execute("""

            SELECT company_name

            FROM companies

            ORDER BY company_name

        """)

        return [row["company_name"] for row in self.db.fetchall()]

    # =====================================================

    def close(self):

        self.db.close()
