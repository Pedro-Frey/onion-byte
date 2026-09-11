"""Módulo de crawlers para coleta de dados públicos."""
from crawlers.base import BaseCrawler
from crawlers.google_search import GoogleSearchCrawler
from crawlers.receita_federal import ReceitaFederalCrawler
from crawlers.reclame_aqui import ReclameAquiCrawler
from crawlers.social_media import SocialMediaCrawler

__all__ = [
    "BaseCrawler",
    "GoogleSearchCrawler", 
    "ReceitaFederalCrawler",
    "ReclameAquiCrawler",
    "SocialMediaCrawler",
]
