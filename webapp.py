from flask import Flask, session, redirect, request, render_template
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
app.secret_key = "chave_super_secreta"


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

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = autenticar(usuario, senha)

        if user:

            session["usuario_id"] = user["id"]
            session["usuario_nome"] = user["usuario"]
            session["usuario_nivel"] = user["nivel"]

            # REGISTRA LOG
            registrar_log(
                user["usuario"],
                "login",
                "acesso ao sistema"
            )

            return redirect("/")

        else:
            erro = "Usuário ou senha inválidos"

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