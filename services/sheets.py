import gspread
import time
from google.oauth2.service_account import Credentials

def conectar_sheet():

    for tentativa in range(5):

        try:

            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = Credentials.from_service_account_file(
                "database/credenciais.json",
                scopes=scope
            )

            client = gspread.authorize(creds)

            return client.open_by_url("https://docs.google.com/spreadsheets/d/1lmJ8ROJi_HqvdevW95rS0Uf49FmZPWg3hpFfeM2jMpo/edit?usp=drive_link")

        except Exception as e:

            print("Erro Google Sheets, tentando novamente...", tentativa+1)

            time.sleep(2)

    raise Exception("Google Sheets indisponível após várias tentativas")