import re
from typing import Dict, Any

class DataCleaner:
    """Classe para limpeza básica de dados e remoção de sujeira (tags HTML, espaços extras)."""
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.IGNORECASE)
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
        
    @staticmethod
    def remove_special_chars(text: str) -> str:
        return re.sub(r'[^\w\s]', '', text)
        
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        return " ".join(text.split())
        
    @classmethod
    def clean_text(cls, text: str) -> str:
        if not isinstance(text, str):
            return text
        text = cls.remove_html_tags(text)
        text = cls.normalize_whitespace(text)
        return text
        
    @classmethod
    def clean_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Limpa recursivamente todos os valores string de um dicionário."""
        cleaned = {}
        for k, v in data.items():
            if isinstance(v, dict):
                cleaned[k] = cls.clean_dict(v)
            elif isinstance(v, list):
                cleaned[k] = [cls.clean_dict(i) if isinstance(i, dict) else cls.clean_text(i) if isinstance(i, str) else i for i in v]
            elif isinstance(v, str):
                cleaned[k] = cls.clean_text(v)
            else:
                cleaned[k] = v
        return cleaned
