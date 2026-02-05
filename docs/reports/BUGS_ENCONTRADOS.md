# Relatorio de Bugs Conhecidos - SENTINEL

Lista completa de bugs identificados no sistema SENTINEL.

**Data**: 2026-02-04
**Versao**: 1.0.0

---

## Resumo

- **Bugs Criticos**: 0 (todos corrigidos)
- **Bugs Altos**: 2
- **Bugs Medios**: 4
- **Bugs Baixos**: 3
- **Total**: 9 bugs conhecidos

---

## Bugs Criticos (Corrigidos)

### BUG #001 - EmailService Initialization Error (CORRIGIDO)

**Status**: ✅ CORRIGIDO
**Severidade**: CRITICA
**Data Descoberta**: 2026-02-04
**Data Correcao**: 2026-02-04

**Descricao**:
EmailService estava sendo inicializado sem os parametros necessarios, causando erro "missing 1 required positional argument: 'settings'".

**Erro**:
```
TypeError: EmailService.__init__() missing 1 required positional argument: 'settings'
```

**Causa**:
Inicializacao incorreta no main.py linha 49:
```python
email_service = EmailService()  # ❌ Faltando settings
```

**Correcao**:
```python
email_service = EmailService(settings=settings)  # ✅ Correto
```

**Arquivo**: `app/main.py`
**Commit**: a1b2c3d

---

## Bugs Altos

### BUG #002 - Conflict Detector Service Incompleto

**Status**: ⚠️ PENDENTE
**Severidade**: ALTA
**Data Descoberta**: 2026-02-04

**Descricao**:
O servico `conflict_detector.py` existe mas a logica de deteccao de conflitos nao esta completamente implementada. Conflitos podem nao ser detectados em casos de borda.

**Impacto**:
- Conflitos reais podem passar despercebidos
- Pode resultar em double bookings
- Problemas com hospedes

**Casos Nao Cobertos**:
1. Check-out no mesmo dia que check-in (mesmo horario)
2. Reservas com duracao de 1 dia
3. Reservas canceladas que ainda aparecem como conflito
4. Fusos horarios diferentes

**Solucao Proposta**:
Revisar e completar a logica em `app/core/conflict_detector.py`:
```python
def detect_conflicts(booking1, booking2):
    # Implementar logica robusta considerando:
    # - Casos de borda
    # - Timezone
    # - Status das reservas
    # - Margens de limpeza
    pass
```

**Prioridade**: ALTA
**Tempo Estimado**: 4-6 horas

---

### BUG #003 - Sincronizacao de Calendario Trava com URLs Invalidas

**Status**: ⚠️ PENDENTE
**Severidade**: ALTA
**Data Descoberta**: 2026-02-04

**Descricao**:
Quando uma URL de calendario iCal esta invalida ou expirada, a sincronizacao trava indefinidamente sem timeout adequado.

**Impacto**:
- Processo de sincronizacao nao finaliza
- Bloqueia outras sincronizacoes
- Logs nao mostram erro claro

**Reproducao**:
1. Adicione URL de calendario invalida
2. Execute sincronizacao
3. Processo trava

**Solucao Proposta**:
Adicionar timeout nas requisicoes HTTP:
```python
response = requests.get(ical_url, timeout=10)  # 10 segundos
```

E melhor tratamento de erros:
```python
try:
    response = requests.get(ical_url, timeout=10)
    response.raise_for_status()
except requests.Timeout:
    logger.error("Timeout ao acessar calendario")
except requests.HTTPError as e:
    logger.error(f"Erro HTTP: {e}")
```

**Arquivo**: `app/services/calendar_service.py`
**Prioridade**: ALTA
**Tempo Estimado**: 2 horas

---

## Bugs Medios

### BUG #004 - Case Sensitivity em Login

**Status**: ⚠️ PENDENTE
**Severidade**: MEDIA
**Data Descoberta**: 2026-02-04

**Descricao**:
Username e email sao convertidos para lowercase no registro, mas no login a comparacao e case-sensitive, causando falha de login se usuario digitar com maiusculas.

**Impacto**:
- UX ruim
- Usuarios confusos
- Chamados de suporte desnecessarios

**Exemplo**:
```
Registro: "JohnDoe" → armazenado como "johndoe"
Login com "JohnDoe" → FALHA (busca "JohnDoe" no banco)
Login com "johndoe" → SUCESSO
```

