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