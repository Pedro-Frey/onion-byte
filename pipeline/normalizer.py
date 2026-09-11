import re
from datetime import datetime
from typing import Optional

class DataNormalizer:
    """Normaliza e valida formatos de dados como CPF, CNPJ, telefone, email."""
    
    @staticmethod
    def normalize_phone(phone: str) -> str:
        """Formata telefone para E.164 (ex: +55...)."""
        clean = re.sub(r'\D', '', phone)
        if len(clean) == 10 or len(clean) == 11:
            return f"+55{clean}"
        return f"+{clean}" if clean else ""
        
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Verifica o dígito verificador do CPF."""
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
            
        def calc_digit(cpf_str, weight):
            s = sum(int(digit) * w for digit, w in zip(cpf_str, range(weight, 1, -1)))
            rest = s % 11
            return '0' if rest < 2 else str(11 - rest)
            
        return calc_digit(cpf[:9], 10) == cpf[9] and calc_digit(cpf[:10], 11) == cpf[10]

    @staticmethod
    def normalize_cpf(cpf: str) -> Optional[str]:
        if not DataNormalizer.validate_cpf(cpf):
            return None
        c = re.sub(r'\D', '', cpf)
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
        
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """Verifica o dígito verificador do CNPJ."""
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
            
        def calc_digit(cnpj_str, weights):
            s = sum(int(digit) * w for digit, w in zip(cnpj_str, weights))
            rest = s % 11
            return '0' if rest < 2 else str(11 - rest)
            
        d1 = calc_digit(cnpj[:12], [5,4,3,2,9,8,7,6,5,4,3,2])
        d2 = calc_digit(cnpj[:12] + d1, [6,5,4,3,2,9,8,7,6,5,4,3,2])
        return cnpj[-2:] == d1 + d2

    @staticmethod
    def normalize_cnpj(cnpj: str) -> Optional[str]:
        if not DataNormalizer.validate_cnpj(cnpj):
            return None
        c = re.sub(r'\D', '', cnpj)
        return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"
        
    @staticmethod
    def normalize_email(email: str) -> str:
        return email.strip().lower()
        
    @staticmethod
    def normalize_name(name: str) -> str:
        return " ".join(word.capitalize() for word in name.strip().split())
        
    @staticmethod
    def normalize_date(date_str: str) -> Optional[datetime]:
        try:
            # Tenta formatos comuns
            for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    pass
            return None
        except Exception:
            return None
