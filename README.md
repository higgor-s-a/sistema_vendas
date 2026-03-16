# Sistema de Vendas

Sistema web para gerenciamento de vendas, clientes, produtos e pagamentos usando Flask e Google Sheets.

## Deploy no Vercel

### Pré-requisitos

1. Conta no [Vercel](https://vercel.com)
2. Projeto no Google Cloud com Service Account configurado
3. Arquivo de credenciais do Google Service Account

### Configuração das Variáveis de Ambiente

No painel do Vercel, adicione as seguintes variáveis de ambiente:

- `GOOGLE_SHEETS_CREDENTIALS`: Conteúdo completo do arquivo `credenciais.json` (copie todo o JSON como uma string)

### Arquivos de Configuração

O projeto já inclui:
- `vercel.json`: Configuração do Vercel
- `requirements.txt`: Dependências Python
- `.vercelignore`: Arquivos a serem ignorados no deploy

### Como fazer o deploy

1. Faça push do código para um repositório Git (GitHub, GitLab, etc.)
2. Conecte o repositório ao Vercel
3. Configure as variáveis de ambiente
4. Faça o deploy

### Estrutura do Projeto

- `api/index.py`: Ponto de entrada para o Vercel
- `webapp.py`: Aplicação Flask principal
- `services/`: Serviços de autenticação e integração com Google Sheets
- `templates/`: Templates HTML
- `static/`: Arquivos estáticos (CSS, JS, imagens)
- `database/`: Funções de acesso aos dados

### Configuração do Google Sheets

1. Crie uma planilha no Google Sheets
2. Compartilhe a planilha com o email do Service Account
3. Configure as abas: usuarios, clientes, produtos, vendas, pagamentos

### Desenvolvimento Local

```bash
pip install -r requirements.txt
python webapp.py
```

### Suporte

Para dúvidas sobre o deploy no Vercel, consulte a [documentação oficial](https://vercel.com/docs).