import logging
from typing import Dict, Any
from .profile_analyzer import ProfileAnalyzerAgent
from .lead_scorer import LeadScorerAgent

logger = logging.getLogger(__name__)

class ScoringEngine:
    """Orquestrador dos agentes de IA."""
    
    def __init__(self):
        self.analyzer = ProfileAnalyzerAgent()
        self.scorer = LeadScorerAgent()
        # self.redis = Redis() para cache em produção
        
    async def score_lead(self, enriched_profile: Dict[str, Any], icp_config: Dict[str, Any]) -> Dict[str, Any]:
        """Coordena a análise e pontuação do lead."""
        try:
            # Em produção, checaríamos o cache aqui
            insights = await self.analyzer.analyze(enriched_profile)
            score_result = await self.scorer.score(insights, icp_config)
            
            return {
                "insights": insights,
                "scoring": score_result
            }
        except Exception as e:
            logger.error(f"Erro ao processar AI Scoring: {e}")
            return {"error": "Failed to analyze and score lead"}
