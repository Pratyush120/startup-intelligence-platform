"""
Contract Tests for API Serializer

Ensures every serializer function produces output matching
the frontend TypeScript interfaces.
"""

import unittest
import json
from src.pipeline.api_serializer import (
    serialize_executive_brief,
    serialize_metric_cards,
    serialize_company_metrics,
    serialize_market_snapshots,
    serialize_strategic_alerts,
    serialize_timeline_events,
    serialize_recommendations,
)


class TestExecutiveBriefSerializer(unittest.TestCase):
    def test_has_required_keys(self):
        result = serialize_executive_brief(
            brief_id="test",
            market_health_score=82.5,
            investment_climate="Favorable",
            risk_level="Medium",
            growth_outlook="Accelerating",
            strategic_summary="Test summary.",
            confidence_score=0.94,
            primary_recommendation="Test recommendation.",
        )
        required_keys = {
            "id",
            "date",
            "marketHealthScore",
            "investmentClimate",
            "riskLevel",
            "growthOutlook",
            "strategicSummary",
            "confidenceScore",
            "primaryRecommendation",
        }
        self.assertEqual(set(result.keys()), required_keys)

    def test_confidence_is_percentage(self):
        result = serialize_executive_brief(
            brief_id="1",
            market_health_score=50,
            investment_climate="Neutral",
            risk_level="Low",
            growth_outlook="Stable",
            strategic_summary="s",
            confidence_score=0.88,
            primary_recommendation="r",
        )
        self.assertEqual(result["confidenceScore"], 88.0)

    def test_market_health_rounded(self):
        result = serialize_executive_brief(
            brief_id="1",
            market_health_score=72.456,
            investment_climate="Favorable",
            risk_level="Medium",
            growth_outlook="Accelerating",
            strategic_summary="s",
            confidence_score=0.9,
            primary_recommendation="r",
        )
        self.assertEqual(result["marketHealthScore"], 72.5)


class TestMetricCardsSerializer(unittest.TestCase):
    def test_returns_four_cards(self):
        result = serialize_metric_cards(
            total_companies=100,
            funding_today=3_400_000_000,
            total_events=250,
            market_health=80.0,
            avg_confidence=0.9,
            companies_sparkline=[50] * 5,
            funding_sparkline=[50] * 5,
            events_sparkline=[50] * 5,
            health_sparkline=[50] * 5,
        )
        self.assertEqual(len(result), 4)

    def test_each_card_has_required_keys(self):
        result = serialize_metric_cards(
            total_companies=10,
            funding_today=1_000_000,
            total_events=5,
            market_health=50,
            avg_confidence=0.7,
            companies_sparkline=[1] * 5,
            funding_sparkline=[1] * 5,
            events_sparkline=[1] * 5,
            health_sparkline=[1] * 5,
        )
        required_keys = {
            "id",
            "label",
            "value",
            "trend",
            "trendLabel",
            "sparkline",
            "iconType",
        }
        for card in result:
            self.assertTrue(
                required_keys.issubset(set(card.keys())), f"Missing keys in {card}"
            )

    def test_sparkline_length(self):
        sparkline = [10.0, 20.0, 30.0, 40.0, 50.0]
        result = serialize_metric_cards(
            total_companies=10,
            funding_today=0,
            total_events=0,
            market_health=50,
            avg_confidence=0.7,
            companies_sparkline=sparkline,
            funding_sparkline=sparkline,
            events_sparkline=sparkline,
            health_sparkline=sparkline,
        )
        for card in result:
            self.assertEqual(len(card["sparkline"]), 5)


class TestCompanyMetricsSerializer(unittest.TestCase):
    def test_trend_direction_values(self):
        class MockCompany:
            company_name = "TestCo"
            business_health = 90.0
            momentum_score = 80
            total_funding = 1000000
            growth_score = 85
            risk_score = 15
            recommendation = "Strong Buy"

        result = serialize_company_metrics([MockCompany()], {})
        self.assertIn(result[0]["trendDirection"], ["up", "down", "flat"])


class TestMarketSnapshotsSerializer(unittest.TestCase):
    def test_output_structure(self):
        rows = [
            {
                "date": "2026-01-01",
                "funding_amount": 500_000_000,
                "hiring_events": 10,
                "layoff_events": 2,
            }
        ]
        result = serialize_market_snapshots(rows)
        self.assertEqual(len(result), 1)
        self.assertIn("fundingAmount", result[0])
        self.assertIn("hiringEvents", result[0])
        self.assertIn("layoffEvents", result[0])


class TestStrategicAlertsSerializer(unittest.TestCase):
    def test_output_structure(self):
        rows = [
            {
                "alert_id": 1,
                "title": "Test Alert",
                "impact": "High impact",
                "confidence": 0.95,
                "company_name": "TestCo",
                "category": "Funding",
                "recommendation": "Act now",
                "timestamp": "2026-01-01T00:00:00Z",
                "priority": "Critical",
            }
        ]
        result = serialize_strategic_alerts(rows)
        self.assertEqual(result[0]["priority"], "Critical")
        self.assertEqual(result[0]["confidence"], 95)


class TestTimelineEventsSerializer(unittest.TestCase):
    def test_importance_mapping(self):
        events = [
            {
                "company_name": "A",
                "event_type": "Funding",
                "published_at": "2026-01-01",
                "title": "t",
                "importance_score": 9.0,
            },
            {
                "company_name": "B",
                "event_type": "Hiring",
                "published_at": "2026-01-01",
                "title": "t",
                "importance_score": 3.0,
            },
        ]
        result = serialize_timeline_events(events)
        self.assertEqual(result[0]["importance"], "Critical")
        self.assertEqual(result[1]["importance"], "Low")


class TestRecommendationsSerializer(unittest.TestCase):
    def test_output_structure(self):
        rows = [
            {
                "rec_id": 1,
                "title": "Test Rec",
                "reason": "Because",
                "evidence_list": json.dumps(["Evidence 1"]),
                "confidence": 0.88,
                "suggested_action": "Do this",
                "priority": "High",
                "strategic_impact": "Big",
                "opportunity_est": "$50M",
                "risk_est": "Low",
                "generated_at": "2026-01-01T00:00:00Z",
                "evidence_score": 92.0,
                "related_companies": json.dumps(["CompanyA"]),
                "related_event_ids": json.dumps(["e1"]),
            }
        ]
        result = serialize_recommendations(rows)
        self.assertEqual(result[0]["confidence"], 88)
        self.assertEqual(result[0]["relatedCompanies"], ["CompanyA"])


if __name__ == "__main__":
    unittest.main()
