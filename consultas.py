from database import DB

class Consultas:

    def __init__(self):

        db = DB()

        self.vendas = db.aba("VENDAS")
        self.pagamentos = db.aba("PAGAMENTOS")
        self.produtos = db.aba("PRODUTOS")
        self.itens = db.aba("ITENS")

    def saldo_cliente(self, cliente_id):

        vendas = self.vendas.get_all_records()
        pagamentos = self.pagamentos.get_all_records()

        total_vendas = sum(
            float(v["total"]) for v in vendas
            if v["cliente_id"] == cliente_id
        )

        total_pag = sum(
            float(p["valor"]) for p in pagamentos
            if p["cliente_id"] == cliente_id
        )

        return total_vendas - total_pag

    def estoque(self):

        return self.produtos.get_all_records()

    def extrato_cliente(self, cliente_id):

        itens = self.itens.get_all_records()

        return [
            i for i in itens
            if i["produto_id"] and i["venda_id"]
        ]
