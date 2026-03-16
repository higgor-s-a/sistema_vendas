# 🚀 Sistema de Vendas - Deploy Vercel Funcional

## ✅ Status: Sistema Pronto!

O código está configurado para:
- **GitHub**: Modo demo (público e seguro)
- **Vercel**: Modo produção (funcional com dados reais)

## 🔧 Configuração Vercel (Para Sistema Funcional)

### Passo 1: Deploy do Código Público
1. Push o código para GitHub público
2. Conecte o repositório ao Vercel
3. Deploy inicial (funcionará em modo demo)

### Passo 2: Ativar Modo Produção no Vercel
No painel do Vercel, configure estas variáveis de ambiente:

#### **Environment Variables:**
```
DEMO_MODE=false
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account","project_id":"sistemavendas-487917",...}
SECRET_KEY=uma-chave-secreta-forte-aqui
```

#### **Como obter GOOGLE_SHEETS_CREDENTIALS:**
1. Vá para [Google Cloud Console](https://console.cloud.google.com)
2. IAM & Admin > Service Accounts
3. Selecione sua service account
4. Keys > Create new key (JSON)
5. **COPIE TODO O CONTEÚDO** do arquivo JSON
6. **COLE INTEIRO** como valor da variável

### Passo 3: Redeploy
Após configurar as variáveis:
1. Vá para Deployments no Vercel
2. Clique em "Redeploy" no último deploy
3. **Aguarde** - o sistema detectará as credenciais e funcionará com dados reais

## 🔐 Segurança Garantida

- ✅ **GitHub**: Código público, mas sem credenciais
- ✅ **Vercel**: Credenciais seguras em variáveis de ambiente
- ✅ **Funcionamento**: Sistema completo com Google Sheets

## 📊 Resultado Final

| Aspecto | GitHub | Vercel |
|---------|--------|--------|
| **Visibilidade** | Público (portfólio) | Público (acesso) |
| **Código** | Visível | Mesmo código |
| **Credenciais** | ❌ Não expostas | ✅ Seguras |
| **Funcionamento** | Demo | ✅ Real |
| **Dados** | Simulados | Google Sheets |

## 🎯 Credenciais de Acesso

Após configurar, use:
- **Usuário:** admin (ou seu usuário real)
- **Senha:** sua senha real do Google Sheets

## 🚨 Importante

1. **Nunca** commite credenciais no GitHub
2. **Sempre** use variáveis de ambiente no Vercel
3. **Monitore** o uso da service account no Google Cloud
4. **Rotacione** chaves periodicamente

## 🔍 Verificação

Após deploy:
1. Acesse: `https://seu-projeto.vercel.app`
2. Login com credenciais reais
3. Verifique se dados são salvos no Google Sheets

---
**✅ Agora você tem portfólio público E sistema funcional!**