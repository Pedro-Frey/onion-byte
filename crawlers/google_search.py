import urllib.parse
from typing import Any, List, Optional
from bs4 import BeautifulSoup
import aiohttp

from crawlers.base import BaseCrawler

class GoogleSearchCrawler(BaseCrawler):
    """Crawler para buscar informações de leads no Google."""

    def __init__(self, serpapi_key: Optional[str] = None):
        super().__init__(name="google_search", base_url="https://www.google.com")
        self.serpapi_key = serpapi_key

    def build_search_query(self, name: str, company: Optional[str] = None, extra_terms: Optional[List[str]] = None) -> str:
        """Constrói uma query de busca otimizada."""
        query_parts = [f'"{name}"']
        
        if company:
            query_parts.append(f'"{company}"')
            
        if extra_terms:
            query_parts.extend(extra_terms)
            
        return " ".join(query_parts)

    async def crawl(self, query: str, **kwargs) -> dict:
        """Executa a busca no Google."""
        max_results = kwargs.get("max_results", 10)
        self.logger.info(f"Iniciando busca no Google para query: {query}")
        
        try:
            if self.serpapi_key:
                return await self._crawl_serpapi(query, max_results)
            else:
                return await self._crawl_direct(query, max_results)
        except Exception as e:
            self.logger.error(f"Erro durante a busca no Google: {e}")
            return {"results": [], "total_found": 0, "news_mentions": 0, "relevant_domains": [], "error": str(e)}

    async def _crawl_serpapi(self, query: str, max_results: int) -> dict:
        """Realiza busca usando SerpAPI."""
        url = "https://serpapi.com/search.json"
        params = {
            "q": query,
            "api_key": self.serpapi_key,
            "engine": "google",
            "num": max_results,
            "hl": "pt",
            "gl": "br"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return self.parse(data, is_serpapi=True)

    async def _crawl_direct(self, query: str, max_results: int) -> dict:
        """Realiza busca direta fazendo scraping na página do Google."""
        encoded_query = urllib.parse.quote_plus(query)
        url = f"{self.base_url}/search?q={encoded_query}&num={max_results}&hl=pt-BR"
        
        await self._rate_limit(delay=2.0)
        
        response = await self._make_request(url)
        html_content = await response.text()
        return self.parse(html_content, is_serpapi=False)

    def parse(self, raw_data: Any, is_serpapi: bool = False) -> dict:
        """Processa os dados brutos da busca."""
        results = []
        domains = set()
        news_mentions = 0
        
        if is_serpapi:
            organic_results = raw_data.get("organic_results", [])
            for res in organic_results:
                link = res.get("link", "")
                domain = urllib.parse.urlparse(link).netloc
                domains.add(domain)
                
                results.append({
                    "title": res.get("title", ""),
                    "snippet": res.get("snippet", ""),
                    "url": link,
                    "domain": domain
                })
                
                if "noticias" in link or "news" in link:
                    news_mentions += 1
        else:
            soup = BeautifulSoup(raw_data, "html.parser")
            search_divs = soup.find_all("div", class_="g")
            
            for div in search_divs:
                title_elem = div.find("h3")
                link_elem = div.find("a")
                snippet_elem = div.find("div", {"style": "-webkit-line-clamp:2"}) or div.find("div", class_="VwiC3b")
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    link = link_elem.get("href", "")
                    
                    if link.startswith("/url?q="):
                        link = urllib.parse.unquote(link.split("/url?q=")[1].split("&")[0])
                    
                    if not link.startswith("http"):
                        continue
                        
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    domain = urllib.parse.urlparse(link).netloc
                    domains.add(domain)
                    
                    results.append({
                        "title": title,
                        "snippet": snippet,
                        "url": link,
                        "domain": domain
                    })
                    
                    if "noticias" in link or "news" in link:
                        news_mentions += 1

        return {
            "results": results,
            "total_found": len(results),
            "news_mentions": news_mentions,
            "relevant_domains": list(domains)
        }
