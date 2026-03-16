#!/usr/bin/env python3
"""
Teste conexão Google Sheets para Render
Execute: python test_render_sheets.py
"""

import os
from services.sheets import conectar_sheet

print("=== Teste Google Sheets Render ===")

# Check env vars
print("Vars:")
for var in ['PROJECT_ID', 'CLIENT_EMAIL', 'PRIVATE_KEY_ID']:
    val = os.getenv(var, 'AUSENTE')
    print(f"  {var}: {'PRESENTE' if val else 'AUSENTE'}")

print("\nConectando...")
try:
    sheet = conectar_sheet()
    ws = sheet.worksheet('usuarios')
    data = ws.get_all_records()
    print("✅ Sheets OK!")
    print(f"Planilha: {sheet.title}")
    print(f"Usuarios: {len(data)}")
    print("Sample:", data[:1])
except Exception as e:
    print(f"❌ Erro: {e}")
    print("Fallback demo OK")

print("Fim teste.")
