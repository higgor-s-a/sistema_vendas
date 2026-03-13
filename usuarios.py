from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from database import (
    listar_usuarios,
    criar_usuario,
    alterar_status_usuario,
    excluir_usuario,
    editar_usuario
)

from services.log_service import registrar_log


usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


# =========================
# LISTAR / CRIAR USUÁRIO
# =========================

@usuarios_bp.route("/", methods=["GET", "POST"])
def usuarios():

    # =========================
    # BLOQUEIO DE ACESSO
    # =========================

    if session.get("usuario_nivel") != "admin":
        return redirect("/")

    # =========================
    # CRIAR USUÁRIO
    # =========================

    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        nivel = request.form.get("nivel")

        if usuario and senha and nivel:

            criar_usuario(usuario, senha, nivel)

            registrar_log(
                session.get("usuario_nome"),
                "criar_usuario",
                f"usuario criado: {usuario}"
            )

        return redirect("/usuarios?sucesso=1")

    lista = listar_usuarios()

    return render_template(
        "usuarios.html",
        usuarios=lista
    )


# =========================
# ATIVAR / DESATIVAR
# =========================

@usuarios_bp.route("/toggle", methods=["POST"])
def toggle_usuario():

    if session.get("usuario_nivel") != "admin":
        return jsonify({"status": "erro"})

    usuario = request.form.get("usuario")
    ativo = request.form.get("ativo") == "true"

    alterar_status_usuario(usuario, ativo)

    registrar_log(
        session.get("usuario_nome"),
        "alterar_status_usuario",
        f"usuario {usuario} ativo={ativo}"
    )

    return jsonify({
        "status": "ok",
        "ativo": ativo
    })


# =========================
# EXCLUIR USUÁRIO
# =========================

@usuarios_bp.route("/excluir", methods=["POST"])
def excluir():

    if session.get("usuario_nivel") != "admin":
        return jsonify({"status": "erro"})

    usuario = request.form.get("usuario")

    excluir_usuario(usuario)

    registrar_log(
        session.get("usuario_nome"),
        "excluir_usuario",
        f"usuario excluido: {usuario}"
    )

    return jsonify({
        "status": "ok"
    })


# =========================
# EDITAR USUÁRIO
# =========================

@usuarios_bp.route("/editar", methods=["POST"])
def editar():

    if session.get("usuario_nivel") != "admin":
        return jsonify({"status": "erro"})

    usuario_original = request.form.get("usuario_original")
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    editar_usuario(
        usuario_original,
        usuario,
        senha
    )

    registrar_log(
        session.get("usuario_nome"),
        "editar_usuario",
        f"usuario editado: {usuario_original} -> {usuario}"
    )

    return jsonify({
        "status": "ok"
    })


# =========================
# LISTA USUÁRIOS (AJAX)
# =========================

@usuarios_bp.route("/lista")
def lista():

    if session.get("usuario_nivel") != "admin":
        return jsonify([])

    lista = listar_usuarios()

    return jsonify(lista)


# =========================
# LOG DA PÁGINA USUÁRIOS
# =========================

@usuarios_bp.route("/log", methods=["POST"])
def log_pagina():

    usuario = session.get("usuario_nome")

    registrar_log(
        usuario,
        "acesso_pagina",
        "usuarios"
    )

    return jsonify({"status": "ok"})