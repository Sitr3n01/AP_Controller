# 💳 Integração Stripe - Sistema de Billing

## 📋 VISÃO GERAL

Guia completo para implementar sistema de pagamentos recorrentes (billing) no SENTINEL usando Stripe, permitindo cobranças automáticas, gerenciamento de assinaturas e compliance com regulamentações financeiras.

**Tempo de implementação:** 2-3 dias
**Complexidade:** Média
**Investimento:** Grátis (taxas apenas sobre transações: 4.99% + R$0,59)

---

## 🎯 FUNCIONALIDADES

### O que será implementado:
- ✅ Criação de assinaturas recorrentes (mensal/anual)
- ✅ Cobranças automáticas via cartão de crédito
- ✅ Gerenciamento de planos (Starter, Professional, Enterprise)
- ✅ Período de trial (14 dias gratuitos)
- ✅ Upgrades e downgrades de planos
- ✅ Cancelamento de assinaturas
- ✅ Webhooks para sincronização de status
- ✅ Portal do cliente (atualizar cartão, ver faturas)
- ✅ Compliance com regulamentações (PCI-DSS)

---

## 🔧 SETUP INICIAL

### 1. Criar Conta no Stripe

1. Acesse: https://dashboard.stripe.com/register
2. Preencha dados da empresa
3. Complete verificação (KYC)
4. Ative conta no Brasil

### 2. Obter API Keys

```bash
# No Dashboard do Stripe:
# Developers → API keys

# Modo de teste (desenvolvimento)
STRIPE_PUBLISHABLE_KEY_TEST=pk_test_XXXXXXXXXXXXXXXX
STRIPE_SECRET_KEY_TEST=sk_test_XXXXXXXXXXXXXXXX

# Modo live (produção)
STRIPE_PUBLISHABLE_KEY_LIVE=pk_live_XXXXXXXXXXXXXXXX
STRIPE_SECRET_KEY_LIVE=sk_live_XXXXXXXXXXXXXXXX
```

### 3. Instalar SDK

```bash
pip install stripe
```

**requirements.txt**
```txt
stripe>=7.0.0
```

---

## 🏗️ ARQUITETURA DE BILLING

### Fluxo de Assinatura

```
1. Usuário escolhe plano
   → Starter ($49/mês)

2. Checkout do Stripe
   → Insere dados do cartão (PCI-compliant)

3. Stripe processa pagamento
   → Cria subscription

4. Webhook notifica backend
   → Atualiza status do tenant

5. Acesso liberado
   → Tenant status = 'active'

6. Cobranças recorrentes
   → Stripe cobra automaticamente todo mês

7. Falha de pagamento?
   → Webhook notifica → Suspende acesso → Email para usuário
```

### Entidades do Stripe

```
Stripe Customer (Cliente)
├── email: admin@empresa.com
├── metadata: {tenant_id: "abc123"}
└── Subscriptions (Assinaturas)
    ├── Subscription 1
    │   ├── status: active
    │   ├── plan: Starter
    │   ├── price: $49/month
    │   └── current_period_end: 2024-03-15
    └── Payment Methods (Cartões)
        └── Card ending in 4242
```

---

## 💻 IMPLEMENTAÇÃO

### PASSO 1: Configurar Produtos no Stripe

**Via Dashboard:**
1. Products → Create product
2. Criar 3 produtos:

```
Produto 1: SENTINEL Starter
- Preço: R$ 49,00 / mês
- ID do preço: price_starter_monthly

Produto 2: SENTINEL Professional
- Preço: R$ 149,00 / mês
- ID do preço: price_professional_monthly

Produto 3: SENTINEL Enterprise
- Preço: Negociado (custom)
- ID do preço: price_enterprise_monthly
```

