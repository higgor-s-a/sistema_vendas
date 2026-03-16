import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file(
    "database/credenciais.json",
    scopes=scope
)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1lmJ8ROJi_HqvdevW95rS0Uf49FmZPWg3hpFfeM2jMpo/edit?usp=drive_link")
print(sheet.worksheets())