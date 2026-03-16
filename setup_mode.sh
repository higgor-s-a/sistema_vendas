#!/bin/bash
echo "=== Configuração do Sistema de Vendas ==="
echo ""
echo "Escolha o modo de operação:"
echo "1) Modo Demo (dados simulados - seguro para repositório público)"
echo "2) Modo Produção (conecta ao Google Sheets real)"
echo ""

read -p "Digite 1 para Demo ou 2 para Produção: " mode

if [ "$mode" = "1" ]; then
    echo "🔧 Configurando MODO DEMO..."
    echo "DEMO_MODE=true" > .env
    echo "✅ Modo demo ativado!"
    echo ""
    echo "Credenciais demo:"
    echo "- Usuário: admin"
    echo "- Senha: demo123"
    echo ""
    echo "Para deploy público, use apenas este modo."

elif [ "$mode" = "2" ]; then
    echo "🏭 Configurando MODO PRODUÇÃO..."
    echo "DEMO_MODE=false" > .env
    echo "✅ Modo produção ativado!"
    echo ""
    echo "IMPORTANTE: Configure as variáveis de ambiente no Vercel:"
    echo "- GOOGLE_SHEETS_CREDENTIALS"
    echo "- SECRET_KEY"
    echo ""
    echo "Para repositório privado, use este modo."

else
    echo "❌ Opção inválida!"
    exit 1
fi

echo ""
echo "Para alterar o modo, execute este script novamente."
echo "Para deploy, faça push para o repositório Git."