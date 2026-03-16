# Configuração das variáveis de ambiente para Vercel
# Execute este script para configurar as variáveis automaticamente

echo "Configurando variáveis de ambiente para Vercel..."

# Verifica se o arquivo de credenciais existe
if [ ! -f "database/credenciais.json" ]; then
    echo "Erro: Arquivo database/credenciais.json não encontrado!"
    echo "Certifique-se de que o arquivo de credenciais está no local correto."
    exit 1
fi

# Lê o conteúdo do arquivo de credenciais
CREDENTIALS=$(cat database/credenciais.json | jq -c .)

echo "Conteúdo das credenciais lido com sucesso."
echo ""
echo "Agora você precisa configurar as seguintes variáveis no Vercel:"
echo ""
echo "1. Acesse https://vercel.com/dashboard"
echo "2. Selecione seu projeto"
echo "3. Vá para Settings > Environment Variables"
echo "4. Adicione a variável:"
echo "   Name: GOOGLE_SHEETS_CREDENTIALS"
echo "   Value: $CREDENTIALS"
echo ""
echo "IMPORTANTE: O conteúdo das credenciais foi preparado acima."
echo "Copie exatamente o valor que aparece após 'Value:'"