import urllib.parse
from typing import Any
from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler, CrawlerError

class ReclameAquiCrawler(BaseCrawler):
    """Crawler para buscar a reputação de uma empresa no Reclame Aqui.
    
    Nota: O Reclame Aqui é um site heavily baseado em JavaScript. 
    Para produção, o ideal é utilizar Playwright ou uma solução headless similar.
    Esta implementação usa aiohttp básico para busca inicial.
    """

    def __init__(self):
        super().__init__(name="reclame_aqui", base_url="https://www.reclameaqui.com.br")

    def _build_search_url(self, company_name: str) -> str:
        """Constrói a URL de busca do Reclame Aqui."""
        encoded_name = urllib.parse.quote(company_name)
        return f"{self.base_url}/busca/?q={encoded_name}"

    def _build_company_url(self, company_slug: str) -> str:
        """Constrói a URL da página da empresa."""
        return f"{self.base_url}/empresa/{company_slug}/"

    async def crawl(self, query: str, **kwargs) -> dict:
        """Busca pela empresa e extrai os dados de reputação."""
        company_name = query
        self.logger.info(f"Buscando reputação para: {company_name}")
        search_url = self._build_search_url(company_name)

        try:
            # Passo 1: Busca a empresa para encontrar o slug
            response = await self._make_request(search_url)
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Nota: O layout do ReclameAqui muda com frequência.
            # Em uma implementação com Playwright, faríamos a interceptação das requisições de API deles
            # ou renderizaríamos o DOM completo. Aqui tentamos encontrar links de empresas.
            
            # Heurística básica para encontrar o slug da empresa: procurar por links que contêm '/empresa/'
            company_link = soup.find("a", href=lambda href: href and "/empresa/" in href)
            
            if not company_link:
                self.logger.warning(f"Empresa não encontrada no Reclame Aqui: {company_name}")
                return {
                    "company_name": company_name,
                    "reputation_score": None,
                    "total_complaints": None,
                    "response_rate": None,
                    "resolution_rate": None,
                    "would_buy_again": None,
                    "status": "Não encontrada",
                    "url": None
                }
                
            href = company_link.get("href")
            # Extrai o slug do formato /empresa/slug-da-empresa/
            parts = href.strip("/").split("/")
            if len(parts) >= 2 and parts[0] == "empresa":
                slug = parts[1]
            else:
                slug = parts[-1]
                
            # Passo 2: Acessa a página da empresa
            company_url = self._build_company_url(slug)
            await self._rate_limit(delay=2.0)
            
            comp_response = await self._make_request(company_url)
            comp_html = await comp_response.text()
            
            return self.parse({
                "html": comp_html,
                "url": company_url,
                "searched_name": company_name
            })
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar reputação de {company_name}: {e}")
            raise CrawlerError(f"Erro ao buscar reputação: {str(e)}") from e

    def parse(self, raw_data: Any) -> dict:
        """Processa a página da empresa e extrai os indicadores."""
        html = raw_data.get("html", "")
        url = raw_data.get("url")
        searched_name = raw_data.get("searched_name", "")
        
        soup = BeautifulSoup(html, "html.parser")
        
        company_name_tag = soup.find("h1")
        company_name = company_name_tag.text.strip() if company_name_tag else searched_name

        score_tag = soup.find(attrs={"data-testid": "company-score"}) or soup.find("span", class_="score")
        reputation_score = None
        if score_tag:
            try:
                reputation_score = float(score_tag.text.strip().replace(",", "."))
            except ValueError:
                pass

        complaints_tag = soup.find(attrs={"data-testid": "company-complaints"}) or soup.find("span", class_="complaints")
        total_complaints = None
        if complaints_tag:
            try:
                total_complaints = int(complaints_tag.text.strip().replace(".", ""))
            except ValueError:
                pass

        resp_tag = soup.find(attrs={"data-testid": "company-response-rate"}) or soup.find("span", class_="response-rate")
        response_rate = resp_tag.text.strip() if resp_tag else None

        res_tag = soup.find(attrs={"data-testid": "company-resolution-rate"}) or soup.find("span", class_="resolution-rate")
        resolution_rate = res_tag.text.strip() if res_tag else None

        buy_tag = soup.find(attrs={"data-testid": "company-would-buy-again"}) or soup.find("span", class_="would-buy-again")
        would_buy_again = buy_tag.text.strip() if buy_tag else None

        status_tag = soup.find(attrs={"data-testid": "company-status"}) or soup.find("span", class_="status")
        status = status_tag.text.strip() if status_tag else "Regular"
        if not status_tag:
            title = soup.find("title")
            if title:
                title_text = title.get_text()
                if "Ótimo" in title_text or "Otimo" in title_text:
                    status = "Ótimo"
                elif "Bom" in title_text:
                    status = "Bom"
                elif "Ruim" in title_text:
                    status = "Ruim"
                elif "Não Recomendada" in title_text:
                    status = "Não Recomendada"

        return {
            "company_name": company_name,
            "reputation_score": reputation_score,
            "total_complaints": total_complaints,
            "response_rate": response_rate,
            "resolution_rate": resolution_rate,
            "would_buy_again": would_buy_again,
            "status": status,
            "url": url,
        }
