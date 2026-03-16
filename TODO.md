# TODO.md - Progresso do Deploy no Render (Atualizado)

## ✅ 1. Criar arquivo .env com configurações
- [x] Criado .env com SECRET_KEY, DEMO_MODE, Google Sheets creds

## ✅ 2. Testar localmente
- [x] Executado `python test_deploy.py` (import error devido a env Anaconda; foco em Render)
- [x] App Flask rodando localmente em http://127.0.0.1:5000 (servidor ativo)

## ✅ 3. Preparar para Render
- [x] Criado Procfile e render.yaml
- [x] Atualizado webapp.py para bind 0.0.0.0:$PORT (Render compatível)
- [ ] Push para Git repo público/privado (.env já em .gitignore)
- [ ] Render → New Web Service → Connect repo → Use render.yaml ou set Build/Start cmds
- [ ] Environment: Copie vars do .env (PRIVATE_KEY multi-line!)

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

