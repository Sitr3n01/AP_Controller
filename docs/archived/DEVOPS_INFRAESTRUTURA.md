# 🚀 DevOps e Infraestrutura - SENTINEL SaaS

## 📋 VISÃO GERAL

Guia completo para configurar infraestrutura de produção do SENTINEL em ambiente SaaS multi-tenant, com alta disponibilidade, auto-scaling e monitoramento.

**Plataforma recomendada:** DigitalOcean (custo-benefício) ou AWS (enterprise)
**Estimativa de custo inicial:** $200-400/mês para 50-100 tenants

---

## 🏗️ ARQUITETURA DE PRODUÇÃO

### Diagrama de Infraestrutura

```
                                    Internet
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                                     │
              [Cloudflare CDN]                    [DNS + WAF]
              SSL/TLS, DDoS                      Firewall Rules
                    │                                     │
                    └──────────────┬──────────────────────┘
                                   │
                            [Load Balancer]
                          HAProxy / Nginx
                         Health Checks
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
           [App Server 1]    [App Server 2]    [App Server 3]
           FastAPI + Uvicorn FastAPI + Uvicorn FastAPI + Uvicorn
           Docker Container  Docker Container  Docker Container
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
            [PostgreSQL Primary]  [Redis Cache]  [S3-compatible]
            Multi-tenant DBs      Session Store  File Storage
                    │
            [PostgreSQL Replica]
            Read-only Failover
                    │
              [Backup Storage]
           Automated Daily Backups
```

### Componentes da Infraestrutura

1. **Frontend (React SPA)**
   - CDN: Cloudflare / Vercel
   - Build otimizado (Vite)
   - Cache agressivo de assets

2. **Backend (FastAPI)**
   - 3+ app servers (auto-scaling)
   - Docker containers
   - Horizontal scaling automático

3. **Database (PostgreSQL)**
   - Primary + Replica (HA)
   - Database-per-tenant
   - Managed service (DigitalOcean Managed DB)

4. **Cache (Redis)**
   - Session management
   - API response caching
   - Rate limiting

5. **Storage (S3)**
   - Uploads de usuários
   - Backups automáticos
   - Logs arquivados

6. **Monitoring**
   - Prometheus + Grafana
   - ELK Stack (logs)
   - Uptime monitoring

---

## 🐳 DOCKER E CONTAINERIZAÇÃO

### Dockerfile (Backend)

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Metadata
LABEL maintainer="sentinel@example.com"
LABEL version="1.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Criar usuário não-root
RUN groupadd -r sentinel && useradd -r -g sentinel sentinel

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/

# Criar diretórios necessários
RUN mkdir -p /app/data/logs && \
    chown -R sentinel:sentinel /app

# Trocar para usuário não-root
USER sentinel

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### docker-compose.yml (Desenvolvimento)

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Backend FastAPI
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: sentinel-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://sentinel:sentinel123@postgres:5432/sentinel_control
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=development
      - DEBUG=true
    volumes:
      - ./app:/app/app  # Hot reload
      - ./data:/app/data
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - sentinel-network
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: sentinel-postgres
    environment:
      - POSTGRES_USER=sentinel
      - POSTGRES_PASSWORD=sentinel123
      - POSTGRES_DB=sentinel_control
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sentinel"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - sentinel-network
    restart: unless-stopped

  # Redis
  redis:
    image: redis:7-alpine
    container_name: sentinel-redis
    command: redis-server --requirepass redis123 --maxmemory 256mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - sentinel-network
    restart: unless-stopped

  # Frontend (opcional - para dev)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: sentinel-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
    environment:
      - VITE_API_URL=http://localhost:8000
    networks:
      - sentinel-network
    restart: unless-stopped

  # Nginx (Load Balancer / Reverse Proxy)
  nginx:
    image: nginx:alpine
    container_name: sentinel-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - backend
    networks:
      - sentinel-network
    restart: unless-stopped

networks:
  sentinel-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

### Nginx Configuration

```nginx
# nginx/nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/x-javascript;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;

    # Backend upstream
    upstream backend {
        least_conn;  # Load balancing method
        server backend:8000 max_fails=3 fail_timeout=30s;
        # Adicionar mais servers para scaling:
        # server backend-2:8000 max_fails=3 fail_timeout=30s;
        # server backend-3:8000 max_fails=3 fail_timeout=30s;
    }

    # HTTP → HTTPS redirect
    server {
        listen 80;
        server_name sentinel.example.com;

        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name sentinel.example.com;

        # SSL certificates
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;

        # Frontend (React SPA)
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;

            # Cache assets
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }
        }

        # Backend API
        location /api {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;

            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Auth endpoints (stricter rate limit)
        location /api/auth {
            limit_req zone=auth_limit burst=5 nodelay;

            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Healthcheck
        location /health {
            proxy_pass http://backend/health;
            access_log off;
        }

        # Docs (opcional - proteger em prod)
        location /docs {
            proxy_pass http://backend/docs;
        }
    }
}
```

---

## ☁️ DEPLOY EM DIGITALOCEAN

### Opção 1: App Platform (PaaS - Mais Fácil)

