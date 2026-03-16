# TODO.md - Progresso do Deploy no Render (Atualizado)

## ✅ 1. Criar arquivo .env com configurações
- [x] Criado .env com SECRET_KEY, DEMO_MODE, Google Sheets creds

## ✅ 2. Testar localmente
- [x] Executado `python test_deploy.py` (import error devido a env Anaconda; foco em Render)
- [x] App Flask rodando localmente em http://127.0.0.1:5000 (servidor ativo)

## ✅ 3. Preparar para Render
- [x] Criado Procfile e render.yaml
- [x] Atualizado webapp.py para bind 0.0.0.0:$PORT (Render compatível)
- [x] Criado test_sheets_render.py para teste conexão Sheets
- [ ] Deploy feito, app em https://sistema-vendas-82e0.onrender.com
- [ ] Fix PRIVATE_KEY no Render dashboard (remover \\ escapes)


## ☐ 4. Deploy e Teste
- Deploy automático via Git
- Testar URL do Render
- Verificar Sheets integration e dados mock fallback

## ☐ 5. Opcional: Persistência DB
- Anexar PostgreSQL no Render (auto DATABASE_URL)
- Migrar SQLite para Postgres se necessário

## ☐ 4. Deploy e Teste
- Deploy automático via Git
- Testar URL do Render
- Verificar Sheets integration e dados mock fallback

## ☐ 5. Opcional: Persistência DB
- Anexar PostgreSQL no Render (auto DATABASE_URL)
- Migrar SQLite para Postgres se necessário

