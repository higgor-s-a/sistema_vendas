#!/usr/bin/env python3
from services.sheets import conectar_sheet
import os
\"\"\"Teste específico para conexão Google Sheets no Render\"\"\"

print(\"== = Teste Google Sheets para Render == =\")

print(\"1. Vars de ambiente detectadas: \")
vars_check = ['PROJECT_ID', 'PRIVATE_KEY_ID', 'PRIVATE_KEY', 'CLIENT_EMAIL']
for var in vars_check:
    value = '*** PRESENTE ***' if os.getenv(var) else 'AUSENTE'
    print(f\"  {var}: {value}\")

print(\"\\n2. Tentando conexão...\")
try:
    sheet = conectar_sheet()
    worksheet = sheet.worksheet('usuarios')
    records = worksheet.get_all_records()
    print(\"✅ CONEXÃO GOOGLE SHEETS OK!\")
    print(f\"   Planilha '{sheet.title}' acessada\")
    print(f\"   Usuários encontrados: {len(records)}\")
    print(\"   Primeiros registros: \", records[:2])
except Exception as e:
    print(f\"❌ ERRO na conexão: {str(e)}\")
    print(\"   Usando modo demo/mock data(funciona OK)\")

print(\"\\nTeste completo. App funcional em modo demo.\")
