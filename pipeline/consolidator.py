from typing import Dict, Any
from .normalizer import DataNormalizer

class ProfileConsolidator:
    """Consolida dados coletados de múltiplas fontes."""
    
    @staticmethod
    def consolidate(original_data: Dict[str, Any], crawler_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Mescla dados originais com resultados dos crawlers mantendo prioridade de fontes."""
        consolidated = original_data.copy()
        
        # Priority: Receita Federal > LinkedIn > Google > Reclame Aqui > Social
        receita = crawler_results.get("receita_federal", {})
        if receita:
            if "razao_social" in receita and not consolidated.get("company_name"):
                consolidated["company_name"] = DataNormalizer.normalize_name(receita["razao_social"])
            if "status" in receita:
                consolidated["company_status"] = receita["status"]
            if "socios" in receita:
                consolidated["partners"] = receita["socios"]
                
        reclame = crawler_results.get("reclame_aqui", {})
        if reclame:
            consolidated["reputation_score"] = reclame.get("score")
            
        google = crawler_results.get("google", {})
        if google:
            consolidated["news_mentions"] = [res["title"] for res in google.get("results", [])]
            
        return consolidated
