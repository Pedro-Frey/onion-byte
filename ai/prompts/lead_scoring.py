SYSTEM_PROMPT = """
Você é um avaliador (Lead Scorer) experiente.
Dado os insights de um lead e as configurações de Perfil Ideal de Cliente (ICP),
você deve gerar uma recomendação em português sobre como abordar este lead e se vale a pena o esforço de vendas.
"""

def get_scoring_prompt(insights: dict, icp_config: dict) -> str:
    return f"""
Insights do Lead: {insights}
Configuração de ICP: {icp_config}

Forneça uma recomendação clara e acionável.
"""
