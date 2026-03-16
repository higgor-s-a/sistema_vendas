import gspread
import time
import json
import os
from google.oauth2.service_account import Credentials

# Dados mockados para demonstração
DADOS_MOCK = {
    "usuarios": [
        {"id": 1, "usuario": "admin", "senha_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LezfxYzHvLz5py2W",
            "nivel": "admin", "ativo": "TRUE"},  # senha: demo123
        {"id": 2, "usuario": "vendedor", "senha_hash": "$2b$12$dummy.hash.for.demo",
            "nivel": "user", "ativo": "TRUE"}
    ],
    "clientes": [
        {"id": 1, "nome": "João Silva", "email": "joao@email.com",
            "telefone": "(11) 99999-9999", "ativo": "TRUE"},
        {"id": 2, "nome": "Maria Santos", "email": "maria@email.com",
            "telefone": "(11) 88888-8888", "ativo": "TRUE"}
    ],
    "produtos": [
        {"id": 1, "nome": "Produto A", "preco": 100.00,
            "estoque": 50, "ativo": "TRUE"},
        {"id": 2, "nome": "Produto B", "preco": 200.00,
            "estoque": 30, "ativo": "TRUE"}
    ],
    "vendas": [
        {"id": 1, "cliente_id": 1, "produto_id": 1, "quantidade": 2,
            "total": 200.00, "data": "2024-01-15", "status": "concluida"}
    ],
    "pagamentos": [
        {"id": 1, "venda_id": 1, "valor": 200.00,
            "data": "2024-01-15", "metodo": "dinheiro"}
    ],
    "logs": []
}


def conectar_sheet():
    """Conecta ao Google Sheets ou retorna dados mockados"""

    # Verifica se está em modo demo (sem credenciais ou variável DEMO_MODE=true)
    demo_mode = os.getenv('DEMO_MODE', 'true').lower() == 'true'

    # Verifica se todas as variáveis de ambiente necessárias estão presentes
    required_vars = ['CLIENT_EMAIL', 'PRIVATE_KEY', 'PROJECT_ID', 'PRIVATE_KEY_ID', 'CLIENT_ID',
                     'AUTH_URI', 'TOKEN_URI', 'AUTH_PROVIDER_X509_CERT_URL', 'CLIENT_X509_CERT_URL']
    env_vars_present = all(os.getenv(var) for var in required_vars)

    if not env_vars_present or demo_mode:
        print("🔧 MODO DEMO: Usando dados simulados")
        return MockSheet()

    # Modo produção - conecta ao Google Sheets real
    for tentativa in range(3):
        try:
            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds_dict = {
                "type": "service_account",
                "project_id": os.environ.get("PROJECT_ID"),
                "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
                "private_key": os.environ.get("PRIVATE_KEY"),
                "client_email": os.environ.get("CLIENT_EMAIL"),
                "client_id": os.environ.get("CLIENT_ID"),
                "auth_uri": os.environ.get("AUTH_URI"),
                "token_uri": os.environ.get("TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
                "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
            }

            creds = Credentials.from_service_account_info(
                creds_dict, scopes=scope)

            client = gspread.authorize(creds)
            return client.open_by_url("https://docs.google.com/spreadsheets/d/1lmJ8ROJi_HqvdevW95rS0Uf49FmZPWg3hpFfeM2jMpo/edit?usp=drive_link")

        except Exception as e:
            print(
                f"Erro ao conectar ao Google Sheets (tentativa {tentativa+1}): {str(e)}")
            time.sleep(1)

    print("❌ Falha na conexão com Google Sheets, usando modo demo")
    return MockSheet()


class MockSheet:
    """Simula uma planilha do Google Sheets com dados mockados"""

    def worksheet(self, nome):
        return MockWorksheet(nome, DADOS_MOCK.get(nome.lower(), []))


class MockWorksheet:
    """Simula uma worksheet do Google Sheets"""

    def __init__(self, nome, dados):
        self.nome = nome
        self.dados = dados.copy()  # Cópia para evitar modificações globais

    def get_all_records(self):
        return self.dados.copy()

    def append_row(self, row):
        print(f"📝 Mock: Adicionando linha à {self.nome}: {row}")
        # Simula adição de dados
        return True

    def update_cell(self, row, col, value):
        print(f"📝 Mock: Atualizando {self.nome} [{row},{col}]: {value}")
        return True

    def delete_rows(self, start_row, end_row=None):
        print(
            f"🗑️ Mock: Removendo linhas {start_row}-{end_row or start_row} de {self.nome}")
        return True