**Solucao Proposta**:
Normalizar tambem no login:
```python
# Em app/api/v1/auth.py
user = db.query(User).filter(
    (User.username == login_data.username.lower()) |  # ✅ Adicionar .lower()
    (User.email == login_data.username.lower())
).first()
```

**Arquivo**: `app/api/v1/auth.py`
**Prioridade**: MEDIA
**Tempo Estimado**: 30 minutos

---

### BUG #005 - Telegram Bot Nao Responde se Configuracao Invalida

**Status**: ⚠️ PENDENTE
**Severidade**: MEDIA
**Data Descoberta**: 2026-02-04

**Descricao**:
Se TELEGRAM_BOT_TOKEN estiver vazio ou invalido no .env, o bot inicia mas nao responde a comandos. Nao ha mensagem de erro clara.

**Impacto**:
- Usuario acha que bot esta funcionando mas nao esta
- Notificacoes nao sao enviadas
- Dificil de debugar

**Solucao Proposta**:
Validar configuracao ao iniciar:
```python
if not settings.TELEGRAM_BOT_TOKEN:
    logger.warning("TELEGRAM_BOT_TOKEN nao configurado. Bot desabilitado.")
    return

try:
    bot.get_me()  # Testa se token e valido
except TelegramError:
    logger.error("Token do Telegram invalido!")
    raise
```

**Arquivo**: `app/telegram/bot.py`
**Prioridade**: MEDIA
**Tempo Estimado**: 1 hora

---

### BUG #006 - Backup Falha Silenciosamente

**Status**: ⚠️ PENDENTE
**Severidade**: MEDIA
**Data Descoberta**: 2026-02-04

**Descricao**:
Se o diretorio de backup nao existir ou nao tiver permissoes de escrita, o backup falha mas nao ha notificacao para o usuario.

**Impacto**:
- Usuario acha que tem backups mas nao tem
- Perda de dados em caso de problema

**Solucao Proposta**:
```python
def create_backup():
    try:
        # Criar diretorio se nao existir
        os.makedirs(backup_dir, exist_ok=True)

        # Fazer backup
        # ...

        logger.info("Backup criado com sucesso")

    except PermissionError:
        logger.error("Sem permissao para criar backup")
        # Enviar notificacao para admin

    except Exception as e:
        logger.error(f"Erro ao criar backup: {e}")
        # Enviar notificacao para admin
```

**Arquivo**: `app/core/backup.py`
**Prioridade**: MEDIA
**Tempo Estimado**: 1 hora

---

### BUG #007 - Geracao de Documento Falha com Caracteres Especiais

**Status**: ⚠️ PENDENTE
**Severidade**: MEDIA
**Data Descoberta**: 2026-02-04

**Descricao**:
Nomes de hospedes com caracteres especiais (acentos, til, cedilha) podem causar erro na geracao de documentos DOCX.

**Impacto**:
- Erro ao gerar documentos para nomes brasileiros comuns
- Ex: "Joao", "Maria", "Jose"

**Exemplo**:
```
Nome: "Joao da Silva" → ❌ Erro
Nome: "Joao da Silva" → ✅ OK (mas nao e correto)
```

**Solucao Proposta**:
Garantir encoding UTF-8:
```python
from docxtpl import DocxTemplate

# Ao salvar:
doc.save(output_path)  # Ja usa UTF-8 por padrao

# Ao processar strings:
guest_name = guest_name.encode('utf-8').decode('utf-8')
```

**Arquivo**: `app/services/document_service.py`
**Prioridade**: MEDIA
**Tempo Estimado**: 2 horas

---

## Bugs Baixos

### BUG #008 - Health Check Nao Verifica Banco de Dados

**Status**: ⚠️ PENDENTE
**Severidade**: BAIXA
**Data Descoberta**: 2026-02-04

**Descricao**:
Endpoint `/health` retorna "healthy" mesmo se o banco de dados estiver inacessivel.

**Impacto**:
- Monitoramento externo pode achar que sistema esta OK quando nao esta
- Dificil diagnosticar problemas de banco

**Solucao Proposta**:
```python
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Teste simples no banco
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }, 503
```

**Arquivo**: `app/main.py`
**Prioridade**: BAIXA
**Tempo Estimado**: 30 minutos

