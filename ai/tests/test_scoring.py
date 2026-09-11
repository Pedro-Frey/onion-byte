import pytest
from ai.agents.scoring_engine import ScoringEngine

@pytest.mark.asyncio
async def test_scoring_engine():
    engine = ScoringEngine()
    profile = {"name": "João", "company_name": "Empresa X"}
    icp = {"target_industry": "Tech"}
    
    result = await engine.score_lead(profile, icp)
    assert "insights" in result
    assert "scoring" in result
    assert "score" in result["scoring"]
    assert result["scoring"]["grade"] in ["A", "B", "C", "D", "F"]
