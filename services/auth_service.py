import bcrypt
from services.sheets import conectar_sheet


def autenticar(usuario, senha):

    sheet = conectar_sheet()
    aba = sheet.worksheet("usuarios")

    dados = aba.get_all_records()

    for u in dados:

        if u["usuario"] == usuario and str(u["ativo"]).upper() == "TRUE":

            senha_hash = u["senha_hash"]

            if bcrypt.checkpw(
                senha.encode(),
                senha_hash.encode()
            ):
                return u

    return None