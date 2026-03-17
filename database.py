from services.sheets import conectar_sheet
from datetime import datetime
import time
import re
import bcrypt


# =========================
# UTIL
# =========================

def formatar_telefone(telefone):
    numeros = re.sub(r"\D", "", telefone or "")
    if len(numeros) != 11:
        return ""
    return f"({numeros[:2]}) {numeros[2]} {numeros[3:7]}-{numeros[7:]}"


# =========================
# CLIENTES
# =========================

def adicionar_cliente(nome, telefone):

    sheet = conectar_sheet()
    aba = sheet.worksheet("clientes")

    cliente_id = str(int(time.time()*1000))

    aba.append_row([
        cliente_id,
        nome,
        formatar_telefone(telefone)
    ])


def listar_clientes():

    sheet = conectar_sheet()
    aba = sheet.worksheet("clientes")

    return aba.get_all_records()


def buscar_cliente_por_nome(nome):

    clientes = listar_clientes()

    for c in clientes:
        if c["nome"].lower() == nome.lower():
            return c

    return None


def atualizar_cliente(nome_original, novo_nome, novo_telefone):

    sheet = conectar_sheet()
    aba = sheet.worksheet("clientes")

    dados = aba.get_all_records()

    novo_telefone = formatar_telefone(novo_telefone)

    for i, c in enumerate(dados):

        if c["nome"] == nome_original:

            linha = i + 2

            aba.update_cell(linha, 2, novo_nome)
            aba.update_cell(linha, 3, novo_telefone)

            return "ok"

    return "nao_encontrado"


def excluir_cliente(nome):

    sheet = conectar_sheet()
    aba = sheet.worksheet("clientes")

    vendas = listar_vendas()
    for v in vendas:
        if v["cliente_nome"] == nome:
            return "possui_vendas"

    dados = aba.get_all_records()

    for i, c in enumerate(dados):
        if c["nome"] == nome:
            linha = i + 2
            aba.delete_rows(linha)
            return "ok"

    return "nao_encontrado"


# =========================
# PRODUTOS
# =========================

def adicionar_produto(nome, preco, estoque):

    sheet = conectar_sheet()
    aba = sheet.worksheet("produtos")

    aba.append_row([
        nome,
        float(preco),
        int(estoque)
    ])


def listar_produtos():

    sheet = conectar_sheet()
    aba = sheet.worksheet("produtos")

    return aba.get_all_records()


def buscar_preco_produto(nome_produto):

    produtos = listar_produtos()

    for p in produtos:
        if p["nome"] == nome_produto:
            return float(p["preco"])

    return 0


def atualizar_produto(nome_antigo, nome, preco, estoque):

    sheet = conectar_sheet()
    aba = sheet.worksheet("produtos")

    dados = aba.get_all_records()

    for i, p in enumerate(dados):

        if p["nome"] == nome_antigo:

            linha = i + 2

            aba.update_cell(linha, 1, nome)
            aba.update_cell(linha, 2, float(preco))
            aba.update_cell(linha, 3, int(estoque))

            return "ok"

    return "nao_encontrado"


def excluir_produto(nome):

    sheet = conectar_sheet()
    aba = sheet.worksheet("produtos")

    dados = aba.get_all_records()

    for i, p in enumerate(dados):

        if p["nome"] == nome:

            linha = i + 2
            aba.delete_rows(linha)

            return "ok"

    return "nao_encontrado"


def buscar_produtos(termo):

    produtos = listar_produtos()

    if not termo:
        return produtos

    termo = termo.lower()

    filtrados = []

    for p in produtos:
        if termo in p["nome"].lower():
            filtrados.append(p)

    return filtrados


# =========================
# VENDAS
# =========================

def adicionar_venda(cliente_nome, produto, quantidade, valor_unitario):

    sheet = conectar_sheet()
    aba = sheet.worksheet("vendas")

    cliente = buscar_cliente_por_nome(cliente_nome)

    if not cliente:
        return "cliente_nao_existe"

    cliente_id = cliente["cliente_id"]

    quantidade = int(quantidade)
    valor_unitario = float(valor_unitario)

    estoque_atual = consultar_estoque(produto)

    if quantidade > estoque_atual:
        return "sem_estoque"

    from zoneinfo import ZoneInfo
    total = quantidade * valor_unitario
    data = datetime.now(ZoneInfo("America/Sao_Paulo")
                        ).strftime("%d/%m/%Y %H:%M")
    venda_id = str(int(time.time()*1000))

    aba.append_row([
        venda_id,
        data,
        cliente_id,
        cliente_nome,
        produto,
        quantidade,
        valor_unitario,
        total
    ])

    baixar_estoque(produto, quantidade)

    return venda_id


