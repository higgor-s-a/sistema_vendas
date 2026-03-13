from flask import Blueprint, render_template, request, redirect, flash, session
from database import (
    adicionar_produto,
    listar_produtos,
    atualizar_produto,
    excluir_produto,
    buscar_produtos
)
from services.log_service import registrar_log

produtos_bp = Blueprint("produtos", __name__)


# =========================
# FUNÇÃO PARA LIMPAR PREÇO
# =========================
def limpar_preco(valor):
    if not valor:
        return 0.0

    valor = valor.replace("R$", "")
    valor = valor.replace(" ", "")
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")

    return float(valor)


# =========================
# LISTAR + CADASTRAR
# =========================
@produtos_bp.route("/produtos", methods=["GET", "POST"])
def produtos():

    if request.method == "POST":

        nome = request.form.get("nome")
        preco = request.form.get("preco")
        estoque = request.form.get("estoque")

        if nome:

            preco = limpar_preco(preco)
            estoque = int(estoque)

            adicionar_produto(nome, preco, estoque)

            registrar_log(
                session.get("usuario_nome"),
                "cadastrar_produto",
                nome
            )

            flash("Produto cadastrado com sucesso!")

        return redirect("/produtos")

    termo = request.args.get("busca")

    if termo:
        lista = buscar_produtos(termo)
    else:
        lista = listar_produtos()

    return render_template("produtos.html", produtos=lista)


# =========================
# EXCLUIR
# =========================
@produtos_bp.route("/excluir_produto/<nome>")
def excluir(nome):

    excluir_produto(nome)

    registrar_log(
        session.get("usuario_nome"),
        "excluir_produto",
        nome
    )

    flash("Produto excluído com sucesso!")

    return redirect("/produtos")


# =========================
# EDITAR
# =========================
@produtos_bp.route("/editar_produto/<nome>", methods=["GET", "POST"])
def editar_produto(nome):

    produtos = listar_produtos()
    produto = None

    for p in produtos:
        if p["nome"] == nome:
            produto = p
            break

    if not produto:
        return "Produto não encontrado"

    if request.method == "POST":

        novo_nome = request.form.get("nome")
        preco = request.form.get("preco")
        estoque = request.form.get("estoque")

        preco = limpar_preco(preco)
        estoque = int(estoque)

        atualizar_produto(nome, novo_nome, preco, estoque)

        registrar_log(
            session.get("usuario_nome"),
            "editar_produto",
            novo_nome
        )

        flash("Produto editado com sucesso!")

        return redirect("/produtos")

    return render_template(
        "editar_produto.html",
        produto=produto
    )


# =========================
# ROTA DE LOG - PRODUTOS
# =========================
@produtos_bp.route("/produtos/log", methods=["POST"])
def log_produtos():

    acao = request.form.get("acao")
    produto = request.form.get("produto")

    registrar_log(
        session.get("usuario_nome"),
        acao,
        produto
    )

    return {"status": "ok"}