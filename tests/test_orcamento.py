from unittest.mock import patch
import pytest

# Imports ajustados apontando para dentro da sua pasta src
from src.orcamento import buscar_cep, Orcamento


# ==========================================
# 📍 TESTES DA API VIACEP (COM MOCK)
# ==========================================

def test_buscar_cep_sucesso():
    """Valida se a função retorna os dados de endereço corretamente com um CEP válido."""
    payload_fake = {
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP"
    }

    # Simulamos que a biblioteca requests retornou sucesso (200) com os dados acima
    with patch("src.orcamento.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = payload_fake

        resultado = buscar_cep("01001-000")

    assert resultado["logradouro"] == "Praça da Sé"
    assert resultado["localidade"] == "São Paulo"
    assert resultado["uf"] == "SP"


def test_buscar_cep_invalido():
    """Valida se a função retorna um dicionário vazio caso o CEP seja inválido."""
    resultado = buscar_cep("123")  # Menos de 8 dígitos
    assert resultado == {}


# ==========================================
# 🧮 TESTES DE CÁLCULO DA CLASSE ORÇAMENTO
# ==========================================

def test_calcular_total_materiais():
    """Valida se a matemática de soma de materiais da sua classe está correta."""
    orc = Orcamento("Bruno Rodrigues", "Instalação Elétrica")
    orc.adicionar_material("Disjuntor 20A", 2, 15.0)
    orc.adicionar_material("Fita Isolante", 1, 10.0)
    
    # O total de materiais deve ser (2 * 15) + (1 * 10) = 40.0
    assert orc.calcular_total_materiais() == 40.0


def test_calcular_total_geral_orcamento():
    """Valida se o cálculo final (Mão de obra + Materiais) fecha o valor correto."""
    orc = Orcamento("Bruno Rodrigues", "Instalação Elétrica")
    orc.definir_mao_de_obra(250.0)
    orc.adicionar_material("Cabo 2.5mm", 1, 100.0)
    
    # O total geral deve ser 250.0 + 100.0 = 350.0
    assert orc.calcular_total() == 350.0