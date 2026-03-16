from services.sheets import conectar_sheet
import sys
sys.path.append('.')


try:
    client = conectar_sheet()
    print("Conexão bem-sucedida!")
    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1lmJ8ROJi_HqvdevW95rS0Uf49FmZPWg3hpFfeM2jMpo/edit?usp=drive_link")
    print(f"Planilha aberta: {sheet.title}")
except Exception as e:
    print(f"Erro: {str(e)}")
