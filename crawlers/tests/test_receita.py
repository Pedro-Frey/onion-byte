import pytest
from crawlers.receita_federal import ReceitaFederalCrawler

@pytest.mark.asyncio
async def test_receita_federal_parse():
    crawler = ReceitaFederalCrawler()
    mock_data = {
        "razao_social": "EMPRESA TESTE S/A",
        "cnpj": "12345678000199",
        "descricao_situacao_cadastral": "ATIVA"
    }
    result = crawler.parse(mock_data)
    assert result["razao_social"] == "EMPRESA TESTE S/A"
    assert result["cnpj"] == "12345678000199"
    assert result["situacao_cadastral"] == "ATIVA"
