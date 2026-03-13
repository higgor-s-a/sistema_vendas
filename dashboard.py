from flask import Blueprint, render_template, request, session
from database import listar_vendas, listar_pagamentos, listar_produtos
from services.log_service import registrar_log

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
def dashboard():

    usuario = session.get("usuario_nome", "desconhecido")

    data_filtro = request.args.get("data")

    # LOG DE ACESSO
    if data_filtro:
        registrar_log(
            usuario,
            "acessar_dashboard",
            f"filtro_data={data_filtro}"
        )
    else:
        registrar_log(
            usuario,
            "acessar_dashboard",
            "sem_filtro"
        )

    vendas = listar_vendas()
    pagamentos = listar_pagamentos()
    produtos = listar_produtos()

    # CONVERTER DATA DO INPUT (YYYY-MM-DD) PARA FORMATO DO BANCO (DD/MM/YYYY)

    if data_filtro:

        partes = data_filtro.split("-")
        data_filtro_convertida = f"{partes[2]}/{partes[1]}/{partes[0]}"

        vendas = [
            v for v in vendas
            if v.get("data", "").startswith(data_filtro_convertida)
        ]

        pagamentos = [
            p for p in pagamentos
            if p.get("data", "").startswith(data_filtro_convertida)
        ]


    # -------------------------
    # CALCULOS PRINCIPAIS
    # -------------------------

    faturamento = sum(float(v["total"]) for v in vendas) if vendas else 0

    recebido = sum(float(p["valor"]) for p in pagamentos) if pagamentos else 0

    recebido_pix = sum(
        float(p["valor"])
        for p in pagamentos
        if p.get("forma_pagamento", "").lower() == "pix"
    ) if pagamentos else 0

    recebido_dinheiro = sum(
        float(p["valor"])
        for p in pagamentos
        if p.get("forma_pagamento", "").lower() == "dinheiro"
    ) if pagamentos else 0

    saldo = faturamento - recebido

    total_vendas = len(vendas)

    ticket = faturamento / total_vendas if total_vendas > 0 else 0


    # ------------------------------
    # RANKING PRODUTOS VENDIDOS
    # ------------------------------

    ranking_produtos = {}

    for v in vendas:

        nome = v.get("produto")

        if nome not in ranking_produtos:
            ranking_produtos[nome] = 0

        ranking_produtos[nome] += int(v.get("quantidade", 1))


    ranking_produtos = dict(
        sorted(ranking_produtos.items(), key=lambda x: x[1], reverse=True)
    )

    ranking_nomes = list(ranking_produtos.keys())
    ranking_quantidades = list(ranking_produtos.values())


    # ------------------------------
    # LUCRO ESTIMADO
    # ------------------------------

    lucro_estimado = 0

    for p in produtos:

        preco = float(p.get("preco", 0))
        estoque = int(p.get("estoque", 0))

        lucro_estimado += preco * estoque


    return render_template(
        "dashboard.html",
        faturamento=faturamento,
        recebido=recebido,
        saldo=saldo,
        ticket=ticket,
        total_vendas=total_vendas,
        recebido_pix=recebido_pix,
        recebido_dinheiro=recebido_dinheiro,
        lucro_estimado=lucro_estimado,
        ranking_nomes=ranking_nomes,
        ranking_quantidades=ranking_quantidades,
        data_filtro=data_filtro
    )