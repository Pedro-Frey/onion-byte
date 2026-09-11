import abc
import asyncio
import logging
import random
import urllib.robotparser
from typing import Any, Optional
from urllib.parse import urlparse

import aiohttp
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential, retry_if_exception_type


class CrawlerError(Exception):
    """Exceção base para erros nos crawlers."""
    pass


class BaseCrawler(abc.ABC):
    """Classe base abstrata para todos os crawlers do projeto."""

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    ]

    def __init__(self, name: str, base_url: str, timeout: int = 30, max_retries: int = 3):
        self.name = name
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(f"crawler.{self.name}")
        self._robot_parser = urllib.robotparser.RobotFileParser()
        self._robot_parsed_urls = set()

    @abc.abstractmethod
    async def crawl(self, query: str, **kwargs) -> dict:
        """Executa a coleta de dados."""
        pass

    @abc.abstractmethod
    def parse(self, raw_data: Any) -> dict:
        """Processa e formata os dados coletados."""
        pass

    def validate(self, data: dict, required_keys: Optional[list[str]] = None) -> bool:
        """Valida se o dicionário de saída contém as chaves obrigatórias."""
        if not required_keys:
            return True
        return all(key in data for key in required_keys)

    def _get_headers(self) -> dict:
        """Retorna cabeçalhos HTTP com um User-Agent aleatório."""
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    def _check_robots_txt(self, url: str) -> bool:
        """Verifica se a URL é permitida pelo robots.txt do domínio."""
        parsed_url = urlparse(url)
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = f"{base_domain}/robots.txt"

        if base_domain not in self._robot_parsed_urls:
            try:
                self._robot_parser.set_url(robots_url)
                self._robot_parser.read()
                self._robot_parsed_urls.add(base_domain)
            except Exception as e:
                self.logger.warning(f"Falha ao ler robots.txt de {base_domain}: {e}")
                return True

        return self._robot_parser.can_fetch("*", url)

    async def _rate_limit(self, delay: float = 1.0):
        """Aplica um atraso para evitar bloqueios por rate limit."""
        await asyncio.sleep(delay)

    async def _make_request(self, url: str, method: str = 'GET', **kwargs) -> aiohttp.ClientResponse:
        """Método centralizado para requisições HTTP com retry e timeout."""
        if not self._check_robots_txt(url):
            self.logger.warning(f"URL bloqueada pelo robots.txt: {url}")
            raise CrawlerError(f"Acesso bloqueado por robots.txt: {url}")

        headers = kwargs.pop("headers", self._get_headers())
        client_timeout = aiohttp.ClientTimeout(total=self.timeout)

        async def _do_request():
            async with aiohttp.ClientSession(timeout=client_timeout) as session:
                async with session.request(method, url, headers=headers, **kwargs) as response:
                    response.raise_for_status()
                    await response.read()
                    return response

        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential(multiplier=1, min=2, max=10),
                retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError))
            ):
                with attempt:
                    self.logger.debug(f"Iniciando requisição {method} para {url} (tentativa {attempt.retry_state.attempt_number})")
                    return await _do_request()
        except Exception as e:
            self.logger.error(f"Erro ao fazer requisição para {url}: {e}")
            raise CrawlerError(f"Falha na requisição: {str(e)}") from e
