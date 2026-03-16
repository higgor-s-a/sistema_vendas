#!/bin/bash
echo "=== Sistema de Vendas - Configuração Final ==="
echo ""
echo "Este script configura o sistema para:"
echo "1. Repositório público com modo demo (seguro)"
echo "2. Deploy no Vercel"
echo "3. Funcionamento offline com dados simulados"
echo ""

# Configurar modo demo
echo "🔧 Configurando modo demo..."
echo "DEMO_MODE=true" > .env
echo "✅ Modo demo ativado!"
echo ""

# Verificar se .gitignore existe
if [ ! -f ".gitignore" ]; then
    echo "❌ Arquivo .gitignore não encontrado!"
    exit 1
fi

echo "🛡️ Verificando proteções de segurança..."
if grep -q "database/credenciais.json" .gitignore; then
    echo "✅ Credenciais protegidas no .gitignore"
else
    echo "❌ Credenciais não protegidas!"
    exit 1
fi
echo ""

# Testar modo demo
echo "🧪 Testando modo demo..."
python3 -c "
import os
os.environ['DEMO_MODE'] = 'true'
try:
    from services.sheets import conectar_sheet
    sheet = conectar_sheet()
    print('✅ Modo demo funcionando!')
except Exception as e:
    print(f'❌ Erro no modo demo: {e}')
    exit(1)
"
echo ""

echo "🎉 Configuração concluída!"
echo ""
echo "=== PRÓXIMOS PASSOS ==="
echo ""
echo "1. 📤 Faça push para repositório público:"
echo "   git add ."
echo "   git commit -m 'Versão demo para portfólio'"
echo "   git push origin main"
echo ""
echo "2. 🌐 Deploy no Vercel:"
echo "   - Fork o repositório"
echo "   - Conecte ao Vercel"
echo "   - Deploy direto (sem variáveis necessárias)"
echo ""
echo "3. 🔐 Credenciais demo:"
echo "   - Usuário: admin"
echo "   - Senha: demo123"
echo ""
echo "4. 📊 Acesse:"
echo "   https://seu-projeto.vercel.app"
echo ""
echo "=== PARA VERSÃO COMPLETA ==="
echo "Para usar com Google Sheets real:"
echo "1. Crie repositório PRIVADO"
echo "2. Execute: ./setup_mode.sh (opção 2)"
echo "3. Configure variáveis no Vercel"
echo ""
echo "✅ Sistema pronto para portfólio público! 🚀"