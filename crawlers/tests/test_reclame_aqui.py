import pytest
from crawlers.reclame_aqui import ReclameAquiCrawler

@pytest.mark.asyncio
async def test_reclame_aqui_parse():
    crawler = ReclameAquiCrawler()
    mock_html = """
    <html>
      <head><title>Empresa Teste - Reclame Aqui</title></head>
      <body>
        <h1>Empresa Teste</h1>
        <span data-testid="company-score">8.5</span>
        <span data-testid="company-complaints">1.200</span>
        <span data-testid="company-response-rate">98.5%</span>
        <span data-testid="company-resolution-rate">85.0%</span>
        <span data-testid="company-would-buy-again">75.0%</span>
        <span data-testid="company-status">Ótimo</span>
      </body>
    </html>
    """
    mock_data = {
        "html": mock_html,
        "url": "https://www.reclameaqui.com.br/empresa/empresa-teste/",
        "searched_name": "Empresa Teste"
    }
    result = crawler.parse(mock_data)
    assert result["company_name"] == "Empresa Teste"
    assert result["reputation_score"] == 8.5
    assert result["total_complaints"] == 1200
    assert result["response_rate"] == "98.5%"
    assert result["resolution_rate"] == "85.0%"
    assert result["would_buy_again"] == "75.0%"
    assert result["status"] == "Ótimo"
    assert result["url"] == "https://www.reclameaqui.com.br/empresa/empresa-teste/"
