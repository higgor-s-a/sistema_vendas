from flask import Flask, session, redirect, request, render_template
import os
from services.auth_service import autenticar
from services.log_service import registrar_log

# IMPORTS DOS BLUEPRINTS
from clientes import clientes_bp
from produtos import produtos_bp
from vendas import vendas_bp
from extrato import extrato_bp
from pagamentos import pagamento_bp
from dashboard import dashboard_bp
from usuarios import usuarios_bp

# =========================
# CRIA APP
# =========================

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave_super_secreta')

# Configurações para ambiente serverless (Vercel)
# Remove configurações de sessão que podem causar problemas
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
# Não define SESSION_TYPE para usar o padrão (cookies)


# =========================
# REGISTRA BLUEPRINTS
# =========================

app.register_blueprint(clientes_bp)
app.register_blueprint(produtos_bp)
app.register_blueprint(vendas_bp)
app.register_blueprint(extrato_bp)
app.register_blueprint(pagamento_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(usuarios_bp)

# =========================
# ERROR HANDLERS
# =========================

@app.errorhandler(500)
def internal_error(error):
    print(f"Erro 500: {str(error)}")
    import traceback
    print(traceback.format_exc())
    return "Erro interno do servidor", 500

@app.errorhandler(Exception)
def handle_exception(error):
    print(f"Erro geral: {str(error)}")
    import traceback
    print(traceback.format_exc())
    return "Erro interno do servidor", 500

# =========================
# PROTEÇÃO GLOBAL DE LOGIN
# =========================


@app.before_request
def proteger_rotas():

    rotas_livres = [
        "/login",
        "/static"
    ]

    caminho = request.path

    # permite rotas livres
    if any(caminho.startswith(r) for r in rotas_livres):
        return

    # bloqueia acesso sem login
    if "usuario_id" not in session:
        return redirect("/login")

    # =====================
    # BLOQUEIO DE USUÁRIOS
    # =====================

    if caminho.startswith("/usuarios"):

        if session.get("usuario_nivel") != "admin":
            return redirect("/")


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    erro = None

    if request.method == "POST":

        try:
            usuario = request.form["usuario"]
            senha = request.form["senha"]

            user = autenticar(usuario, senha)

            if user:
                session["usuario_id"] = user["id"]
                session["usuario_nome"] = user["usuario"]
                session["usuario_nivel"] = user["nivel"]

                # REGISTRA LOG
                try:
                    registrar_log(
                        user["usuario"],
                        "login",
                        "acesso ao sistema"
                    )
                except Exception as log_error:
                    print(f"Erro ao registrar log: {log_error}")
                    # Não falha o login por causa do log

                return redirect("/")

            else:
                erro = "Usuário ou senha inválidos"

        except Exception as e:
            print(f"Erro durante login: {str(e)}")
            import traceback
            print(traceback.format_exc())
            erro = "Erro interno do servidor. Tente novamente."

    return render_template("login.html", erro=erro)


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    usuario = session.get("usuario_nome")

    if usuario:
        registrar_log(
            usuario,
            "logout",
            "saída do sistema"
        )

    session.clear()

    return redirect("/login")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)
