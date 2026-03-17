from flask import Blueprint, render_template, request, redirect, url_for, session
from database import listar_vendas, listar_clientes, registrar_pagamento, listar_pagamentos, aplicar_pagamento_cliente
from services.log_service import registrar_log
from datetime import datetime

extrato_bp = Blueprint("extrato", __name__)


def limpar_dict(lista):
    nova = []
    for d in lista:
        novo = {k.strip().lower(): v for k, v in d.items()}
        nova.append(novo)
    return nova


def formatar_data_local(data):
    """Formata data string para horário local BR sem timezone shift."""
    for fmt in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"):
        try:
            dt = datetime.strptime(data, fmt)
            return dt.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            pass
    return data  # Fallback para data inválida


@extrato_bp.route("/extrato", methods=["GET", "POST"])
def extrato():

    clientes = listar_clientes()
    extrato_lista = []
    saldo = 0
    cliente_sel = None
    pagamento_registrado = False

    usuario = session.get("usuario_nome", "desconhecido")

    # =========================
    # REGISTRAR PAGAMENTO
    # =========================
    if request.method == "POST":

        cliente_sel = request.form.get("cliente")
        valor_pag = request.form.get("valor_pagamento")
        forma_pagamento = request.form.get("forma_pagamento")

        if valor_pag and cliente_sel and forma_pagamento:

            valor_float = float(
                valor_pag
                .replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )

            aplicar_pagamento_cliente(
                cliente_sel, valor_float, forma_pagamento)

            # LOG
            registrar_log(
                usuario,
                "registrar_pagamento_extrato",
                f"cliente={cliente_sel} valor={valor_float} forma={forma_pagamento}"
            )

            return redirect(
                url_for(
                    "extrato.extrato",
                    cliente=cliente_sel,
                    pagamento="true"
                )
            )

    cliente_sel = request.args.get("cliente") or None
    pagamento_registrado = request.args.get("pagamento") == "true"

    if cliente_sel:

        # LOG DE CONSULTA
        registrar_log(
            usuario,
            "consultar_extrato",
            f"cliente={cliente_sel}"
        )

        # =========================
        # VENDAS
        # =========================
        vendas = limpar_dict(listar_vendas())

        for v in vendas:
            if v.get("cliente_nome") == cliente_sel:
                data = formatar_data_local(v.get("data", ""))
                extrato_lista.append({
                    "data": data,
                    "tipo": "Venda",
                    "valor": float(v.get("total", 0)),
                    "produto": v.get("produto", ""),
                    "quantidade": int(v.get("quantidade", 0)),
                    "forma_pagamento": ""
                })

        # =========================
        # PAGAMENTOS
        # =========================
        pagamentos = limpar_dict(listar_pagamentos())

        for p in pagamentos:
            if p.get("cliente_nome") == cliente_sel:
                data = formatar_data_local(p.get("data", ""))
                extrato_lista.append({
                    "data": data,
                    "tipo": "Pagamento",
                    "valor": -float(p.get("valor", 0)),
                    "produto": "",
                    "quantidade": "",
                    "forma_pagamento": p.get("forma_pagamento", "")
                })

        # =========================
        # ORDENAR POR DATA
        # =========================
        extrato_lista.sort(
            key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y %H:%M")
        )

        saldo = sum(item["valor"] for item in extrato_lista)

    return render_template(
        "extrato.html",
        clientes=clientes,
        extrato=extrato_lista,
        saldo=saldo,
        cliente=cliente_sel,
        pagamento_registrado=pagamento_registrado
    )
