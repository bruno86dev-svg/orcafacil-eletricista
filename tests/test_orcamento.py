from unittest.mock import patch
from src.orcamento import buscar_cep


def test_buscar_cep_sucesso():
    """Valida se a função retorna os dados de endereço corretamente com um CEP válido."""
    payload_fake = {
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP"
    }

    # Simulamos que a biblioteca requests retornou sucesso (200) com os dados acima
    with patch("requests.get") as mock_get:
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