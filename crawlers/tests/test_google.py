import pytest
from crawlers.google_search import GoogleSearchCrawler

@pytest.mark.asyncio
async def test_google_search_parse():
    crawler = GoogleSearchCrawler()
    html_mock = '''
    <div class="g">
        <h3>Test Title</h3>
        <a href="https://example.com">Link</a>
        <div class="VwiC3b">Test Snippet</div>
    </div>
    '''
    result = crawler.parse(html_mock)
    assert len(result["results"]) == 1
    assert result["results"][0]["title"] == "Test Title"
    assert result["results"][0]["url"] == "https://example.com"