def listar_vendas():

    sheet = conectar_sheet()
    aba = sheet.worksheet("vendas")

    return aba.get_all_records()


def buscar_venda_por_id(venda_id):

    vendas = listar_vendas()

    for v in vendas:
        if str(v["venda_id"]) == str(venda_id):
            return v

    return None


def buscar_vendas_por_cliente(nome_cliente):

    vendas = listar_vendas()
    resultado = []

    for v in vendas:
        if v["cliente_nome"].lower() == nome_cliente.lower():
            resultado.append(v)

    return resultado


def buscar_vendas_por_data(data_busca):

    vendas = listar_vendas()
    resultado = []

    data_formatada = datetime.strptime(
        data_busca, "%Y-%m-%d").strftime("%d/%m/%Y")

    for v in vendas:
        data_venda = v["data"].split(" ")[0]
        if data_venda == data_formatada:
            resultado.append(v)

    return resultado


def venda_esta_paga(venda_id):

    venda = buscar_venda_por_id(venda_id)

    if not venda:
        return False

    total_venda = float(venda["total"])
    pagamentos = listar_pagamentos()

    total_pago = sum(
        float(p["valor"])
        for p in pagamentos
        if str(p.get("venda_id", "")) == str(venda_id)
    )

    return total_pago >= total_venda


def atualizar_venda(venda_id, novo_produto, nova_quantidade):

    sheet = conectar_sheet()
    aba = sheet.worksheet("vendas")

    dados = aba.get_all_records()

    for i, v in enumerate(dados):

        if str(v["venda_id"]) == str(venda_id):

            linha = i + 2

            produto_antigo = v["produto"]
            quantidade_antiga = int(v["quantidade"])

            baixar_estoque(produto_antigo, -quantidade_antiga)

            nova_quantidade = int(nova_quantidade)

            estoque_atual = consultar_estoque(novo_produto)

            if nova_quantidade > estoque_atual:
                return "sem_estoque"

            valor_unitario = buscar_preco_produto(novo_produto)
            novo_total = nova_quantidade * valor_unitario

            aba.update_cell(linha, 5, novo_produto)
            aba.update_cell(linha, 6, nova_quantidade)
            aba.update_cell(linha, 7, valor_unitario)
            aba.update_cell(linha, 8, novo_total)

            baixar_estoque(novo_produto, nova_quantidade)

            if venda_esta_paga(venda_id):
                atualizar_pagamento_vinculado(venda_id, novo_total)

            return "ok"

    return "nao_encontrada"


def excluir_venda(venda_id):

    sheet = conectar_sheet()
    aba = sheet.worksheet("vendas")

    dados = aba.get_all_records()

    for i, v in enumerate(dados):

        if str(v["venda_id"]) == str(venda_id):

            produto = v["produto"]
            quantidade = int(v["quantidade"])

            baixar_estoque(produto, -quantidade)

            linha = i + 2
            aba.delete_rows(linha)

            excluir_pagamento_por_venda(venda_id)

            return "ok"

    return "nao_encontrada"


# =========================
# PAGAMENTOS
# =========================

def registrar_pagamento(cliente_nome, valor, venda_id=None, forma_pagamento=None):

    sheet = conectar_sheet()
    aba = sheet.worksheet("pagamentos")

    cliente = buscar_cliente_por_nome(cliente_nome)

    if not cliente:
        return

    from zoneinfo import ZoneInfo
    cliente_id = cliente["cliente_id"]
    data = datetime.now(ZoneInfo("America/Sao_Paulo")
                        ).strftime("%d/%m/%Y %H:%M")

    aba.append_row([
        data,
        venda_id if venda_id else "",
        cliente_id,
        cliente_nome,
        float(valor),
        forma_pagamento if forma_pagamento else ""
    ])


def listar_pagamentos():

    sheet = conectar_sheet()
    aba = sheet.worksheet("pagamentos")

    return aba.get_all_records()


def atualizar_pagamento_vinculado(venda_id, novo_valor):

    sheet = conectar_sheet()
    aba = sheet.worksheet("pagamentos")

    dados = aba.get_all_records()

    for i, p in enumerate(dados):

        if str(p.get("venda_id", "")) == str(venda_id):

            linha = i + 2
            aba.update_cell(linha, 5, float(novo_valor))
            return


