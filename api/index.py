import sys
import os

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from webapp import app

# Exporta o app para Vercel
app = app