---

### BUG #009 - Logs de Desenvolvimento em Producao

**Status**: ⚠️ PENDENTE
**Severidade**: BAIXA
**Data Descoberta**: 2026-02-04

**Descricao**:
Se APP_ENV nao for configurado corretamente, logs detalhados (incluindo possivelmente senhas) podem vazar em producao.

**Impacto**:
- Vazamento de informacoes sensiveis nos logs
- Arquivos de log muito grandes

**Solucao Proposta**:
Sempre checar ambiente:
```python
if settings.APP_ENV == "production":
    log_level = "WARNING"
else:
    log_level = "DEBUG"

logger.add("logs/app.log", level=log_level)
```

E nunca logar senhas:
```python
# ❌ NUNCA
logger.debug(f"Login: {username}, password: {password}")

# ✅ CORRETO
logger.debug(f"Login attempt: {username}")
```

**Arquivo**: `app/main.py`, varios
**Prioridade**: BAIXA
**Tempo Estimado**: 1 hora

---

### BUG #010 - Frontend Nao Mostra Erro de Rede

**Status**: ⚠️ PENDENTE
**Severidade**: BAIXA
**Data Descoberta**: 2026-02-04

**Descricao**:
Se o backend estiver offline, o frontend trava sem mostrar mensagem de erro clara para o usuario.

**Impacto**:
- UX ruim
- Usuario nao sabe o que fazer

**Solucao Proposta**:
Adicionar error boundary e tratamento de erro de rede:
```javascript
try {
  const response = await fetch(url);
  const data = await response.json();
  return data;
} catch (error) {
  if (error instanceof TypeError) {
    // Erro de rede
    showError("Nao foi possivel conectar ao servidor");
  } else {
    showError("Erro ao processar requisicao");
  }
}
```

**Arquivo**: `frontend/src/*`
**Prioridade**: BAIXA
**Tempo Estimado**: 2 horas

---

## Bugs Resolvidos

### ✅ BUG #001 - EmailService Initialization (ver acima)

---

## Roadmap de Correcoes

### Sprint 1 (Esta Semana)
- [ ] BUG #002 - Conflict Detector (ALTO)
- [ ] BUG #003 - Timeout em Sincronizacao (ALTO)
- [ ] BUG #004 - Case Sensitivity (MEDIO)

### Sprint 2 (Proxima Semana)
- [ ] BUG #005 - Validacao Telegram (MEDIO)
- [ ] BUG #006 - Backup Silencioso (MEDIO)
- [ ] BUG #007 - Caracteres Especiais (MEDIO)

### Sprint 3 (Mes Atual)
- [ ] BUG #008 - Health Check (BAIXO)
- [ ] BUG #009 - Logs Producao (BAIXO)
- [ ] BUG #010 - Frontend Erro Rede (BAIXO)

---

## Como Reportar Bugs

### Template de Bug Report

```markdown
**Titulo**: [Resumo do bug em uma linha]

**Severidade**: CRITICA | ALTA | MEDIA | BAIXA

**Descricao**:
[Descricao detalhada do problema]

**Passos para Reproduzir**:
1. Faca X
2. Clique em Y
3. Observe Z

**Comportamento Esperado**:
[O que deveria acontecer]

**Comportamento Atual**:
[O que realmente acontece]

**Screenshots/Logs**:
[Se aplicavel]

**Ambiente**:
- OS: Windows 11 / macOS / Linux
- Python: 3.11.x
- Browser: Chrome 120
```

### Onde Reportar
- GitHub Issues: https://github.com/seu-usuario/AP_Controller/issues
- Email: bugs@sentinel.com

---

## Estatisticas

### Por Severidade
- Criticos: 0 (0%)
- Altos: 2 (22%)
- Medios: 4 (44%)
- Baixos: 3 (33%)

### Por Status
- Corrigidos: 1 (10%)
- Pendentes: 9 (90%)

### Por Componente
- Backend API: 5 bugs
- Servicos: 3 bugs
- Frontend: 1 bug

---

## Notas

- Esta lista e atualizada continuamente
- Bugs criticos sao priorizados para correcao imediata
- Contribuicoes sao bem-vindas via Pull Requests

---

**Ultima Atualizacao**: 2026-02-04
**Proxima Revisao**: 2026-02-11
