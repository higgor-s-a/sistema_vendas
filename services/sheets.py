import gspread
import time
import json
import os
from google.oauth2.service_account import Credentials


def conectar_sheet():

    for tentativa in range(5):

        try:

            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            # Tenta usar variável de ambiente primeiro (para Vercel)
            creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')

            if creds_json:
                # Carrega credenciais da variável de ambiente
                creds_dict = json.loads(creds_json)
                creds = Credentials.from_service_account_info(
                    creds_dict, scopes=scope)
            else:
                # Fallback para arquivo local (desenvolvimento)
                creds = Credentials.from_service_account_file(
                    "database/credenciais.json",
                    scopes=scope
                )

            client = gspread.authorize(creds)

            return client.open_by_url("https://docs.google.com/spreadsheets/d/1lmJ8ROJi_HqvdevW95rS0Uf49FmZPWg3hpFfeM2jMpo/edit?usp=drive_link")

        except Exception as e:

            print(
                f"Erro ao conectar ao Google Sheets (tentativa {tentativa+1}): {str(e)}")

            time.sleep(2)

    raise Exception("Google Sheets indisponível após várias tentativas")
