from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
from services.log_service import registrar_log

from database import (
    listar_clientes,
    listar_produtos,
    buscar_preco_produto,
    adicionar_venda,
    registrar_pagamento,
    buscar_vendas_por_cliente,
    venda_esta_paga,
    atualizar_venda,
    excluir_venda,
    buscar_venda_por_id,
    buscar_vendas_por_data,
    excluir_pagamento_por_venda
)

vendas_bp = Blueprint("vendas", __name__, url_prefix="/vendas")


# =========================
# PÁGINA NOVA VENDA
# =========================

@vendas_bp.route("/", methods=["GET", "POST"])
def nova_venda():

    if request.method == "POST":

        cliente = request.form["cliente"]
        produto = request.form["produto"]
        quantidade = request.form["quantidade"]
        pago = request.form.get("pago")
        forma_pagamento = request.form.get("forma_pagamento")

        usuario = session.get("usuario_nome", "desconhecido")

        # BUSCA PREÇO
        valor_unitario = buscar_preco_produto(produto)

        venda_id = adicionar_venda(cliente, produto, quantidade, valor_unitario)

        # LOG VENDA
        registrar_log(
            usuario,
            "nova_venda",
            f"venda_id={venda_id} cliente={cliente} produto={produto} qtd={quantidade}"
        )

        if pago == "sim" and forma_pagamento:

            venda = buscar_venda_por_id(venda_id)

            if venda:

                registrar_pagamento(
                    venda["cliente_nome"],
                    venda["total"],
                    venda_id,
                    forma_pagamento
                )

                # LOG PAGAMENTO
                registrar_log(
                    usuario,
                    "pagamento",
                    f"venda_id={venda_id} valor={venda['total']} forma={forma_pagamento}"
                )

        return redirect(url_for("vendas.nova_venda", venda_registrada="true"))

    clientes = listar_clientes()
    produtos = listar_produtos()
    venda_registrada = request.args.get("venda_registrada") == "true"

    return render_template(
        "vendas.html",
        clientes=clientes,
        produtos=produtos,
        venda_registrada=venda_registrada
    )


# =========================
# ROTA BUSCAR PREÇO
# =========================

@vendas_bp.route("/preco/<produto>")
def obter_preco(produto):
    preco = buscar_preco_produto(produto)
    return jsonify({"preco": preco})


# =========================
# PÁGINA EDITAR
# =========================

@vendas_bp.route("/editar")
def editar_vendas():
    produtos = listar_produtos()
    return render_template("editar_venda.html", produtos=produtos)


# =========================
# BUSCAR POR DATA
# =========================

@vendas_bp.route("/por_data/<data>")
def por_data(data):

    vendas = buscar_vendas_por_data(data)

    vendas.sort(
        key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y %H:%M"),
        reverse=True
    )

    resultado = []

    for v in vendas:

        resultado.append({
            "id": v["venda_id"],
            "data_hora": v["data"],
            "produto": v["produto"],
            "quantidade": v["quantidade"],
            "cliente": v["cliente_nome"],
            "paga": venda_esta_paga(v["venda_id"]),
            "forma_pagamento": buscar_forma_pagamento(v["venda_id"])
        })

    return jsonify(resultado)


def buscar_forma_pagamento(venda_id):

    from database import listar_pagamentos

    pagamentos = listar_pagamentos()

    for p in pagamentos:
        if str(p.get("venda_id", "")) == str(venda_id):
            return p.get("forma_pagamento", "")

    return ""


# =========================
# SALVAR EDIÇÃO
# =========================

@vendas_bp.route("/salvar_edicao", methods=["POST"])
def salvar_edicao():

    usuario = session.get("usuario_nome", "desconhecido")

    venda_id = request.form["venda_id"]
    novo_produto = request.form["produto"]
    nova_quantidade = request.form["quantidade"]
    pagar_agora = request.form.get("pagar_agora") == "true"
    forma_pagamento = request.form.get("forma_pagamento")

    resultado = atualizar_venda(venda_id, novo_produto, nova_quantidade)

    if resultado != "ok":
        return jsonify({"status": resultado})

    venda = buscar_venda_por_id(venda_id)

    if not venda:
        return jsonify({"status": "erro_venda"})

    from database import listar_pagamentos

    # LOG EDIÇÃO
    registrar_log(
        usuario,
        "editar_venda",
        f"venda_id={venda_id} produto={novo_produto} qtd={nova_quantidade}"
    )

    # ===============================
    # MARCOU COMO PAGA
    # ===============================
    if pagar_agora:

        if not forma_pagamento:
            return jsonify({"status": "forma_pagamento_obrigatoria"})

        excluir_pagamento_por_venda(venda_id)

        registrar_pagamento(
            venda["cliente_nome"],
            venda["total"],
            venda_id,
            forma_pagamento
        )

        registrar_log(
            usuario,
            "pagamento",
            f"venda_id={venda_id} valor={venda['total']} forma={forma_pagamento}"
        )

    # ===============================
    # DESMARCOU PAGAMENTO
    # ===============================
    else:

        excluir_pagamento_por_venda(venda_id)

        registrar_log(
            usuario,
            "remover_pagamento",
            f"venda_id={venda_id}"
        )

    return jsonify({"status": "ok"})


# =========================
# EXCLUIR VENDA
# =========================

@vendas_bp.route("/excluir/<venda_id>", methods=["POST"])
def excluir(venda_id):

    usuario = session.get("usuario_nome", "desconhecido")

    resultado = excluir_venda(venda_id)

    if resultado == "ok":

        registrar_log(
            usuario,
            "excluir_venda",
            f"venda_id={venda_id}"
        )

    return jsonify({"status": resultado})