**Via API (automático):**
```python
# scripts/setup_stripe_products.py
import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Criar produtos
products = [
    {
        'name': 'SENTINEL Starter',
        'description': 'Plano ideal para proprietários com 1-5 propriedades',
        'metadata': {'plan_code': 'starter'},
        'prices': [
            {'amount': 4900, 'currency': 'brl', 'interval': 'month'},
            {'amount': 470, 'currency': 'brl', 'interval': 'year'},  # 20% desconto
        ]
    },
    {
        'name': 'SENTINEL Professional',
        'description': 'Para gestores profissionais com 6-30 propriedades',
        'metadata': {'plan_code': 'professional'},
        'prices': [
            {'amount': 14900, 'currency': 'brl', 'interval': 'month'},
            {'amount': 1430, 'currency': 'brl', 'interval': 'year'},
        ]
    },
]

for product_data in products:
    # Criar produto
    product = stripe.Product.create(
        name=product_data['name'],
        description=product_data['description'],
        metadata=product_data['metadata'],
    )

    # Criar preços
    for price_data in product_data['prices']:
        price = stripe.Price.create(
            product=product.id,
            unit_amount=price_data['amount'],  # em centavos
            currency=price_data['currency'],
            recurring={'interval': price_data['interval']},
        )

        print(f"✅ Criado: {product.name} - {price.id}")
```

---

### PASSO 2: Models de Billing

```python
# app/models/billing.py
from sqlalchemy import Column, String, DateTime, Numeric, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base

class StripeCustomer(Base):
    """
    Relaciona tenant com Stripe Customer.
    """
    __tablename__ = "stripe_customers"
    __table_args__ = {'schema': 'public'}  # sentinel_control

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), unique=True, nullable=False)

    stripe_customer_id = Column(String(255), unique=True, nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StripeSubscription(Base):
    """
    Armazena dados da subscription do Stripe.
    """
    __tablename__ = "stripe_subscriptions"
    __table_args__ = {'schema': 'public'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)

    stripe_subscription_id = Column(String(255), unique=True, nullable=False, index=True)
    stripe_customer_id = Column(String(255), nullable=False)
    stripe_price_id = Column(String(255), nullable=False)

    status = Column(String(50), nullable=False)  # active, canceled, past_due, etc.
    plan = Column(String(50), nullable=False)  # starter, professional, enterprise

    current_period_start = Column(DateTime, nullable=False)
    current_period_end = Column(DateTime, nullable=False)

    cancel_at_period_end = Column(Boolean, default=False)
    canceled_at = Column(DateTime, nullable=True)

    trial_start = Column(DateTime, nullable=True)
    trial_end = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Invoice(Base):
    """
    Histórico de faturas.
    """
    __tablename__ = "invoices"
    __table_args__ = {'schema': 'public'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False)

    stripe_invoice_id = Column(String(255), unique=True, nullable=False, index=True)

    amount_due = Column(Numeric(10, 2), nullable=False)
    amount_paid = Column(Numeric(10, 2), default=0)

    status = Column(String(50), nullable=False)  # draft, open, paid, void, uncollectible

    invoice_pdf = Column(String(500), nullable=True)  # URL do PDF

    period_start = Column(DateTime)
    period_end = Column(DateTime)

    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

### PASSO 3: Stripe Service

```python
# app/services/stripe_service.py
import stripe
from sqlalchemy.orm import Session
from typing import Optional, Dict
from datetime import datetime

