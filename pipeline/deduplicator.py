from rapidfuzz import fuzz
from typing import List, Dict, Any

class DataDeduplicator:
    """Classe responsável por encontrar e mesclar registros duplicados."""
    
    @staticmethod
    def deduplicate_leads(leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove leads duplicados de uma lista baseando-se em CPF/CNPJ, Email ou nome similar."""
        unique_leads = []
        for lead in leads:
            is_duplicate = False
            for u_lead in unique_leads:
                # Match exato
                if (lead.get("email") and lead.get("email") == u_lead.get("email")) or \
                   (lead.get("cpf") and lead.get("cpf") == u_lead.get("cpf")) or \
                   (lead.get("cnpj") and lead.get("cnpj") == u_lead.get("cnpj")):
                    is_duplicate = True
                    DataDeduplicator.merge_profiles_inplace(u_lead, lead)
                    break
                    
                # Match parcial (fuzzy)
                name1 = lead.get("name", "")
                name2 = u_lead.get("name", "")
                if name1 and name2 and fuzz.ratio(name1.lower(), name2.lower()) > 90:
                    is_duplicate = True
                    DataDeduplicator.merge_profiles_inplace(u_lead, lead)
                    break
                    
            if not is_duplicate:
                unique_leads.append(lead)
                
        return unique_leads
        
    @staticmethod
    def merge_profiles_inplace(target: Dict[str, Any], source: Dict[str, Any]):
        """Mescla campos preenchendo os faltantes no target."""
        for k, v in source.items():
            if not target.get(k):
                target[k] = v
                
    @staticmethod
    def merge_profiles(profile_a: Dict[str, Any], profile_b: Dict[str, Any]) -> Dict[str, Any]:
        """Retorna um novo perfil mesclado."""
        merged = profile_a.copy()
        DataDeduplicator.merge_profiles_inplace(merged, profile_b)
        return merged
