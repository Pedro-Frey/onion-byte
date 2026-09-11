import json
from typing import Dict, Any

SYSTEM_PROMPT = """
Você é um analista de dados especialista em perfis corporativos brasileiros (B2B/B2C).
Sua missão é receber um JSON com informações enriquecidas de um lead e extrair insights estruturados.
Considere fatores como Senioridade, Fit com a indústria, Estabilidade da empresa e Força da presença online.
Responda APENAS com um JSON válido correspondendo ao esquema solicitado.
"""

def get_user_prompt(profile: Dict[str, Any]) -> str:
    return f"""
Por favor, analise o seguinte perfil de lead e forneça os insights:

{json.dumps(profile, indent=2, ensure_ascii=False)}
"""