**Vantagens:**
- Deploy automático via Git
- Auto-scaling embutido
- Zero configuração de servidor
- SSL gratuito

**Custo estimado:**
- Backend: $12/mês (Basic) → $24/mês (Professional)
- PostgreSQL Managed: $15/mês (1GB RAM) → $55/mês (4GB RAM)
- Redis Managed: $15/mês
- **Total:** ~$42-94/mês

**Setup:**

1. **Criar App no DigitalOcean App Platform**
```bash
# Instalar doctl CLI
brew install doctl  # macOS
# ou: https://github.com/digitalocean/doctl/releases

# Autenticar
doctl auth init

# Criar app (via app.yaml)
doctl apps create --spec app.yaml
```

2. **app.yaml**
```yaml
name: sentinel-saas
region: nyc

# Database
databases:
  - name: sentinel-postgres
    engine: PG
    version: "15"
    size: db-s-1vcpu-1gb
    num_nodes: 1

# Redis
  - name: sentinel-redis
    engine: REDIS
    version: "7"
    size: db-s-1vcpu-1gb

# Backend
services:
  - name: backend
    github:
      repo: seu-usuario/sentinel-apartment-manager
      branch: main
      deploy_on_push: true
    source_dir: /
    dockerfile_path: Dockerfile
    http_port: 8000
    instance_count: 2
    instance_size_slug: basic-xs  # $12/mês
    routes:
      - path: /api
    health_check:
      http_path: /health
      initial_delay_seconds: 30
      period_seconds: 10
      timeout_seconds: 5
      success_threshold: 1
      failure_threshold: 3
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${sentinel-postgres.DATABASE_URL}
      - key: REDIS_URL
        scope: RUN_TIME
        value: ${sentinel-redis.DATABASE_URL}
      - key: SECRET_KEY
        scope: RUN_TIME
        type: SECRET
        value: "seu-secret-key-aqui"
      - key: ENVIRONMENT
        value: production

# Frontend
  - name: frontend
    github:
      repo: seu-usuario/sentinel-apartment-manager
      branch: main
    source_dir: /frontend
    build_command: npm run build
    output_dir: dist
    routes:
      - path: /
    envs:
      - key: VITE_API_URL
        value: ${backend.PUBLIC_URL}
```

3. **Deploy**
```bash
# Aplicar configuração
doctl apps create --spec app.yaml

# Ver status
doctl apps list

# Ver logs
doctl apps logs <APP_ID> --type RUN
```

---

### Opção 2: Droplets (VPS - Mais Controle)

**Vantagens:**
- Controle total
- Custo menor em escala
- Customização ilimitada

**Custo estimado:**
- Droplet (4GB RAM, 2 vCPU): $24/mês
- Managed PostgreSQL: $55/mês
- Load Balancer: $12/mês
- **Total:** ~$91/mês

**Setup:**

1. **Criar Droplet**
```bash
# Via CLI
doctl compute droplet create sentinel-prod \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys <YOUR_SSH_KEY_ID>

# Obter IP
doctl compute droplet list
```

2. **Configurar Servidor (SSH)**
```bash
ssh root@<DROPLET_IP>

# Atualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com | sh
systemctl start docker
systemctl enable docker

# Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Criar usuário para app
adduser --disabled-password sentinel
usermod -aG docker sentinel

# Configurar firewall
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

3. **Deploy da Aplicação**
```bash
su - sentinel

# Clonar repositório
git clone https://github.com/seu-usuario/sentinel-apartment-manager.git
cd sentinel-apartment-manager

# Configurar .env
cp .env.example .env
nano .env  # Editar com credenciais de produção

# Build e start
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose logs -f
```

4. **docker-compose.prod.yml**
```yaml
version: '3.8'

services:
  backend:
    build: .
    restart: always
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=production
      - DEBUG=false
    depends_on:
      - redis
    networks:
      - sentinel-network
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - sentinel-network

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/nginx/ssl:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - backend
    networks:
      - sentinel-network

networks:
  sentinel-network:

volumes:
  redis-data:
```

5. **Configurar SSL (Let's Encrypt)**
```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx

# Obter certificado
certbot --nginx -d sentinel.example.com

# Renovação automática (crontab)
crontab -e
# Adicionar:
0 0 * * * certbot renew --quiet
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest tests/ --cov=app

      - name: Lint
        run: |
          pip install flake8 black
          flake8 app/
          black --check app/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: seuusuario/sentinel-backend:latest,seuusuario/sentinel-backend:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to DigitalOcean
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.DROPLET_IP }}
          username: sentinel
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd ~/sentinel-apartment-manager
            git pull origin main
            docker-compose pull
            docker-compose up -d --force-recreate
            docker image prune -f
```

---

## 📊 MONITORAMENTO E OBSERVABILIDADE

### Prometheus + Grafana

**docker-compose.monitoring.yml**
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: sentinel-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - sentinel-network
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: sentinel-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./monitoring/grafana-dashboards:/etc/grafana/provisioning/dashboards
    networks:
      - sentinel-network
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    container_name: sentinel-node-exporter
    ports:
      - "9100:9100"
    networks:
      - sentinel-network
    restart: unless-stopped

networks:
  sentinel-network:
    external: true

volumes:
  prometheus-data:
  grafana-data:
```

