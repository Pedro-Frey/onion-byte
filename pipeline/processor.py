from typing import Dict, Any
from .cleaner import DataCleaner
from .normalizer import DataNormalizer
from .deduplicator import DataDeduplicator
from .consolidator import ProfileConsolidator

class PipelineProcessor:
    """Orquestrador do pipeline de dados."""
    
    def __init__(self):
        self.cleaner = DataCleaner()
        self.normalizer = DataNormalizer()
        self.deduplicator = DataDeduplicator()
        self.consolidator = ProfileConsolidator()
        
    def process(self, original_data: Dict[str, Any], crawler_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Executa toda a cadeia: limpar, normalizar, consolidar."""
        # 1. Limpeza
        clean_original = self.cleaner.clean_dict(original_data)
        
        # 2. Normalização
        if "cpf" in clean_original:
            clean_original["cpf"] = self.normalizer.normalize_cpf(clean_original["cpf"])
        if "cnpj" in clean_original:
            clean_original["cnpj"] = self.normalizer.normalize_cnpj(clean_original["cnpj"])
        if "phone" in clean_original:
            clean_original["phone"] = self.normalizer.normalize_phone(clean_original["phone"])
        if "email" in clean_original:
            clean_original["email"] = self.normalizer.normalize_email(clean_original["email"])
        if "name" in clean_original:
            clean_original["name"] = self.normalizer.normalize_name(clean_original["name"])
            
        # 3. Consolidação com os crawlers (os crawlers já retornam dados tratados/estruturados)
        consolidated = self.consolidator.consolidate(clean_original, crawler_results)
        
        return consolidated