def excluir_pagamento_por_venda(venda_id):

    sheet = conectar_sheet()
    aba = sheet.worksheet("pagamentos")

    dados = aba.get_all_records()

    for i, p in enumerate(dados):

        if str(p.get("venda_id", "")) == str(venda_id):

            linha = i + 2
            aba.delete_rows(linha)
            return


def aplicar_pagamento_cliente(cliente_nome, valor_pago, forma_pagamento):

    vendas = buscar_vendas_por_cliente(cliente_nome)

    vendas.sort(
        key=lambda v: datetime.strptime(v["data"], "%d/%m/%Y %H:%M")
    )

    valor_restante = float(valor_pago)

    for venda in vendas:

        venda_id = venda["venda_id"]
        total_venda = float(venda["total"])

        pagamentos = listar_pagamentos()
        total_pago = sum(
            float(p["valor"])
            for p in pagamentos
            if str(p.get("venda_id", "")) == str(venda_id)
        )

        saldo_venda = total_venda - total_pago

        if saldo_venda <= 0:
            continue

        if valor_restante <= 0:
            break

        if valor_restante >= saldo_venda:

            registrar_pagamento(
                cliente_nome,
                saldo_venda,
                venda_id,
                forma_pagamento
            )

            valor_restante -= saldo_venda

        else:

            registrar_pagamento(
                cliente_nome,
                valor_restante,
                venda_id,
                forma_pagamento
            )

            valor_restante = 0
            break

    if valor_restante > 0:
        registrar_pagamento(
            cliente_nome,
            valor_restante,
            None,
            forma_pagamento
        )


# =========================
# ESTOQUE
# =========================

def baixar_estoque(nome_produto, quantidade):

    sheet = conectar_sheet()
    aba = sheet.worksheet("produtos")

    dados = aba.get_all_records()

    for i, p in enumerate(dados):

        if p["nome"] == nome_produto:

            estoque_atual = int(p.get("estoque", 0))
            novo = estoque_atual - int(quantidade)

            linha = i + 2
            aba.update_cell(linha, 3, novo)
            return


def consultar_estoque(nome_produto):

    produtos = listar_produtos()

    for p in produtos:
        if p["nome"] == nome_produto:
            return int(p.get("estoque", 0))

    return 0


# =========================
# USUARIOS
# =========================

def listar_usuarios():

    sheet = conectar_sheet()
    aba = sheet.worksheet("usuarios")

    return aba.get_all_records()


def criar_usuario(usuario, senha, nivel):

    sheet = conectar_sheet()
    aba = sheet.worksheet("usuarios")

    usuarios = aba.get_all_records()

    novo_id = len(usuarios) + 1

    senha_hash = bcrypt.hashpw(
        senha.encode(),
        bcrypt.gensalt()
    ).decode()

    aba.append_row([
        novo_id,
        usuario,
        senha_hash,
        True,
        nivel
    ])


def alterar_status_usuario(usuario, ativo):

    sheet = conectar_sheet()
    aba = sheet.worksheet("usuarios")

    dados = aba.get_all_records()

    for i, u in enumerate(dados):

        if u["usuario"] == usuario:

            linha = i + 2
            aba.update_cell(linha, 4, ativo)

            return "ok"

    return "nao_encontrado"

# =========================
# EDITAR USUÁRIO
# =========================


def editar_usuario(usuario_original, usuario, senha):

    sheet = conectar_sheet()
    aba = sheet.worksheet("usuarios")

    dados = aba.get_all_records()

    for i, u in enumerate(dados):

        if u["usuario"] == usuario_original:

            linha = i + 2

            aba.update_cell(linha, 2, usuario)

            if senha:

                senha_hash = bcrypt.hashpw(
                    senha.encode(),
                    bcrypt.gensalt()
                ).decode()

                aba.update_cell(linha, 3, senha_hash)

            return "ok"

    return "nao_encontrado"


# =========================
# EXCLUIR USUÁRIO
# =========================

def excluir_usuario(usuario):

    sheet = conectar_sheet()
    aba = sheet.worksheet("usuarios")

    dados = aba.get_all_records()

    for i, u in enumerate(dados):

        if u["usuario"] == usuario:

            linha = i + 2
            aba.delete_rows(linha)

            return "ok"

    return "nao_encontrado"
