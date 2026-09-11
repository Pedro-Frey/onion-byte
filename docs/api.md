# Documentação da API (FastAPI)

## `POST /api/v1/leads/enrich`
Envia um lead para enriquecimento.

**Request Body:**
```json
{
  "name": "João Silva",
  "email": "joao@exemplo.com",
  "cpf": "111.222.333-44",
  "company_name": "Exemplo LTDA"
}
```

**Response:**
```json
{
  "lead_id": "uuid",
  "enriched_data": {
    "company_status": "ATIVA",
    "reputation_score": 8.5
  },
  "scoring": {
    "score": 85.5,
    "grade": "A",
    "recommendation": "Lead altamente qualificado."
  }
}
```
