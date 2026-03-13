from flask import Blueprint, render_template, request, redirect
from database import registrar_pagamento, listar_clientes

pagamento_bp = Blueprint("pagamento", __name__, url_prefix="/pagamento")


@pagamento_bp.route("/", methods=["GET", "POST"])
def pagamento():

    clientes = listar_clientes()

    if request.method == "POST":

        cliente = request.form["cliente"]
        valor = request.form["valor"]
        forma_pagamento = request.form.get("forma_pagamento")

        # 🔥 valida forma obrigatória
        if not forma_pagamento:
            return render_template(
                "pagamento.html",
                clientes=clientes,
                erro="Selecione a forma de pagamento."
            )

        registrar_pagamento(cliente, valor, None, forma_pagamento)

        return redirect("/pagamento")

    return render_template("pagamento.html", clientes=clientes)