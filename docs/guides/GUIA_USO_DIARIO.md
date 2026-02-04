# Guia de Uso Diario - LUMINA

Como usar o sistema LUMINA no dia a dia para gerenciar suas reservas e imoveis.

---

## Indice

1. [Acesso ao Sistema](#acesso-ao-sistema)
2. [Dashboard Principal](#dashboard-principal)
3. [Gerenciar Imoveis](#gerenciar-imoveis)
4. [Gerenciar Reservas](#gerenciar-reservas)
5. [Sincronizacao de Calendarios](#sincronizacao-de-calendarios)
6. [Deteccao de Conflitos](#deteccao-de-conflitos)
7. [Gerar Documentos](#gerar-documentos)
8. [Notificacoes Telegram](#notificacoes-telegram)
9. [Estatisticas e Relatorios](#estatisticas-e-relatorios)
10. [Configuracoes](#configuracoes)

---

## 1. Acesso ao Sistema

### Login
1. Acesse: http://localhost:5173 (desenvolvimento) ou seu dominio em producao
2. Digite seu username ou email
3. Digite sua senha
4. Clique em "Entrar"

### Recuperar Senha
(Feature nao implementada ainda - contate o administrador)

---

## 2. Dashboard Principal

O dashboard mostra uma visao geral do sistema:

### Metricas Principais
- **Total de Reservas**: Quantidade de reservas ativas
- **Ocupacao Atual**: Percentual de imoveis ocupados hoje
- **Receita Mensal**: Total de receita do mes atual
- **Proximos Check-ins**: Reservas com check-in nos proximos 7 dias

### Calendario Visual
- Visualize todas as reservas em um calendario mensal
- Cores diferentes para cada imovel
- Clique em uma reserva para ver detalhes

### Alertas
- Conflitos de reserva detectados
- Sincronizacoes pendentes
- Documentos a gerar

---

## 3. Gerenciar Imoveis

### Adicionar Novo Imovel

1. Va em **Imoveis** > **Novo Imovel**
2. Preencha os campos:
   - **Nome**: Nome do imovel (ex: "Apartamento 2 Quartos - Centro")
   - **Endereco**: Endereco completo
   - **Descricao**: Descricao detalhada
   - **Capacidade**: Numero de hospedes
   - **Quartos**: Numero de quartos
   - **Banheiros**: Numero de banheiros
   - **Preco por Noite**: Valor da diaria
3. Clique em **Salvar**

### Editar Imovel

1. Va em **Imoveis**
2. Clique no imovel que deseja editar
3. Clique em **Editar**
4. Modifique os campos
5. Clique em **Salvar**

### Configurar URLs de Calendario

Para sincronizar com Airbnb/Booking:

1. Edite o imovel
2. Cole as URLs de calendario (iCal):
   - **Airbnb iCal URL**: URL do calendario do Airbnb
   - **Booking.com iCal URL**: URL do calendario do Booking
3. Clique em **Salvar**
4. Clique em **Sincronizar Agora**

### Desativar Imovel

1. Edite o imovel
2. Desmarque "Ativo"
3. Salve

---

## 4. Gerenciar Reservas

### Criar Nova Reserva Manualmente

1. Va em **Reservas** > **Nova Reserva**
2. Selecione o **Imovel**
3. Preencha os dados:
   - **Data de Check-in**
   - **Data de Check-out**
   - **Numero de Hospedes**
   - **Valor Total**
   - **Status**: Confirmada, Pendente, Cancelada
   - **Fonte**: Airbnb, Booking, Direto, Outro
4. Preencha dados do hospede:
   - **Nome Completo**
   - **Email**
   - **Telefone**
   - **CPF** (opcional)
5. Clique em **Salvar**

### Editar Reserva

1. Va em **Reservas**
2. Clique na reserva
3. Clique em **Editar**
4. Modifique os campos
5. Salve

### Cancelar Reserva

1. Edite a reserva
2. Mude o status para "Cancelada"
3. Salve

### Filtrar Reservas

Use os filtros no topo da lista:
- **Por Imovel**: Veja reservas de um imovel especifico
- **Por Status**: Confirmadas, Pendentes, Canceladas
- **Por Data**: Periodo especifico
- **Por Fonte**: Airbnb, Booking, etc

---

## 5. Sincronizacao de Calendarios

### Sincronizacao Automatica

O sistema sincroniza automaticamente a cada hora. Verifique em:
- **Dashboard** > **Ultima Sincronizacao**

### Sincronizacao Manual

1. Va em **Imoveis**
2. Clique no imovel
3. Clique em **Sincronizar Agora**
4. Aguarde a conclusao

### Verificar Logs de Sincronizacao

1. Va em **Sincronizacoes**
2. Veja o historico de sincronizacoes:
   - Data/Hora
   - Imovel
   - Reservas importadas
   - Erros

### Troubleshooting

**Erro: "URL de calendario invalida"**
- Verifique se a URL esta correta
- Teste a URL no navegador - deve baixar um arquivo .ics

**Erro: "Nenhuma reserva encontrada"**
- Verifique se ha reservas no Airbnb/Booking
- URLs podem expirar - gere uma nova no Airbnb/Booking

---

## 6. Deteccao de Conflitos

### O que e um Conflito?

Conflito ocorre quando:
- Duas reservas do mesmo imovel tem datas sobrepostas
- Check-out de uma reserva e no mesmo dia do check-in de outra

### Ver Conflitos

1. Va em **Conflitos**
2. Veja lista de conflitos detectados:
   - Imovel afetado
   - Reservas em conflito
   - Periodo de sobreposicao
   - Severidade

### Resolver Conflitos

**Opcao 1: Ajustar Datas**
1. Clique no conflito
2. Clique em "Editar Reserva"
3. Ajuste as datas
4. Salve

**Opcao 2: Cancelar uma Reserva**
1. Cancele a reserva incorreta
2. Conflito sera automaticamente resolvido

**Opcao 3: Marcar como "Permitido"**
Se o conflito for intencional (ex: mesmo hospede):
1. Clique no conflito
2. Marque "Permitir sobreposicao"

### Notificacoes de Conflito

Configure notificacoes no Telegram para ser alertado imediatamente quando um conflito for detectado.

---

## 7. Gerar Documentos

### Autorizacao de Condominio

1. Va em **Documentos** > **Gerar Autorizacao**
2. Selecione a **Reserva**
3. Verifique os dados pre-preenchidos:
   - Nome do hospede
   - CPF
   - Datas de check-in/out
   - Dados do imovel
4. Clique em **Gerar Documento**
5. Download automatico do arquivo .docx

### Personalizar Template

Templates estao em `templates/`:
- `autorizacao_condominio.docx`

Edite o arquivo .docx com Microsoft Word ou LibreOffice.

Use variaveis:
- `{{ guest_name }}`
- `{{ guest_cpf }}`
- `{{ check_in }}`
- `{{ check_out }}`
- Veja lista completa em [MVP2 Implementacao](../status/MVP2_IMPLEMENTACAO.md)

### Enviar Documento por Email

1. Gere o documento
2. Va em **Emails** > **Enviar Email**
3. Anexe o documento
4. Envie para o hospede ou condominio

---

## 8. Notificacoes Telegram

### Configurar Bot

1. Crie um bot no Telegram via @BotFather
2. Obtenha o token do bot
3. Adicione ao `.env`:
```
TELEGRAM_BOT_TOKEN=seu-token-aqui
```
4. Inicie uma conversa com seu bot
5. Envie `/start`
6. Copie seu chat_id e adicione ao `.env`:
```
TELEGRAM_CHAT_ID=seu-chat-id
```
7. Reinicie o backend

### Comandos Disponiveis

- `/start` - Iniciar bot
- `/status` - Status do sistema
- `/reservas` - Listar proximas reservas
- `/conflitos` - Ver conflitos
- `/sync` - Forcar sincronizacao
- `/stats` - Estatisticas

### Notificacoes Automaticas

O sistema envia automaticamente:
- Nova reserva detectada
- Conflito de reserva
- Check-in hoje
- Check-out hoje
- Erros de sincronizacao

---

## 9. Estatisticas e Relatorios

### Dashboard de Estatisticas

Va em **Estatisticas** para ver:

**Ocupacao**:
- Taxa de ocupacao mensal
- Dias ocupados vs disponiveis
- Grafico de tendencia

**Financeiro**:
- Receita mensal
- Receita por imovel
- Projecao de receita

**Reservas**:
- Total de reservas
- Reservas por fonte (Airbnb, Booking, Direto)
- Duracao media de estadia
- Taxa de cancelamento

**Hospedes**:
- Total de hospedes
- Hospedes recorrentes
- Nacionalidades

### Exportar Relatorios

(Feature em desenvolvimento)

---

## 10. Configuracoes

### Perfil do Usuario

1. Va em **Perfil**
2. Atualize:
   - Nome
   - Email
   - Telefone
3. Salve

### Mudar Senha

1. Va em **Perfil** > **Mudar Senha**
2. Digite a senha atual
3. Digite a nova senha (minimo 8 caracteres)
4. Confirme a nova senha
5. Salve

### Configuracoes do Sistema

**Admin apenas**:

1. Va em **Configuracoes** > **Sistema**
2. Configure:
   - Intervalo de sincronizacao
   - Ativar backups automaticos
   - Configuracoes de email
   - Configuracoes de Telegram
3. Salve

### Usuarios (Admin)

**Criar Novo Usuario**:
1. Va em **Usuarios** > **Novo Usuario**
2. Preencha:
   - Username
   - Email
   - Senha
   - Nivel de acesso (Admin/Usuario)
3. Salve

**Desativar Usuario**:
1. Edite o usuario
2. Desmarque "Ativo"
3. Salve

---

## Dicas e Melhores Praticas

### Sincronizacao
- Sincronize manualmente apos fazer mudancas no Airbnb/Booking
- Verifique conflitos diariamente

### Documentos
- Gere a autorizacao 2-3 dias antes do check-in
- Envie para o condominio com antecedencia

### Backup
- Faca backup semanal do banco de dados
- Guarde backups em local seguro

### Seguranca
- Mude a senha regularmente
- Use senhas fortes
- Nao compartilhe credenciais
- Faca logout em computadores publicos

### Performance
- Limpe reservas antigas periodicamente
- Arquive dados antigos

---

## Problemas Comuns

### "Erro ao conectar com o backend"
- Verifique se o backend esta rodando
- Acesse http://localhost:8000/health

### "Sincronizacao falhando"
- Verifique URLs de calendario
- Teste URLs no navegador
- Veja logs de erro

### "Conflito nao detectado"
- Force sincronizacao manual
- Verifique se as datas estao corretas
- Atualize a pagina

### "Email nao enviado"
- Verifique configuracoes de email no .env
- Use App Password, nao senha normal
- Verifique logs de erro

---

## Suporte

- **Documentacao**: [docs/README.md](../README.md)
- **Issues**: GitHub Issues
- **Email**: suporte@lumina.com

---

**Aproveite o LUMINA para facilitar sua gestao de imoveis!**

**Atualizado**: 2026-02-04
