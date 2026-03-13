from flask import Blueprint, render_template, request, redirect, url_for, session
from services.log_service import registrar_log
from database import listar_clientes, adicionar_cliente, atualizar_cliente, excluir_cliente

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


# =========================
# CADASTRAR CLIENTE
# =========================
@clientes_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_cliente():

    cliente_cadastrado = False

    if request.method == "POST":

        nome = request.form.get("nome")
        telefone = request.form.get("telefone")

        usuario = session.get("usuario_nome", "desconhecido")

        if nome:

            adicionar_cliente(nome, telefone)

            # LOG
            registrar_log(
                usuario,
                "cadastrar_cliente",
                f"cliente={nome} telefone={telefone}"
            )

            cliente_cadastrado = True

    return render_template(
        "cadastrar_cliente.html",
        cliente_cadastrado=cliente_cadastrado
    )


# =========================
# TELA EDITAR (BUSCAR + EDITAR)
# =========================
@clientes_bp.route("/editar", methods=["GET"])
def tela_editar_cliente():

    clientes = listar_clientes()

    return render_template(
        "editar_cliente.html",
        clientes=clientes,
        cliente_atualizado=request.args.get("atualizado") == "true"
    )


# =========================
# SALVAR EDIÇÃO
# =========================
@clientes_bp.route("/editar", methods=["POST"])
def editar_cliente():

    nome_original = request.form.get("nome_original")
    novo_nome = request.form.get("novo_nome")
    novo_telefone = request.form.get("novo_telefone")

    usuario = session.get("usuario_nome", "desconhecido")

    if nome_original and novo_nome:

        atualizar_cliente(nome_original, novo_nome, novo_telefone)

        # LOG
        registrar_log(
            usuario,
            "editar_cliente",
            f"cliente_antigo={nome_original} cliente_novo={novo_nome} telefone={novo_telefone}"
        )

    return redirect(url_for("clientes.tela_editar_cliente", atualizado="true"))


# =========================
# EXCLUIR CLIENTE
# =========================
@clientes_bp.route("/excluir", methods=["POST"])
def excluir_cliente_rota():

    nome = request.form.get("nome")

    usuario = session.get("usuario_nome", "desconhecido")

    if nome:

        excluir_cliente(nome)

        # LOG
        registrar_log(
            usuario,
            "excluir_cliente",
            f"cliente={nome}"
        )

    return redirect(url_for("clientes.tela_editar_cliente", atualizado="true"))