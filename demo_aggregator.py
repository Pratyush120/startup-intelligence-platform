import asyncio
from src.database.repository import Repository
from src.services.intelligence_aggregator import IntelligenceAggregator
from src.services.providers.gemini_provider import GeminiProvider


async def test_aggregator():
    repo = Repository()
    agg = IntelligenceAggregator(repo)
    print("Fetching intelligence for 'Apple Inc'...")
    ctx = await agg.build_global_context("Apple Inc")
    print("--- CONTEXT ---")
    print(f"Company: {ctx.get('company')}")
    print(f"Financials: {len(ctx.get('financials', []))} metrics found")
    print(f"Latest News: {len(ctx.get('latest_news', []))} articles found")
    if ctx.get("latest_news"):
        print(
            f"Top News: {ctx['latest_news'][0].title} (Source: {ctx['latest_news'][0].source.provider})"
        )

    print("\n--- GEMINI REASONING ---")
    gemini = GeminiProvider()
    res = gemini.analyze_strategic_context(
        ctx, "What are the latest strategic moves and financial health of Apple?"
    )
    print(res.summary)


if __name__ == "__main__":
    asyncio.run(test_aggregator())
