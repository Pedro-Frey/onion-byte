import asyncio
import json
from pipeline.processor import PipelineProcessor
from ai.agents.scoring_engine import ScoringEngine

async def test_enrichment():
    print("Iniciando teste de enriquecimento de lead...")
    
    # Mock data
    original_lead = {
        "name": "empresa de tecnologia ltda",
        "cnpj": "00000000000191",
        "email": " CONTATO@TECH.COM.BR "
    }
    
    crawler_results = {
        "receita_federal": {
            "razao_social": "EMPRESA DE TECNOLOGIA LTDA",
            "status": "ATIVA",
            "socios": ["João", "Maria"]
        }
    }
    
    icp_config = {
        "target_industry": "Tecnologia",
        "min_score": 50
    }
    
    # 1. Pipeline
    processor = PipelineProcessor()
    enriched_profile = processor.process(original_lead, crawler_results)
    print("\nPerfil Enriquecido:")
    print(json.dumps(enriched_profile, indent=2, ensure_ascii=False))
    
    # 2. AI Scoring
    engine = ScoringEngine()
    ai_result = await engine.score_lead(enriched_profile, icp_config)
    print("\nResultado da IA (Scoring):")
    print(json.dumps(ai_result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_enrichment())
