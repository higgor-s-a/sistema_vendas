# Sistema de Vendas - Versão Demo

Esta é uma versão DEMO do sistema de vendas, configurada para funcionar sem credenciais reais do Google Sheets.

## 🎯 Estratégia de Segurança

Este repositório pode ser **público** porque:
- ✅ Usa dados mockados (não conecta ao Google Sheets real)
- ✅ Não contém credenciais reais
- ✅ Demonstra funcionalidades completas
- ✅ Seguro para portfólio

## ⚠️ IMPORTANTE
Esta versão usa dados simulados e NÃO se conecta ao Google Sheets real.
Para versão completa, configure as credenciais conforme documentação privada.

## 🚀 Deploy Público (Demo)

### Passo 1: Configurar Modo Demo
```bash
./setup_mode.sh
# Escolha opção 1 (Demo)
```

### Passo 2: Deploy no Vercel
1. Fork este repositório
2. Conecte ao Vercel
3. **Deploy direto** (sem variáveis de ambiente necessárias)
4. Acesse: `https://seu-projeto.vercel.app`

## 🔐 Credenciais Demo
- **Usuário:** admin
- **Senha:** demo123

## 📊 Funcionalidades Demo
- ✅ Interface de login
- ✅ Dashboard com dados simulados
- ✅ CRUD de clientes (dados locais)
- ✅ Sistema de vendas simulado
- ✅ Relatórios básicos
- ✅ Logs de auditoria

## 🔄 Modo Produção (Privado)

Para versão completa com Google Sheets:

### 1. Criar Repositório Privado
```bash
./setup_mode.sh
# Escolha opção 2 (Produção)
```

### 2. Configurar Vercel
Variáveis de ambiente necessárias:
- `GOOGLE_SHEETS_CREDENTIALS`: Credenciais do Service Account
- `SECRET_KEY`: Chave secreta para sessões
- `DEMO_MODE`: false

### 3. Configurar Google Cloud
- Service Account com permissões
- Planilha Google Sheets compartilhada

## 📁 Estrutura do Projeto
```
api/           # Endpoints Vercel
├── index.py   # App principal
└── debug.py   # Diagnóstico

services/      # Lógica de negócio
├── sheets.py  # Google Sheets (ou mock)
├── auth_service.py
└── log_service.py

templates/     # Interface web
static/        # CSS, JS, imagens
database/      # Configurações (não incluído)
```

## 🛡️ Segurança Implementada
- `.gitignore` protege credenciais
- Modo demo automático sem credenciais
- Variáveis de ambiente para produção
- Dados mockados para demonstração

## 🎨 Personalização
Para usar como portfólio:
- Modifique templates em `templates/`
- Adicione funcionalidades em `services/`
- Customize estilos em `static/`
- Adapte dados mockados em `services/sheets.py`

---
*Para versão completa, consulte a documentação privada ou entre em contato.*