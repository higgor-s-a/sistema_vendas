# Sistema de Vendas

Sistema web para gerenciamento de vendas, clientes, produtos e pagamentos usando Flask e Google Sheets.

## ⚠️ IMPORTANTE - Segurança

**NUNCA commite arquivos de credenciais no Git!**

- O arquivo `database/credenciais.json` está no `.gitignore`
- Use variáveis de ambiente para credenciais em produção
- Mantenha seu repositório privado se possível

## Deploy no Vercel

### Pré-requisitos

1. Conta no [Vercel](https://vercel.com)
2. Projeto no Google Cloud com Service Account configurado
3. Arquivo de credenciais do Google Service Account

### Configuração das Variáveis de Ambiente

No painel do Vercel, adicione as seguintes variáveis de ambiente:

- `GOOGLE_SHEETS_CREDENTIALS`: Conteúdo completo do arquivo `credenciais.json` (copie todo o JSON como uma string)
- `SECRET_KEY`: Chave secreta para sessões Flask (ex: `openssl rand -hex 32`)

### Arquivos de Configuração

O projeto já inclui:
- `vercel.json`: Configuração do Vercel
- `requirements.txt`: Dependências Python
- `.vercelignore`: Arquivos a serem ignorados no deploy
- `.gitignore`: Arquivos a serem ignorados pelo Git

### Como fazer o deploy

1. Faça push do código para um repositório Git (GitHub, GitLab, etc.)
2. Conecte o repositório ao Vercel
3. Configure as variáveis de ambiente
4. Faça o deploy

### Desenvolvimento Local

```bash
pip install -r requirements.txt
python webapp.py
```

### Endpoints de Debug

- `/debug`: Testa funcionalidades básicas
- `/`: Página inicial (requer login)

### Segurança Adicional

- Mantenha seu repositório privado
- Use variáveis de ambiente para credenciais
- Regularmente rotacione as chaves do Service Account
- Monitore o uso das credenciais no Google Cloud Console

### Suporte

Para dúvidas sobre o deploy no Vercel, consulte a [documentação oficial](https://vercel.com/docs).