**prometheus.yml**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Backend FastAPI
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']

  # Node Exporter (métricas do servidor)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # PostgreSQL Exporter
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  # Redis Exporter
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Instrumentar FastAPI com Prometheus

```python
# app/middleware/metrics.py
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
import time

# Métricas
http_requests_total = Counter(
    'http_requests_total',
    'Total de requests HTTP',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'Duração dos requests HTTP',
    ['method', 'endpoint']
)

tenant_requests_total = Counter(
    'tenant_requests_total',
    'Requests por tenant',
    ['tenant_id']
)

async def metrics_middleware(request: Request, call_next):
    """Middleware para coletar métricas"""
    start_time = time.time()

    response = await call_next(request)

    # Duração
    duration = time.time() - start_time

    # Labels
    method = request.method
    endpoint = request.url.path
    status = response.status_code

    # Registrar métricas
    http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
    http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)

    # Métrica por tenant
    if hasattr(request.state, 'tenant_id'):
        tenant_requests_total.labels(tenant_id=request.state.tenant_id).inc()

    return response


# Endpoint de métricas
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

---

## 🔐 BACKUP AUTOMATIZADO

```bash
#!/bin/bash
# scripts/backup-databases.sh

DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="/backups"
S3_BUCKET="s3://sentinel-backups"

# Backup do sentinel_control
pg_dump -h localhost -U sentinel sentinel_control | gzip > "$BACKUP_DIR/control_$DATE.sql.gz"

# Backup de todos os tenants
psql -h localhost -U sentinel -d sentinel_control -t -c "SELECT database_name FROM tenants WHERE status = 'active'" | while read DB; do
    if [ -n "$DB" ]; then
        pg_dump -h localhost -U sentinel "$DB" | gzip > "$BACKUP_DIR/${DB}_$DATE.sql.gz"
    fi
done

# Upload para S3
aws s3 sync "$BACKUP_DIR" "$S3_BUCKET" --storage-class STANDARD_IA

# Limpar backups locais antigos (>7 dias)
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete

echo "✅ Backup concluído: $DATE"
```

**Agendar com cron:**
```bash
# Backup diário às 2h da manhã
0 2 * * * /scripts/backup-databases.sh >> /var/log/sentinel-backup.log 2>&1
```

---

## 📈 AUTO-SCALING

### Horizontal Pod Autoscaler (Kubernetes)

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sentinel-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sentinel-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

---

## ✅ CHECKLIST DE DEPLOY

### Pré-Deploy
- [ ] Testes passando (pytest)
- [ ] Linting OK (flake8, black)
- [ ] Secrets configurados no GitHub
- [ ] SSL certificate válido
- [ ] Backup do banco atual
- [ ] Rollback plan documentado

### Deploy
- [ ] Build Docker image
- [ ] Push para registry
- [ ] Deploy em staging primeiro
- [ ] Smoke tests em staging
- [ ] Deploy em produção
- [ ] Verificar healthchecks
- [ ] Verificar logs

### Pós-Deploy
- [ ] Testar login
- [ ] Testar criação de tenant
- [ ] Verificar métricas no Grafana
- [ ] Configurar alertas
- [ ] Atualizar documentação
- [ ] Notificar equipe

---

## 🚨 TROUBLESHOOTING

### App não inicia
```bash
# Ver logs
docker-compose logs -f backend

# Verificar healthcheck
curl http://localhost:8000/health

# Verificar banco de dados
docker-compose exec postgres psql -U sentinel -d sentinel_control -c "\dt"
```

### Performance ruim
```bash
# Ver uso de recursos
docker stats

# Ver queries lentas no PostgreSQL
docker-compose exec postgres psql -U sentinel -d sentinel_control -c "SELECT * FROM pg_stat_activity WHERE state != 'idle';"
```

### Erro 502 Bad Gateway
- Verificar se backend está rodando
- Verificar configuração do Nginx
- Verificar logs: `docker-compose logs nginx`

---

## 💰 ESTIMATIVA DE CUSTOS

### Starter (0-50 tenants)
- DigitalOcean Droplet (4GB): $24/mês
- Managed PostgreSQL (2GB): $30/mês
- Redis Managed: $15/mês
- Backups (100GB): $5/mês
- **Total: ~$74/mês**

### Growth (50-200 tenants)
- App Platform Professional: $48/mês
- Managed PostgreSQL (4GB): $55/mês
- Redis Managed (1GB): $15/mês
- Load Balancer: $12/mês
- Backups (500GB): $25/mês
- **Total: ~$155/mês**

### Scale (200-1000 tenants)
- Kubernetes Cluster: $100/mês
- Managed PostgreSQL (8GB): $120/mês
- Redis Cluster: $60/mês
- Load Balancers (2x): $24/mês
- Backups (2TB): $100/mês
- Monitoring: $30/mês
- **Total: ~$434/mês**

---

**Próximo passo:** Implementar sistema de billing com Stripe para cobranças automáticas.
