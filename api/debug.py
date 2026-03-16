import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_basic():
    """Testa funcionalidades básicas"""
    try:
        # Testa imports básicos
        import flask
        import gspread
        import json

        # Testa se conseguimos criar uma app Flask simples
        from flask import Flask
        app = Flask(__name__)

        @app.route('/')
        def hello():
            return 'Hello from Vercel!'

        # Testa se conseguimos acessar as variáveis de ambiente
        creds = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        if creds:
            try:
                creds_dict = json.loads(creds)
                return f'Success: Credenciais carregadas, project_id: {creds_dict.get("project_id", "unknown")}'
            except:
                return 'Error: Credenciais malformadas'
        else:
            return 'Warning: GOOGLE_SHEETS_CREDENTIALS não definida'

    except Exception as e:
        return f'Error: {str(e)}'

# Para Vercel
app = Flask(__name__)

@app.route('/')
def home():
    result = test_basic()
    return f'<h1>Test Result</h1><p>{result}</p>'

@app.route('/debug')
def debug():
    import traceback
    try:
        from webapp import app as main_app
        return 'Main app import successful'
    except Exception as e:
        return f'<pre>{traceback.format_exc()}</pre>'