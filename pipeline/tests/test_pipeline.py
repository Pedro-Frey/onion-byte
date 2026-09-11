from pipeline.processor import PipelineProcessor

def test_pipeline_processor():
    processor = PipelineProcessor()
    original = {
        "name": " joão SILVA ",
        "email": "JOAO@empresa.COM",
        "phone": "(11) 98888-7777",
        "cpf": "52998224725"
    }
    crawler_results = {
        "receita_federal": {
            "razao_social": "JOAO SILVA LTDA",
            "status": "ATIVA"
        }
    }
    
    result = processor.process(original, crawler_results)
    
    assert result["name"] == "João Silva"
    assert result["email"] == "joao@empresa.com"
    assert result["phone"] == "+5511988887777"
    assert result["company_name"] == "Joao Silva Ltda"
    assert result["company_status"] == "ATIVA"
