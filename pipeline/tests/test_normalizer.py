from pipeline.normalizer import DataNormalizer

def test_cpf_validation():
    # CPF válido real ou gerado
    assert DataNormalizer.validate_cpf("52998224725") == True
    assert DataNormalizer.validate_cpf("11111111111") == False

def test_cnpj_validation():
    # CNPJ válido da Receita (apenas exemplo)
    assert DataNormalizer.validate_cnpj("00000000000191") == True
    assert DataNormalizer.validate_cnpj("11111111111111") == False

def test_normalize_phone():
    assert DataNormalizer.normalize_phone("11999999999") == "+5511999999999"
    
def test_normalize_email():
    assert DataNormalizer.normalize_email(" Teste@EMAIL.com ") == "teste@email.com"
