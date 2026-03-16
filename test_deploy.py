#!/usr/bin/env python3
"""
Script de teste para verificar se a aplicação está pronta para deploy no Vercel
"""

import sys
import os
import json


def test_imports():
    """Testa se todos os imports necessários funcionam"""
    try:
        from webapp import app
        from services.sheets import conectar_sheet
        from services.auth_service import autenticar
        print("✓ Todos os imports funcionaram")
        return True
    except ImportError as e:
        print(f"✗ Erro de import: {e}")
        return False


def test_credentials():
    """Testa se as credenciais estão configuradas"""
    creds_env = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    creds_file = os.path.exists('database/credenciais.json')

    if creds_env:
        try:
            creds_dict = json.loads(creds_env)
            print("✓ Credenciais encontradas na variável de ambiente")
            return True
        except json.JSONDecodeError:
            print("✗ Credenciais na variável de ambiente estão malformadas")
            return False
    elif creds_file:
        print("✓ Arquivo de credenciais encontrado (modo desenvolvimento)")
        return True
    else:
        print("✗ Nenhuma credencial encontrada")
        return False


def test_flask_app():
    """Testa se a aplicação Flask pode ser criada"""
    try:
        from webapp import app
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code in [200, 302]:  # 302 é redirect para login
                print("✓ Aplicação Flask funcionando")
                return True
            else:
                print(
                    f"✗ Erro na aplicação Flask: status {response.status_code}")
                return False
    except Exception as e:
        print(f"✗ Erro ao testar aplicação Flask: {e}")
        return False


def main():
    print("=== Teste de Preparação para Deploy no Vercel ===\n")

    tests = [
        ("Imports", test_imports),
        ("Credenciais", test_credentials),
        ("Aplicação Flask", test_flask_app),
    ]

    passed = 0
    total = len(tests)

    for name, test_func in tests:
        print(f"Testando {name}...")
        if test_func():
            passed += 1
        print()

    print(f"Resultado: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 Tudo pronto para o deploy no Vercel!")
        print("\nPróximos passos:")
        print("1. Faça commit e push do código para um repositório Git")
        print("2. Conecte o repositório ao Vercel")
        print("3. Configure a variável GOOGLE_SHEETS_CREDENTIALS no Vercel")
        print("4. Faça o deploy")
    else:
        print("❌ Alguns testes falharam. Corrija os problemas antes do deploy.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