from app.core.config import settings
from app.models.tenant import Tenant
from app.models.billing import StripeCustomer, StripeSubscription, Invoice

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    """
    Serviço para gerenciar integrações com Stripe.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, tenant: Tenant, email: str) -> str:
        """
        Cria Stripe Customer para o tenant.

        Returns:
            stripe_customer_id
        """
        # Verificar se já existe
        existing = self.db.query(StripeCustomer).filter(
            StripeCustomer.tenant_id == tenant.id
        ).first()

        if existing:
            return existing.stripe_customer_id

        # Criar no Stripe
        stripe_customer = stripe.Customer.create(
            email=email,
            name=tenant.company_name,
            metadata={
                'tenant_id': str(tenant.id),
                'tenant_slug': tenant.slug,
            }
        )

        # Salvar no banco
        customer = StripeCustomer(
            tenant_id=tenant.id,
            stripe_customer_id=stripe_customer.id,
        )
        self.db.add(customer)
        self.db.commit()

        return stripe_customer.id

    def create_checkout_session(
        self,
        tenant: Tenant,
        price_id: str,
        success_url: str,
        cancel_url: str,
        trial_days: int = 14
    ) -> Dict:
        """
        Cria Checkout Session para assinatura.

        Returns:
            {
                'session_id': 'cs_XXX',
                'url': 'https://checkout.stripe.com/...'
            }
        """
        # Obter/criar customer
        customer_id = self.create_customer(tenant, tenant.users[0].email)

        # Criar Checkout Session
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            subscription_data={
                'trial_period_days': trial_days,
                'metadata': {
                    'tenant_id': str(tenant.id),
                }
            },
            success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_url,
            allow_promotion_codes=True,  # Permitir cupons
        )

        return {
            'session_id': session.id,
            'url': session.url
        }

    def create_portal_session(self, tenant: Tenant, return_url: str) -> str:
        """
        Cria Billing Portal session para cliente gerenciar assinatura.

        O portal permite:
        - Atualizar cartão de crédito
        - Ver faturas anteriores
        - Cancelar assinatura

        Returns:
            URL do portal
        """
        customer = self.db.query(StripeCustomer).filter(
            StripeCustomer.tenant_id == tenant.id
        ).first()

        if not customer:
            raise ValueError("Cliente não encontrado no Stripe")

        portal_session = stripe.billing_portal.Session.create(
            customer=customer.stripe_customer_id,
            return_url=return_url,
        )

        return portal_session.url

    def cancel_subscription(self, subscription_id: str, immediately: bool = False):
        """
        Cancela assinatura.

        Args:
            subscription_id: ID da subscription no Stripe
            immediately: Se True, cancela imediatamente. Se False, cancela no fim do período.
        """
        if immediately:
            # Cancelar agora
            stripe.Subscription.delete(subscription_id)
        else:
            # Cancelar no fim do período
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )

    def change_subscription_plan(
        self,
        subscription_id: str,
        new_price_id: str,
        prorate: bool = True
    ):
        """
        Muda plano da assinatura (upgrade/downgrade).

        Args:
            prorate: Se True, calcula proporcionalmente (recomendado)
        """
        # Obter subscription
        subscription = stripe.Subscription.retrieve(subscription_id)

        # Atualizar subscription
        stripe.Subscription.modify(
            subscription_id,
            proration_behavior='create_prorations' if prorate else 'none',
            items=[{
                'id': subscription['items']['data'][0].id,
                'price': new_price_id,
            }]
        )

    def sync_subscription_from_stripe(self, stripe_subscription_id: str):
        """
        Sincroniza dados da subscription do Stripe para o banco.
        Usado após webhooks.
        """
        # Buscar no Stripe
        stripe_sub = stripe.Subscription.retrieve(stripe_subscription_id)

        tenant_id = stripe_sub.metadata.get('tenant_id')
        if not tenant_id:
            raise ValueError("tenant_id não encontrado nos metadados")

        # Buscar ou criar registro local
        local_sub = self.db.query(StripeSubscription).filter(
            StripeSubscription.stripe_subscription_id == stripe_subscription_id
        ).first()

        if not local_sub:
            local_sub = StripeSubscription(
                tenant_id=tenant_id,
                stripe_subscription_id=stripe_subscription_id,
                stripe_customer_id=stripe_sub.customer,
            )
            self.db.add(local_sub)

        # Atualizar campos
        local_sub.stripe_price_id = stripe_sub['items']['data'][0].price.id
        local_sub.status = stripe_sub.status
        local_sub.current_period_start = datetime.fromtimestamp(stripe_sub.current_period_start)
        local_sub.current_period_end = datetime.fromtimestamp(stripe_sub.current_period_end)
        local_sub.cancel_at_period_end = stripe_sub.cancel_at_period_end

        if stripe_sub.trial_start:
            local_sub.trial_start = datetime.fromtimestamp(stripe_sub.trial_start)
        if stripe_sub.trial_end:
            local_sub.trial_end = datetime.fromtimestamp(stripe_sub.trial_end)

        # Atualizar status do tenant
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if tenant:
            if stripe_sub.status == 'active':
                tenant.status = 'active'
            elif stripe_sub.status in ['past_due', 'unpaid']:
                tenant.status = 'suspended'
            elif stripe_sub.status == 'canceled':
                tenant.status = 'canceled'

        self.db.commit()

    def save_invoice(self, stripe_invoice_id: str):
        """
        Salva fatura no banco de dados.
        """
        # Buscar no Stripe
        stripe_invoice = stripe.Invoice.retrieve(stripe_invoice_id)

        tenant_id = stripe_invoice.subscription_details.metadata.get('tenant_id') if stripe_invoice.subscription_details else None

        if not tenant_id:
            return

        # Verificar se já existe
        existing = self.db.query(Invoice).filter(
            Invoice.stripe_invoice_id == stripe_invoice_id
        ).first()

        if existing:
            # Atualizar
            existing.status = stripe_invoice.status
            existing.amount_paid = stripe_invoice.amount_paid / 100
            if stripe_invoice.status == 'paid':
                existing.paid_at = datetime.fromtimestamp(stripe_invoice.status_transitions.paid_at)
        else:
            # Criar
            invoice = Invoice(
                tenant_id=tenant_id,
                stripe_invoice_id=stripe_invoice_id,
                amount_due=stripe_invoice.amount_due / 100,
                amount_paid=stripe_invoice.amount_paid / 100,
                status=stripe_invoice.status,
                invoice_pdf=stripe_invoice.invoice_pdf,
                period_start=datetime.fromtimestamp(stripe_invoice.period_start),
                period_end=datetime.fromtimestamp(stripe_invoice.period_end),
            )
            self.db.add(invoice)

        self.db.commit()
```

---

### PASSO 4: API Endpoints

```python
# app/api/v1/billing.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.services.stripe_service import StripeService
from app.models.tenant import Tenant
from app.api.dependencies import get_current_tenant

router = APIRouter(prefix="/api/billing", tags=["Billing"])

class CreateCheckoutRequest(BaseModel):
    price_id: str  # price_starter_monthly
    plan: str  # starter, professional

class CheckoutResponse(BaseModel):
    checkout_url: str

@router.post("/checkout", response_model=CheckoutResponse)
def create_checkout_session(
    data: CreateCheckoutRequest,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Cria Checkout Session para iniciar assinatura.

    Frontend redireciona usuário para checkout_url do Stripe.
    """
    stripe_service = StripeService(db)

    # URLs de retorno
    success_url = f"{settings.FRONTEND_URL}/billing/success"
    cancel_url = f"{settings.FRONTEND_URL}/billing/canceled"

    try:
        session = stripe_service.create_checkout_session(
            tenant=tenant,
            price_id=data.price_id,
            success_url=success_url,
            cancel_url=cancel_url,
            trial_days=14
        )

        return CheckoutResponse(checkout_url=session['url'])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PortalResponse(BaseModel):
    portal_url: str

