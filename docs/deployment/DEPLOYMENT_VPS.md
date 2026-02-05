# 🚀 SENTINEL - Guia Completo de Deployment em VPS

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Preparação do Servidor](#preparação-do-servidor)
3. [Deployment Automático](#deployment-automático)
4. [Deployment Manual](#deployment-manual)
5. [Configuração SSL/HTTPS](#configuração-sslhttps)
6. [Monitoramento e Logs](#monitoramento-e-logs)
7. [Backup e Restore](#backup-e-restore)
8. [Troubleshooting](#troubleshooting)
9. [Manutenção](#manutenção)

---

## 🔧 Pré-requisitos

### Servidor VPS

- **Sistema Operacional**: Ubuntu 22.04 LTS ou Debian 12+ (recomendado)
- **Memória RAM**: Mínimo 2GB (recomendado 4GB)
- **Disco**: Mínimo 20GB SSD
- **CPU**: 1 vCore mínimo (2+ recomendado)
- **Acesso**: SSH com root ou sudo

### Domínio

- Domínio registrado apontando para o IP do VPS
- DNS configurado (registros A/AAAA)

### Conhecimentos Básicos

- Linux command line
- SSH
- Conceitos de web servers e reverse proxy

---

## 🖥️ Preparação do Servidor

### 1. Atualizar Sistema

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Criar Usuário Não-Root

```bash
# Criar usuário
sudo adduser sentinel

# Adicionar ao grupo sudo
sudo usermod -aG sudo sentinel

# Trocar para o novo usuário
su - sentinel
```

### 3. Configurar SSH (Opcional mas Recomendado)

```bash
# Gerar chave SSH no seu computador local
ssh-keygen -t ed25519 -C "seu-email@example.com"

# Copiar chave pública para o servidor
ssh-copy-id sentinel@seu-servidor.com

# No servidor, desabilitar login com senha (opcional)
sudo nano /etc/ssh/sshd_config
# Alterar: PasswordAuthentication no
sudo systemctl restart sshd
```

---

## ⚡ Deployment Automático

### Script de Deployment Completo

O script `deploy_vps.sh` automatiza todo o processo de deployment:

```bash
# No servidor, como root ou com sudo
wget https://raw.githubusercontent.com/SEU_USUARIO/AP_Controller/main/deployment/scripts/deploy_vps.sh
chmod +x deploy_vps.sh
sudo ./deploy_vps.sh
```

**O script irá:**

1. ✅ Atualizar o sistema
2. ✅ Instalar todas as dependências
3. ✅ Criar usuário `sentinel`
4. ✅ Clonar o repositório
5. ✅ Configurar Python virtual environment
6. ✅ Gerar SECRET_KEY segura
7. ✅ Inicializar banco de dados
8. ✅ Criar usuário admin
9. ✅ Configurar systemd service
10. ✅ Configurar nginx
11. ✅ Configurar fail2ban
12. ✅ Configurar firewall (UFW)

### Após o Script

```bash
# 1. Editar configurações
sudo nano /opt/sentinel/.env

# 2. Editar nginx com seu domínio
sudo nano /etc/nginx/nginx.conf
# Substitua "server_name _;" por "server_name seu-dominio.com;"

# 3. Configurar SSL
cd /opt/sentinel/deployment/scripts
chmod +x setup_ssl.sh
sudo ./setup_ssl.sh seu-dominio.com seu-email@example.com

# 4. Reiniciar serviços
sudo systemctl restart sentinel
sudo systemctl restart nginx

# 5. Verificar status
sudo systemctl status sentinel
```

---

## 🔨 Deployment Manual

### 1. Instalar Dependências

```bash
sudo apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    nginx \
    git \
    fail2ban \
    ufw \
    certbot \
    python3-certbot-nginx
```

### 2. Clonar Repositório

```bash
sudo mkdir -p /opt/sentinel
sudo chown sentinel:sentinel /opt/sentinel
cd /opt/sentinel
git clone https://github.com/SEU_USUARIO/AP_Controller.git .
```

### 3. Configurar Python Environment

```bash
cd /opt/sentinel
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
cp .env.example .env  # Se existir, senão criar novo
nano .env
```

**Conteúdo mínimo do `.env`:**

```env
# Ambiente
APP_ENV=production
SECRET_KEY=GERE_UMA_CHAVE_FORTE_AQUI
LOG_LEVEL=INFO

# Banco de Dados
DATABASE_URL=sqlite:///./data/sentinel.db

# CORS (substitua pelo seu domínio)
CORS_ORIGINS=https://seu-dominio.com

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60

# Calendários (configure conforme necessário)
AIRBNB_ICAL_URL=
BOOKING_ICAL_URL=
CALENDAR_SYNC_INTERVAL_MINUTES=30

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_ADMIN_USER_IDS=
```

**Gerar SECRET_KEY segura:**

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Inicializar Banco de Dados

```bash
source venv/bin/activate
python -c "from app.database.session import create_all_tables; create_all_tables()"
python scripts/create_default_admin.py
```

### 6. Configurar Systemd Service

```bash
sudo cp deployment/systemd/sentinel.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sentinel
sudo systemctl start sentinel
sudo systemctl status sentinel
```

### 7. Configurar Nginx

```bash
sudo cp deployment/nginx/nginx.conf /etc/nginx/nginx.conf

# Editar com seu domínio
sudo nano /etc/nginx/nginx.conf
# Substitua "server_name _;" por "server_name seu-dominio.com;"

# Testar configuração
sudo nginx -t

# Iniciar nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### 8. Configurar Firewall

```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
sudo ufw status
```

### 9. Configurar Fail2ban

```bash
sudo cp deployment/fail2ban/sentinel.conf /etc/fail2ban/filter.d/
sudo cp deployment/fail2ban/jail.local /etc/fail2ban/jail.d/sentinel.local
sudo systemctl enable fail2ban
sudo systemctl restart fail2ban
```

---

## 🔒 Configuração SSL/HTTPS

### Método 1: Script Automático (Recomendado)

```bash
cd /opt/sentinel/deployment/scripts
chmod +x setup_ssl.sh
sudo ./setup_ssl.sh seu-dominio.com seu-email@example.com
```

### Método 2: Manual com Certbot

```bash
# Obter certificado
sudo certbot certonly \
    --nginx \
    -d seu-dominio.com \
    --email seu-email@example.com \
    --agree-tos \
    --no-eff-email

# Certificados serão salvos em:
# /etc/letsencrypt/live/seu-dominio.com/

# Testar renovação automática
sudo certbot renew --dry-run
```

### Renovação Automática

Certbot configura automaticamente um timer systemd:

```bash
# Verificar timer
sudo systemctl status certbot.timer

# Verificar próxima execução
sudo systemctl list-timers | grep certbot
```

---

## 📊 Monitoramento e Logs

### Health Checks

```bash
# Verificar se API está respondendo
curl http://localhost:8000/api/v1/health/
curl http://localhost:8000/api/v1/health/ready
curl http://localhost:8000/api/v1/health/live

# Métricas do sistema
curl http://localhost:8000/api/v1/health/metrics
```

### Logs da Aplicação

```bash
# Ver logs em tempo real
sudo journalctl -u sentinel -f

# Últimas 100 linhas
sudo journalctl -u sentinel -n 100

# Logs de hoje
sudo journalctl -u sentinel --since today

# Logs com filtro de erro
sudo journalctl -u sentinel -p err
```

### Logs do Nginx

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### Logs do Fail2ban

```bash
# Status geral
sudo fail2ban-client status

# Status do jail sentinel
sudo fail2ban-client status sentinel-auth

# Ver IPs banidos
sudo fail2ban-client get sentinel-auth banip
```

### Monitoramento de Recursos

```bash
# CPU e memória
htop

# Uso de disco
df -h

# Processos da aplicação
ps aux | grep uvicorn

# Conexões de rede
sudo netstat -tulpn | grep 8000
```

---

## 💾 Backup e Restore

### Backup Manual

```bash
# Via Python
cd /opt/sentinel
source venv/bin/activate
python -c "from app.core.backup import create_manual_backup; create_manual_backup('daily')"
```

### Backups Automáticos

O sistema executa backups automáticos:

- **Diários**: 3h da manhã (mantém 7 backups)
- **Semanais**: Domingos às 3h (mantém 4 backups)
- **Mensais**: Dia 1 do mês às 3h (mantém 6 backups)

**Localização dos backups:**

```
/opt/sentinel/data/backups/
├── daily/
├── weekly/
└── monthly/
```

### Listar Backups

```bash
cd /opt/sentinel
source venv/bin/activate
python -c "
from app.core.backup import BackupManager
bm = BackupManager()
for b in bm.list_backups():
    print(f\"{b['type']:10} {b['filename']:50} {b['size_mb']:6.2f}MB {b['created_at']}\")
"
```

### Restaurar Backup

```bash
cd /opt/sentinel
source venv/bin/activate

# Parar aplicação
sudo systemctl stop sentinel

# Restaurar
python -c "
from app.core.backup import BackupManager
from pathlib import Path
bm = BackupManager()
backup_file = Path('data/backups/daily/NOME_DO_BACKUP.db.gz')
bm.restore_backup(backup_file)
"

# Reiniciar aplicação
sudo systemctl start sentinel
```

### Backup Completo do Servidor

```bash
# Criar backup de tudo (exceto venv)
cd /opt
sudo tar -czf sentinel-backup-$(date +%Y%m%d).tar.gz \
    --exclude='sentinel/venv' \
    --exclude='sentinel/__pycache__' \
    sentinel/

# Baixar para seu computador
scp sentinel@servidor:/opt/sentinel-backup-*.tar.gz ./
```

---

## 🔧 Troubleshooting

### Aplicação Não Inicia

```bash
# Verificar logs
sudo journalctl -u sentinel -n 50

# Verificar se porta está em uso
sudo lsof -i :8000

# Testar manualmente
cd /opt/sentinel
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Erro de Permissões

```bash
# Corrigir ownership
sudo chown -R sentinel:sentinel /opt/sentinel
sudo chmod 600 /opt/sentinel/.env
```

### Banco de Dados Corrompido

```bash
# Restaurar do backup mais recente
cd /opt/sentinel
sudo systemctl stop sentinel
source venv/bin/activate

python -c "
from app.core.backup import BackupManager
from pathlib import Path
bm = BackupManager()
backups = bm.list_backups('daily')
if backups:
    latest = Path(backups[0]['path'])
    bm.restore_backup(latest)
    print(f'Restored from {latest}')
"

sudo systemctl start sentinel
```

### SSL/HTTPS Não Funciona

```bash
# Verificar certificados
sudo certbot certificates

# Testar nginx config
sudo nginx -t

# Renovar certificado
sudo certbot renew --force-renewal

# Verificar logs do certbot
sudo journalctl -u certbot -n 50
```

### Alta Carga de CPU/Memória

```bash
# Ver processos
top -u sentinel

# Ajustar workers do uvicorn
sudo nano /etc/systemd/system/sentinel.service
# Reduzir --workers de 4 para 2

sudo systemctl daemon-reload
sudo systemctl restart sentinel
```

### IPs Banidos por Engano

```bash
# Ver IPs banidos
sudo fail2ban-client get sentinel-auth banip

# Desbanir IP específico
sudo fail2ban-client set sentinel-auth unbanip 192.168.1.100

# Desabilitar jail temporariamente
sudo fail2ban-client stop sentinel-auth
```

---

## 🔄 Manutenção

### Atualizar Aplicação

```bash
cd /opt/sentinel
sudo systemctl stop sentinel

# Backup antes de atualizar
source venv/bin/activate
python -c "from app.core.backup import create_manual_backup; create_manual_backup('daily')"

# Atualizar código
git pull origin main

# Atualizar dependências
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Migrar banco se necessário
# python scripts/migrate_db.py

# Reiniciar
sudo systemctl start sentinel
sudo systemctl status sentinel
```

### Limpar Logs Antigos

```bash
# Limpar logs do journald (manter últimos 7 dias)
sudo journalctl --vacuum-time=7d

# Limpar logs do nginx
sudo find /var/log/nginx -name "*.log" -mtime +30 -delete

# Limpar backups antigos (90+ dias)
cd /opt/sentinel
source venv/bin/activate
python -c "from app.core.backup import BackupManager; bm = BackupManager(); print(f'Removed {bm.cleanup_old_backups(90)} old backups')"
```

### Rotação de SECRET_KEY

```bash
# Gerar nova chave
NEW_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Atualizar .env
sudo nano /opt/sentinel/.env
# Substitua SECRET_KEY com o novo valor

# Reiniciar
sudo systemctl restart sentinel

# NOTA: Todos os tokens JWT existentes serão invalidados
# Usuários precisarão fazer login novamente
```

### Monitoramento de Espaço em Disco

```bash
# Verificar uso
df -h

# Encontrar diretórios grandes
du -h /opt/sentinel | sort -h | tail -20

# Limpar cache do pip
rm -rf ~/.cache/pip

# Limpar __pycache__
find /opt/sentinel -type d -name __pycache__ -exec rm -rf {} +
```

---

## 📈 Melhorias Futuras Recomendadas

### 1. PostgreSQL ao Invés de SQLite

Para produção com múltiplos workers e alta carga:

```bash
sudo apt-get install postgresql postgresql-contrib
# Configurar PostgreSQL e atualizar DATABASE_URL
```

### 2. Redis para Cache

```bash
sudo apt-get install redis-server
# Implementar cache de sessões e rate limiting
```

### 3. Docker Deployment

```bash
# Usar docker-compose.yml fornecido
docker-compose up -d
```

### 4. Monitoramento Avançado

- **Grafana + Prometheus**: Métricas detalhadas
- **Sentry**: Tracking de erros
- **Uptime Robot**: Monitoramento de disponibilidade

### 5. CDN e Load Balancer

Para escalar horizontalmente:

- Cloudflare (CDN + DDoS protection)
- AWS ELB ou DigitalOcean Load Balancer

---

## 📞 Suporte

### Verificação de Status Completo

```bash
#!/bin/bash
echo "=== SENTINEL Status Check ==="
echo ""
echo "Application Service:"
sudo systemctl status sentinel --no-pager | head -5
echo ""
echo "Nginx Status:"
sudo systemctl status nginx --no-pager | head -3
echo ""
echo "Fail2ban Status:"
sudo fail2ban-client status sentinel-auth
echo ""
echo "Disk Usage:"
df -h / | tail -1
echo ""
echo "Last 5 Application Logs:"
sudo journalctl -u sentinel -n 5 --no-pager
```

### Informações do Sistema

```bash
# Criar script de diagnóstico
curl http://localhost:8000/api/v1/health/metrics | jq
curl http://localhost:8000/api/v1/health/ready | jq
```

---

## ✅ Checklist Pós-Deployment

- [ ] Aplicação respondendo em HTTPS
- [ ] Certificado SSL válido
- [ ] Firewall configurado (apenas portas 22, 80, 443)
- [ ] Fail2ban ativo e funcionando
- [ ] Backups automáticos configurados
- [ ] Logs sendo gravados corretamente
- [ ] Health checks respondendo
- [ ] Senha do admin alterada
- [ ] SECRET_KEY única gerada
- [ ] Domínio apontando corretamente
- [ ] Emails de monitoramento configurados (se aplicável)

---

**🎉 Parabéns! Seu SENTINEL está em produção!**

Para dúvidas ou problemas, consulte os logs e a seção de troubleshooting.
