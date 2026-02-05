# Guia do Bot Telegram - SENTINEL

Como configurar e usar o bot do Telegram para gerenciar seu sistema SENTINEL remotamente.

---

## Indice

1. [Visao Geral](#visao-geral)
2. [Criar Bot no Telegram](#criar-bot-no-telegram)
3. [Configurar no Sistema](#configurar-no-sistema)
4. [Comandos Disponiveis](#comandos-disponiveis)
5. [Notificacoes Automaticas](#notificacoes-automaticas)
6. [Troubleshooting](#troubleshooting)

---

## 1. Visao Geral

O bot Telegram do SENTINEL permite:
- Receber notificacoes em tempo real
- Executar comandos remotamente
- Ver status do sistema
- Listar reservas e conflitos
- Forcar sincronizacao

---

## 2. Criar Bot no Telegram

### Passo 1: Falar com o BotFather

1. Abra o Telegram
2. Procure por `@BotFather`
3. Inicie conversa clicando em "Start"

### Passo 2: Criar Novo Bot

Digite o comando:
```
/newbot
```

O BotFather vai perguntar:
1. **Nome do bot**: Digite `SENTINEL Controller` (ou o que preferir)
2. **Username do bot**: Digite `sentinel_controller_bot` (deve terminar com _bot)

### Passo 3: Copiar o Token

O BotFather vai responder com algo como:
```
Done! Congratulations on your new bot.
Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

Keep your token secure and store it safely...
```

**COPIE ESSE TOKEN!** Voce vai precisar dele.

---

## 3. Configurar no Sistema

### Passo 1: Adicionar Token ao .env

Abra o arquivo `.env` na raiz do projeto e adicione:

```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

(Use o token que o BotFather te deu)

### Passo 2: Obter seu Chat ID

1. Procure pelo seu bot no Telegram (usando o username)
2. Inicie conversa com ele clicando em "Start"
3. Envie qualquer mensagem (ex: "oi")

### Passo 3: Descobrir o Chat ID

Execute este comando no terminal (com o backend rodando):

```bash
# Windows
python -c "from app.telegram.bot import get_chat_id; get_chat_id()"

# macOS/Linux
python3 -c "from app.telegram.bot import get_chat_id; get_chat_id()"
```

Ou acesse:
```
https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
```

Procure por `"chat":{"id": 123456789}` na resposta.

### Passo 4: Adicionar Chat ID ao .env

```bash
TELEGRAM_CHAT_ID=123456789
```

### Passo 5: Reiniciar Backend

```bash
# Pare o backend (Ctrl+C)
# Inicie novamente:
uvicorn app.main:app --reload
```

### Passo 6: Testar

Envie `/start` para o bot. Ele deve responder!

---

## 4. Comandos Disponiveis

### Comandos Basicos

#### /start
Inicia o bot e mostra menu de comandos.

**Exemplo**:
```
Usuario: /start
Bot: Bem-vindo ao SENTINEL Controller!
     Comandos disponiveis:
     /status - Status do sistema
     /reservas - Proximas reservas
     ...
```

---

#### /status
Mostra status geral do sistema.

**Exemplo**:
```
Usuario: /status
Bot: Sistema: Online
     Reservas Ativas: 3
     Proximos Check-ins: 2
     Conflitos: 0
     Ultima Sync: 10 minutos atras
```

---

#### /reservas
Lista proximas reservas (proximos 7 dias).

**Exemplo**:
```
Usuario: /reservas
Bot: Proximas Reservas:

     Reserva #123
     Imovel: Apartamento 2 Quartos
     Hospede: Joao Silva
     Check-in: 05/02/2026
     Check-out: 08/02/2026

     Reserva #124
     ...
```

---

#### /conflitos
Mostra conflitos de reserva detectados.

**Exemplo**:
```
Usuario: /conflitos
Bot: Conflitos Detectados: 1

     Conflito #1 (ALTO)
     Imovel: Apartamento Centro
     Reserva 1: 01/03 - 05/03
     Reserva 2: 03/03 - 07/03
     Sobreposicao: 2 dias
```

---

#### /sync
Forca sincronizacao de todos os calendarios.

**Exemplo**:
```
Usuario: /sync
Bot: Iniciando sincronizacao...
     Imoveis sincronizados: 3
     Reservas importadas: 5
     Novos conflitos: 0
     Concluido!
```

---

#### /stats
Mostra estatisticas gerais.

**Exemplo**:
```
Usuario: /stats
Bot: Estatisticas do Sistema:

     Total de Imoveis: 3
     Total de Reservas: 45
     Ocupacao Atual: 75%
     Receita Mensal: R$ 12.500,00

     Top Imovel:
     Apartamento Centro (85% ocupacao)
```

---

### Comandos Avancados

#### /imovel [id]
Detalhes de um imovel especifico.

**Exemplo**:
```
Usuario: /imovel 1
Bot: Apartamento 2 Quartos

     Endereco: Rua X, 123
     Capacidade: 4 hospedes
     Preco: R$ 150/noite
     Proximas Reservas: 3
```

---

#### /reserva [id]
Detalhes de uma reserva especifica.

**Exemplo**:
```
Usuario: /reserva 123
Bot: Reserva #123

     Hospede: Joao Silva
     Email: joao@example.com
     Telefone: (62) 99999-9999
     Check-in: 05/02/2026 (14:00)
     Check-out: 08/02/2026 (12:00)
     Total: R$ 450,00
     Status: Confirmada
```

---

#### /cancelar [booking_id]
Cancela uma reserva.

**Exemplo**:
```
Usuario: /cancelar 123
Bot: Tem certeza que deseja cancelar a reserva #123?
     Hospede: Joao Silva
     Check-in: 05/02/2026

     Digite /confirmar_cancelar_123 para confirmar
```

---

## 5. Notificacoes Automaticas

O bot envia notificacoes automaticamente para os seguintes eventos:

### Nova Reserva
```
Nova Reserva Detectada!

Reserva #125
Imovel: Apartamento Centro
Hospede: Maria Santos
Check-in: 15/03/2026
Check-out: 18/03/2026
Fonte: Airbnb
```

### Check-in Hoje
```
Check-in HOJE!

Reserva #123
Imovel: Apartamento 2 Quartos
Hospede: Joao Silva
Horario: 14:00
Telefone: (62) 99999-9999
```

### Check-out Hoje
```
Check-out HOJE!

Reserva #120
Imovel: Apartamento Centro
Hospede: Pedro Lima
Horario: 12:00
Lembrar de vistoria!
```

### Conflito Detectado
```
ALERTA: Conflito de Reserva!

Imovel: Apartamento Centro
Severidade: ALTA

Reserva 1: 01/03 - 05/03 (Airbnb)
Reserva 2: 03/03 - 07/03 (Booking)

Acao necessaria!
```

### Erro de Sincronizacao
```
Erro na Sincronizacao

Imovel: Apartamento 2 Quartos
Erro: URL de calendario invalida
Tentativa: 3/3

Verifique as configuracoes.
```

---

## 6. Configuracoes Avancadas

### Personalizar Mensagens

Edite os templates em `app/telegram/notifications.py`:

```python
def format_new_booking(booking):
    return f"""
    Nova Reserva!

    Hospede: {booking.guest.name}
    ...
    """
```

### Adicionar Novos Comandos

Em `app/telegram/bot.py`:

```python
@bot.message_handler(commands=['meucomando'])
def meu_comando(message):
    bot.reply_to(message, "Resposta do comando")
```

### Configurar Horarios de Notificacao

Em `.env`:

```bash
TELEGRAM_NOTIFICATIONS_ENABLED=True
TELEGRAM_QUIET_HOURS_START=22
TELEGRAM_QUIET_HOURS_END=8
```

---

## 7. Troubleshooting

### Bot nao responde

**Causa**: Token invalido ou nao configurado

**Solucao**:
1. Verifique o token no `.env`
2. Reinicie o backend
3. Envie `/start` novamente

---

### Nao recebo notificacoes

**Causa**: Chat ID incorreto

**Solucao**:
1. Verifique o chat ID no `.env`
2. Confirme que iniciou conversa com o bot
3. Teste com `/status`

---

### Erro "Unauthorized"

**Causa**: Token expirou ou foi revogado

**Solucao**:
1. Crie novo bot com BotFather
2. Atualize o token no `.env`
3. Reinicie o backend

---

### Comandos nao funcionam

**Causa**: Bot nao esta rodando

**Solucao**:
1. Verifique se backend esta rodando
2. Veja logs do backend para erros
3. Teste acesso a API do Telegram

---

## 8. Seguranca

### Proteger o Token

- **NUNCA** compartilhe o token do bot
- **NUNCA** commite o `.env` no Git
- Use `.gitignore` para excluir `.env`

### Restringir Acesso

Apenas usuarios com o chat ID configurado podem usar o bot.

Para adicionar multiplos usuarios:

```bash
TELEGRAM_CHAT_ID=123456789,987654321,555666777
```

### Regenerar Token

Se o token vazar:

1. Fale com @BotFather
2. Digite `/mybots`
3. Selecione seu bot
4. Clique em "API Token"
5. Clique em "Revoke current token"
6. Copie o novo token
7. Atualize `.env`

---

## 9. Recursos Adicionais

- [Documentacao Telegram Bot API](https://core.telegram.org/bots/api)
- [pyTelegramBotAPI Docs](https://github.com/eternnoir/pyTelegramBotAPI)
- [BotFather Commands](https://core.telegram.org/bots#6-botfather)

---

## 10. Exemplos de Uso no Dia a Dia

### Verificar Sistema pela Manha
```
Usuario: /status
Bot: [Status do sistema]

Usuario: /reservas
Bot: [Proximas reservas]

Usuario: /conflitos
Bot: Nenhum conflito detectado
```

### Sincronizar Manualmente
```
Usuario: /sync
Bot: Sincronizacao iniciada...
     [Resultado]
```

### Ver Detalhes de uma Reserva
```
Usuario: /reservas
Bot: [Lista]

Usuario: /reserva 123
Bot: [Detalhes completos]
```

---

**Aproveite o poder do Telegram para gerenciar seu SENTINEL remotamente!**

**Atualizado**: 2026-02-04