@router.post("/portal", response_model=PortalResponse)
def create_portal_session(
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Cria Billing Portal para cliente gerenciar assinatura.

    Cliente pode:
    - Atualizar cartão
    - Ver faturas
    - Cancelar assinatura
    """
    stripe_service = StripeService(db)

    return_url = f"{settings.FRONTEND_URL}/settings/billing"

    try:
        portal_url = stripe_service.create_portal_session(tenant, return_url)
        return PortalResponse(portal_url=portal_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SubscriptionInfo(BaseModel):
    status: str
    plan: str
    current_period_end: str
    cancel_at_period_end: bool

@router.get("/subscription", response_model=SubscriptionInfo)
def get_subscription_info(
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Retorna informações da assinatura atual.
    """
    subscription = db.query(StripeSubscription).filter(
        StripeSubscription.tenant_id == tenant.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada")

    return SubscriptionInfo(
        status=subscription.status,
        plan=subscription.plan,
        current_period_end=subscription.current_period_end.isoformat(),
        cancel_at_period_end=subscription.cancel_at_period_end
    )


@router.post("/cancel")
def cancel_subscription(
    immediately: bool = False,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Cancela assinatura.

    Args:
        immediately: Se True, cancela agora. Se False, no fim do período.
    """
    subscription = db.query(StripeSubscription).filter(
        StripeSubscription.tenant_id == tenant.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="Assinatura não encontrada")

    stripe_service = StripeService(db)

    try:
        stripe_service.cancel_subscription(
            subscription.stripe_subscription_id,
            immediately=immediately
        )

        return {"message": "Assinatura cancelada com sucesso"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### PASSO 5: Webhooks do Stripe

```python
# app/api/webhooks/stripe.py
from fastapi import APIRouter, Request, HTTPException, Header
from sqlalchemy.orm import Session
import stripe

from app.core.config import settings
from app.database import SessionLocal
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None)
):
    """
    Endpoint para receber webhooks do Stripe.

    Eventos tratados:
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    payload = await request.body()

    # Verificar assinatura do webhook
    try:
        event = stripe.Webhook.construct_event(
            payload,
            stripe_signature,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Processar evento
    db = SessionLocal()
    stripe_service = StripeService(db)

    try:
        event_type = event['type']
        data_object = event['data']['object']

        if event_type == 'customer.subscription.created':
            # Nova assinatura criada
            stripe_service.sync_subscription_from_stripe(data_object['id'])
            print(f"✅ Subscription criada: {data_object['id']}")

        elif event_type == 'customer.subscription.updated':
            # Assinatura atualizada (upgrade, downgrade, cancelamento)
            stripe_service.sync_subscription_from_stripe(data_object['id'])
            print(f"✅ Subscription atualizada: {data_object['id']}")

        elif event_type == 'customer.subscription.deleted':
            # Assinatura cancelada
            stripe_service.sync_subscription_from_stripe(data_object['id'])
            print(f"⚠️  Subscription deletada: {data_object['id']}")

        elif event_type == 'invoice.payment_succeeded':
            # Pagamento bem-sucedido
            stripe_service.save_invoice(data_object['id'])
            print(f"✅ Pagamento recebido: {data_object['id']}")

        elif event_type == 'invoice.payment_failed':
            # Falha no pagamento
            stripe_service.save_invoice(data_object['id'])
            # TODO: Enviar email para cliente
            # TODO: Suspender acesso após X tentativas
            print(f"❌ Falha no pagamento: {data_object['id']}")

        else:
            print(f"⚠️  Evento não tratado: {event_type}")

    finally:
        db.close()

    return {"status": "success"}
```

**Configurar Webhook no Stripe Dashboard:**
1. Developers → Webhooks → Add endpoint
2. URL: `https://api.sentinel.com.br/webhooks/stripe`
3. Eventos:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
4. Copiar **Signing secret** → adicionar ao `.env` como `STRIPE_WEBHOOK_SECRET`

---

### PASSO 6: Frontend (Checkout)

```jsx
// frontend/src/pages/Billing.jsx
import { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { CreditCard, Check } from 'lucide-react';
import api from '../services/api';

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY);

const plans = [
  {
    name: 'Starter',
    price: 49,
    priceId: 'price_starter_monthly',
    features: [
      '1-5 propriedades',
      'Sincronização Airbnb + Booking',
      'Detecção de conflitos',
      'Bot do Telegram',
      'Suporte por email',
    ]
  },
  {
    name: 'Professional',
    price: 149,
    priceId: 'price_professional_monthly',
    features: [
      '6-30 propriedades',
      'Tudo do Starter',
      'Multi-usuários',
      'API access',
      'Webhooks customizados',
      'Suporte prioritário',
    ],
    recommended: true,
  },
];

export default function Billing() {
  const [loading, setLoading] = useState(false);

  const handleSubscribe = async (priceId, planName) => {
    setLoading(true);

    try {
      // Criar checkout session
      const response = await api.post('/api/billing/checkout', {
        price_id: priceId,
        plan: planName.toLowerCase()
      });

      // Redirecionar para Stripe Checkout
      window.location.href = response.data.checkout_url;

    } catch (error) {
      console.error('Erro ao criar checkout:', error);
      alert('Erro ao processar. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold mb-4">Escolha seu plano</h1>
        <p className="text-gray-600">
          14 dias de teste grátis. Cancele quando quiser.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className={`border rounded-lg p-8 relative ${
              plan.recommended ? 'border-blue-500 shadow-lg' : 'border-gray-200'
            }`}
          >
            {plan.recommended && (
              <div className="absolute top-0 right-6 -translate-y-1/2">
                <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                  Recomendado
                </span>
              </div>
            )}

            <div className="mb-6">
              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold">R$ {plan.price}</span>
                <span className="text-gray-600">/mês</span>
              </div>
            </div>

            <ul className="space-y-3 mb-8">
              {plan.features.map((feature, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>

            <button
              onClick={() => handleSubscribe(plan.priceId, plan.name)}
              disabled={loading}
              className={`w-full py-3 rounded-lg font-semibold transition ${
                plan.recommended
                  ? 'bg-blue-500 text-white hover:bg-blue-600'
                  : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
              } disabled:opacity-50`}
            >
              {loading ? 'Processando...' : 'Começar teste grátis'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 🧪 TESTES

```python
# tests/test_billing.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_create_checkout_session(client, auth_headers):
    """Testa criação de checkout session"""
    with patch('app.services.stripe_service.stripe.checkout.Session.create') as mock_create:
        mock_create.return_value = MagicMock(
            id='cs_test_123',
            url='https://checkout.stripe.com/test'
        )

        response = client.post(
            '/api/billing/checkout',
            json={'price_id': 'price_starter_monthly', 'plan': 'starter'},
            headers=auth_headers
        )

        assert response.status_code == 200
        assert 'checkout_url' in response.json()

def test_webhook_subscription_created(client):
    """Testa webhook de subscription criada"""
    payload = {
        'type': 'customer.subscription.created',
        'data': {
            'object': {
                'id': 'sub_123',
                'customer': 'cus_123',
                'status': 'active',
                'metadata': {'tenant_id': 'test-tenant-id'}
            }
        }
    }

    with patch('stripe.Webhook.construct_event') as mock_verify:
        mock_verify.return_value = payload

        response = client.post(
            '/webhooks/stripe',
            json=payload,
            headers={'stripe-signature': 'test-signature'}
        )

        assert response.status_code == 200
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Setup
- [ ] Criar conta no Stripe
- [ ] Obter API keys (test e live)
- [ ] Instalar `stripe` package
- [ ] Configurar produtos e preços no Stripe
- [ ] Criar webhook endpoint

### Backend
- [ ] Criar models (StripeCustomer, StripeSubscription, Invoice)
- [ ] Implementar StripeService
- [ ] Criar endpoints de billing (/checkout, /portal, /subscription)
- [ ] Implementar webhook handler
- [ ] Configurar webhook no Stripe Dashboard
- [ ] Testar webhooks com Stripe CLI

### Frontend
- [ ] Criar página de escolha de planos
- [ ] Integrar Stripe.js
- [ ] Implementar fluxo de checkout
- [ ] Criar página de gerenciamento de assinatura
- [ ] Indicador visual do plano atual

### Testes
- [ ] Testar checkout com cartão de teste
- [ ] Testar webhooks (subscription.created, updated, deleted)
- [ ] Testar falha de pagamento
- [ ] Testar cancelamento de assinatura
- [ ] Testar upgrade/downgrade de planos

### Deploy
- [ ] Trocar para chaves de produção
- [ ] Configurar webhook em produção
- [ ] Compliance: Termos de serviço e política de privacidade
- [ ] Testar em produção com cartão de teste
- [ ] Ativar conta (remover modo de teste)

---

## 💰 TAXAS DO STRIPE NO BRASIL

- **Cartão de crédito brasileiro:** 4.99% + R$ 0,59 por transação
- **Cartão de crédito internacional:** 5.99% + R$ 0,59
- **Boleto:** 3.99% + R$ 2,00 (mínimo R$ 3,00)

**Exemplo:**
- Assinatura Starter: R$ 49,00
- Taxa Stripe: R$ 49,00 × 4.99% + R$ 0,59 = R$ 3,04
- **Você recebe: R$ 45,96**

---

## ✅ CONCLUSÃO

Com o Stripe integrado, o SENTINEL agora possui:
- ✅ Cobranças recorrentes automáticas
- ✅ Gestão de assinaturas self-service
- ✅ Compliance PCI-DSS (Stripe é certificado)
- ✅ Webhooks para sincronização em tempo real
- ✅ Portal do cliente para gerenciar pagamento

**Próximo passo:** Implementar sistema de emails transacionais para notificações de pagamento.
