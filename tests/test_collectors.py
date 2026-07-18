from unittest.mock import patch, MagicMock

from src.collectors.google_news_collector import GoogleNewsCollector
from src.collectors.mock_collector import MockCollector
from src.collectors.newsapi_collector import NewsAPICollector
from src.models.record import Record


def test_mock_collector():
    collector = MockCollector()
    records = collector.collect()
    assert len(records) > 0
    assert isinstance(records[0], Record)
    assert records[0].source == "MockSource"
    assert "OpenAI" in records[0].title


@patch("src.collectors.google_news_collector.feedparser")
def test_google_news_collector(mock_feedparser):
    mock_feed = MagicMock()
    mock_feed.entries = [
        {
            "title": "Startup XYZ gets funded",
            "summary": "Funding news",
            "link": "http://test",
            "published": "2023-01-01",
            "source": {"title": "TechBlog"},
        }
    ]
    mock_feedparser.parse.return_value = mock_feed

    collector = GoogleNewsCollector()
    with patch.object(collector.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.content = b"xml data"
        mock_get.return_value = mock_response
        records = collector.collect()

    assert len(records) == 1
    assert records[0].source == "Google News"
    assert records[0].title == "Startup XYZ gets funded"


def test_newsapi_collector_no_key():
    collector = NewsAPICollector()
    collector.api_key = None
    records = collector.collect()
    assert len(records) == 0


def test_newsapi_collector_with_key():
    collector = NewsAPICollector()
    collector.api_key = "fake_key"

    with patch.object(collector.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "title": "Test AI",
                    "description": "Desc",
                    "url": "url",
                    "publishedAt": "2023",
                    "source": {"name": "WSJ"},
                }
            ],
        }
        mock_get.return_value = mock_response

        records = collector.collect()
        assert len(records) == 1
        assert records[0].title == "Test AI"
        assert records[0].source == "NewsAPI"
