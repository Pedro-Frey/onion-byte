import re
from typing import Any

from crawlers.base import BaseCrawler, CrawlerError

class ReceitaFederalCrawler(BaseCrawler):
    """Crawler para buscar dados de empresas por CNPJ em APIs públicas."""

    def __init__(self):
        super().__init__(name="receita_federal", base_url="https://brasilapi.com.br")
        self.primary_api = "https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        self.fallback_api = "https://receitaws.com.br/v1/cnpj/{cnpj}"

    def _clean_cnpj(self, cnpj: str) -> str:
        """Remove formatação do CNPJ, retornando apenas números."""
        return re.sub(r"[^\d]", "", cnpj)

    def _validate_cnpj(self, cnpj: str) -> bool:
        """Valida o CNPJ usando o algoritmo de dígitos verificadores."""
        cleaned = self._clean_cnpj(cnpj)
        if len(cleaned) != 14:
            return False

        if cleaned == cleaned[0] * 14:
            return False

        def calc_digit(cnpj_str: str, weights: list[int]) -> int:
            total = sum(int(digit) * weight for digit, weight in zip(cnpj_str, weights))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder

        weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        digit_1 = calc_digit(cleaned[:12], weights_1)
        if int(cleaned[12]) != digit_1:
            return False

        weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        digit_2 = calc_digit(cleaned[:13], weights_2)
        if int(cleaned[13]) != digit_2:
            return False

        return True

    async def crawl(self, query: str, **kwargs) -> dict:
        """Busca dados da empresa usando o CNPJ."""
        cnpj = query
        cleaned_cnpj = self._clean_cnpj(cnpj)
        if not self._validate_cnpj(cleaned_cnpj):
            self.logger.warning(f"CNPJ inválido: {cnpj}")
            raise CrawlerError(f"CNPJ inválido: {cnpj}")

        self.logger.info(f"Buscando dados para o CNPJ: {cleaned_cnpj}")

        # Tenta a API primária
        try:
            url = self.primary_api.format(cnpj=cleaned_cnpj)
            response = await self._make_request(url)
            data = await response.json()
            return self.parse(data, source="brasilapi")
        except Exception as e:
            self.logger.warning(f"Falha na API primária para o CNPJ {cleaned_cnpj}: {e}. Tentando fallback...")

        # Tenta a API de fallback
        try:
            await self._rate_limit(delay=3.0) # ReceitaWS tem limite mais estrito de rate
            url = self.fallback_api.format(cnpj=cleaned_cnpj)
            response = await self._make_request(url)
            data = await response.json()
            
            if data.get("status") == "ERROR":
                raise CrawlerError(f"Erro na ReceitaWS: {data.get('message')}")
                
            return self.parse(data, source="receitaws")
        except Exception as e:
            self.logger.error(f"Falha na API de fallback para o CNPJ {cleaned_cnpj}: {e}")
            raise CrawlerError(f"Não foi possível obter dados para o CNPJ {cleaned_cnpj}") from e

    def parse(self, raw_data: Any, source: str = "brasilapi") -> dict:
        """Processa e padroniza a resposta das diferentes APIs."""
        if source == "brasilapi":
            cnae_principal = raw_data.get("cnae_fiscal", "")
            cnae_desc = raw_data.get("cnae_fiscal_descricao", "")
            
            socios = []
            for socio in raw_data.get("qsa", []):
                socios.append({
                    "nome": socio.get("nome_socio", ""),
                    "qualificacao": socio.get("qualificacao_socio", "")
                })

            return {
                "razao_social": raw_data.get("razao_social", ""),
                "nome_fantasia": raw_data.get("nome_fantasia", ""),
                "cnpj": raw_data.get("cnpj", ""),
                "situacao_cadastral": raw_data.get("descricao_situacao_cadastral", ""),
                "data_abertura": raw_data.get("data_inicio_atividade", ""),
                "natureza_juridica": raw_data.get("natureza_juridica", ""),
                "atividade_principal": {
                    "codigo": str(cnae_principal),
                    "descricao": cnae_desc
                },
                "endereco": {
                    "logradouro": raw_data.get("logradouro", ""),
                    "bairro": raw_data.get("bairro", ""),
                    "municipio": raw_data.get("municipio", ""),
                    "uf": raw_data.get("uf", ""),
                    "cep": raw_data.get("cep", "")
                },
                "socios": socios,
                "capital_social": raw_data.get("capital_social", 0.0),
                "porte": raw_data.get("porte", "")
            }
        else: # receitaws
            atividades = raw_data.get("atividade_principal", [{}])
            cnae = atividades[0] if atividades else {}
            
            socios = []
            for socio in raw_data.get("qsa", []):
                socios.append({
                    "nome": socio.get("nome", ""),
                    "qualificacao": socio.get("qual", "")
                })

            return {
                "razao_social": raw_data.get("nome", ""),
                "nome_fantasia": raw_data.get("fantasia", ""),
                "cnpj": raw_data.get("cnpj", "").replace(".", "").replace("/", "").replace("-", ""),
                "situacao_cadastral": raw_data.get("situacao", ""),
                "data_abertura": raw_data.get("abertura", ""),
                "natureza_juridica": raw_data.get("natureza_juridica", ""),
                "atividade_principal": {
                    "codigo": cnae.get("code", "").replace(".", "").replace("-", ""),
                    "descricao": cnae.get("text", "")
                },
                "endereco": {
                    "logradouro": raw_data.get("logradouro", ""),
                    "bairro": raw_data.get("bairro", ""),
                    "municipio": raw_data.get("municipio", ""),
                    "uf": raw_data.get("uf", ""),
                    "cep": raw_data.get("cep", "").replace("-", "")
                },
                "socios": socios,
                "capital_social": float(raw_data.get("capital_social", "0").replace(",", ".")) if isinstance(raw_data.get("capital_social"), str) else raw_data.get("capital_social", 0.0),
                "porte": raw_data.get("porte", "")
            }
