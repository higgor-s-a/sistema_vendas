# 🔒 Guia de Resolução - Credenciais Expostas no GitHub

## ❌ Problema Identificado
Suas credenciais do Google Service Account foram expostas publicamente no GitHub, resultando na desabilitação automática da chave pelo Google.

## ✅ Soluções Implementadas

### 1. Credenciais Removidas do Histórico
- Arquivo `database/credenciais.json` removido completamente do histórico Git
- Histórico limpo usando `git filter-repo`

### 2. Proteções de Segurança Adicionadas
- `.gitignore` configurado para nunca commitar credenciais
- `.vercelignore` atualizado
- Documentação de segurança no README

### 3. Nova Chave de Serviço Account
Você já criou uma nova chave - isso é correto!

## 🚀 Próximos Passos

### Passo 1: Criar Novo Repositório GitHub
1. **DELETE** o repositório antigo `sistema_vendas` no GitHub
2. Crie um **NOVO** repositório com o mesmo nome
3. **IMPORTANTE**: Configure como **PRIVADO** para maior segurança

### Passo 2: Configurar e Fazer Push
Execute o script `setup_github.sh`:
```bash
./setup_github.sh
```
Ou manualmente:
```bash
git remote add origin https://github.com/SEU_USERNAME/sistema_vendas.git
git push -u origin main
```

### Passo 3: Atualizar Vercel
1. No painel do Vercel, vá para seu projeto
2. **Environment Variables**:
   - `GOOGLE_SHEETS_CREDENTIALS`: Cole o conteúdo do NOVO `credenciais.json`
   - `SECRET_KEY`: Gere uma nova chave (ex: `openssl rand -hex 32`)
3. **Redeploy** o projeto

### Passo 4: Verificar Segurança no Google Cloud
1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Vá para **IAM & Admin > Service Accounts**
3. **DELETE** a chave antiga (ID: ca547fcedac1a152961dcbd576ca89c9f35bdd75)
4. Verifique se a nova chave está ativa

## 🛡️ Medidas de Segurança Futuras

### Repositório
- Mantenha sempre **PRIVADO**
- Use `.gitignore` para arquivos sensíveis

### Credenciais
- Nunca commite chaves API ou credenciais
- Use variáveis de ambiente em produção
- Rotacione chaves regularmente

### Google Cloud
- Monitore o uso do Service Account
- Configure alertas de segurança
- Use princípios de menor privilégio

## 🔍 Verificação

Após seguir os passos acima:
1. Teste o login no Vercel
2. Verifique se não há erros de autenticação
3. Confirme que o Service Account está funcionando

## 📞 Suporte

Se ainda houver problemas:
- Verifique os logs do Vercel
- Teste localmente com `python test_deploy.py`
- Use o endpoint `/debug` para diagnóstico