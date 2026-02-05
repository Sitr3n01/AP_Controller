# 🚀 Guia de Início Rápido - SENTINEL

## Instalação em 5 Minutos

### 1. Pré-requisitos
- Python 3.11+
- Git

### 2. Instalação

```bash
# Clone
git clone https://github.com/Sitr3n01/AP_Controller.git
cd AP_Controller

# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Dependências
pip install -r requirements.txt

# Configuração
cp .env.example .env
# Edite .env com SECRET_KEY:
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))" >> .env
```

### 3. Primeiro Uso

```bash
# Iniciar servidor
uvicorn app.main:app --reload

# Abrir navegador
http://localhost:8000/docs
```

### 4. Configurar Calendários

No arquivo `.env`:
```bash
AIRBNB_ICAL_URL=<sua_url_ical_airbnb>
BOOKING_ICAL_URL=<sua_url_ical_booking>
```

### 5. Testar

```bash
# Via API docs: http://localhost:8000/docs
# Ou curl:
curl http://localhost:8000/health
```

✅ **Pronto! Sistema funcionando!**

## Próximos Passos

- Configure email para notificações
- Configure bot Telegram
- Explore a documentação completa

Veja: [USER_GUIDE.md](USER_GUIDE.md)
