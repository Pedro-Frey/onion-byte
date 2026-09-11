from typing import Dict, Any

class LeadScorerAgent:
    """Agente responsável por pontuar e classificar o lead."""
    
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "industry_fit": 0.4,
            "company_stability": 0.3,
            "online_presence_strength": 0.3
        }
        
    async def score(self, insights: Dict[str, Any], icp_config: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula o score de 0 a 100 e atribui um grade (A-F)."""
        
        # Simulação de cálculo baseado em insights
        fit = insights.get("industry_fit", 0.5) * 100
        stability_map = {"High": 100, "Medium": 50, "Low": 0}
        presence_map = {"High": 100, "Medium": 50, "Low": 0}
        
        stability = stability_map.get(insights.get("company_stability", "Medium"), 50)
        presence = presence_map.get(insights.get("online_presence_strength", "Medium"), 50)
        
        final_score = (
            fit * self.weights["industry_fit"] +
            stability * self.weights["company_stability"] +
            presence * self.weights["online_presence_strength"]
        )
        final_score = min(max(final_score, 0), 100)
        
        if final_score >= 80:
            grade = "A"
        elif final_score >= 60:
            grade = "B"
        elif final_score >= 40:
            grade = "C"
        elif final_score >= 20:
            grade = "D"
        else:
            grade = "F"
            
        return {
            "score": round(final_score, 2),
            "grade": grade,
            "breakdown": {
                "industry_fit_score": fit,
                "stability_score": stability,
                "presence_score": presence
            },
            "recommendation": f"O lead possui uma classificação {grade} com score {round(final_score, 2)}."
        }
