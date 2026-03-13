from services.sheets import conectar_sheet
from datetime import datetime


def registrar_log(usuario, acao, detalhes=""):

    sheet = conectar_sheet()
    aba = sheet.worksheet("logs")

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    aba.append_row([
        data_hora,
        usuario,
        acao,
        detalhes
    ])