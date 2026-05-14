import requests


def buscar_cep(cep: str) -> dict:
    """Consome a API ViaCEP para buscar o endereço do cliente."""
    cep_limpo = "".join(filter(str.isdigit, cep))

    if len(cep_limpo) != 8:
        print("❌ Erro: O CEP deve conter exatamente 8 dígitos.")
        return {}

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            if "erro" in dados:
                print("❌ Erro: CEP não encontrado na base do ViaCEP.")
                return {}
            return dados
        else:
            print(f"⚠️ API retornou status code: {resposta.status_code}")
            return {}
    except requests.RequestException:
        print("❌ Erro: Não foi possível conectar à API de CEP (Falha de rede).")
        return {}


class Orcamento:
    def __init__(self, cliente, servico):
        self.cliente = cliente
        self.servico = servico
        self.materiais = []
        self.valor_mao_de_obra = 0.0

    def adicionar_material(self, nome, quantidade, preco_unitario):
        self.materiais.append({
            "nome": nome,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario
        })

    def definir_mao_de_obra(self, valor):
        self.valor_mao_de_obra = valor

    def calcular_total_materiais(self):
        total = 0
        for m in self.materiais:
            total += m["quantidade"] * m["preco_unitario"]
        return total

    def calcular_total(self):
        return self.calcular_total_materiais() + self.valor_mao_de_obra


def main():
    print("=" * 50)
    print("      SISTEMA ORCAFÁCIL ELETRICISTA - NOVO ORÇAMENTO      ")
    print("=" * 50)

    cliente = input("Nome do Cliente: ").strip()
    
    print("\n--- Endereço do Cliente ---")
    cep = input("Digite o CEP do cliente: ").strip()

    # Chamada da API Pública
    dados_endereco = buscar_cep(cep)

    if dados_endereco:
        logradouro = dados_endereco.get("logradouro")
        bairro = dados_endereco.get("bairro")
        cidade = dados_endereco.get("localidade")
        uf = dados_endereco.get("uf")

        print("📍 Endereço Encontrado automaticamente:")
        print(f"   Rua: {logradouro} | Bairro: {bairro} | Cidade: {cidade}-{uf}\n")
    else:
        print("⚠️ Prossiga preenchendo o endereço manualmente...")
        logradouro = input("Rua: ").strip()

    # Instanciação da classe corrigida
    orcamento = Orcamento(cliente, "Serviço Padrão")
    
    # Exemplo de uso da sua lógica:
    orcamento.definir_mao_de_obra(150.0)
    orcamento.adicionar_material("Cabo Flexível 2.5mm", 2, 25.0)
    
    print("=" * 50)
    print(f"Orçamento gerado para {orcamento.cliente}!")
    print(f"Total Geral: R$ {orcamento.calcular_total():.2f}")
    print("=" * 50)


if __name__ == "__main__":
    main()