# Configuração Render para Produção

## 1. Dashboard Render → Environment Variables (TODAS obrigatórias)

```
DEMO_MODE=false
SECRET_KEY=chave-super-secreta-$(openssl rand -hex 32)

# Google Sheets Service Account (RAW de database/credenciais.json)
PROJECT_ID=sistemavendas-487917
PRIVATE_KEY_ID=b789ce5ee3077d5b5299dc1b5dd19862625c78ad
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDqUujukXy4RePf
1SBIAkve+viv9F2IfdJIZonpn7VlhZQXyL8dAc68otjreRJRtElaKWCR6ph1CtmQ
[... COMPLETE PEM sem ', preserve ENTER para \\n ...]
-----END PRIVATE KEY-----
CLIENT_EMAIL=sistema-vendas@sistemavendas-487917.iam.gserviceaccount.com
CLIENT_ID=111034601948906795404
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/sistema-vendas@sistemavendas-487917.iam.gserviceaccount.com
```

**IMPORTANTE PRIVATE_KEY:**
- Multi-line
- Cole **RAW** do `"private_key"` em credenciais.json
- **SEM** `'` ou extra `\`

## 2. Settings (auto de render.yaml ou manual):
```
Runtime: Python
Build: pip install -r requirements.txt
Start: python webapp.py
```

## 3. Login após redeploy:
- **higgor.alves** / **[sua senha]**
- Dados da planilha real (https://docs.google.com/spreadsheets/d/1lmJ8ROJi_HqvdevW95rS0Uf49FmZPWg3hpFfeM2jMpo)

## 4. Verificar:
- Sem "MODO DEMO"
- Usuários da planilha real
- Logs OK

URL: https://sistema-vendas-82e0.onrender.com
