import { useState, useEffect } from 'react';
import { Save, RefreshCw, CheckCircle, AlertCircle } from 'lucide-react';
import { systemAPI, settingsAPI } from '../services/api';
import './Settings.css';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('easy'); // 'easy' or 'advanced'
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);

  const [settings, setSettings] = useState({
    // Dados do imóvel
    propertyName: 'Apartamento 2 Quartos - Goiânia',
    propertyAddress: 'Rua Exemplo, 123, Setor Central, 74000-000 Goiânia - GO',
    maxGuests: 4,
    condoName: 'Condomínio Exemplo',
    condoAdminName: 'Administração do Condomínio',

    // URLs iCal
    airbnbIcalUrl: '',
    bookingIcalUrl: '',

    // Sincronização
    syncIntervalMinutes: 30,

    // Telegram (futuro)
    telegramBotToken: '',
    telegramAdminUserIds: '',

    // Features
    enableAutoDocumentGeneration: false,
    enableConflictNotifications: true,
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      setLoading(true);
      const response = await systemAPI.getInfo();

      // Mapear os dados da API para o estado local
      setSettings(prev => ({
        ...prev,
        propertyName: response.data.property_name || prev.propertyName,
        syncIntervalMinutes: response.data.sync_interval_minutes || prev.syncIntervalMinutes,
        enableAutoDocumentGeneration: response.data.features?.document_generation || prev.enableAutoDocumentGeneration,
        enableConflictNotifications: response.data.features?.conflict_notifications || prev.enableConflictNotifications,
      }));
    } catch (error) {
      console.error('Error loading settings:', error);
      showMessage('Erro ao carregar configurações', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await settingsAPI.update(settings);
      showMessage('Configurações salvas com sucesso!', 'success');
    } catch (error) {
      console.error('Error saving settings:', error);
      showMessage('Erro ao salvar configurações', 'error');
    } finally {
      setSaving(false);
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 3000);
  };

  const handleChange = (field, value) => {
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  if (loading) {
    return (
      <div className="settings-page">
        <div className="loading">Carregando configurações...</div>
      </div>
    );
  }

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1>Configurações</h1>
        <p className="subtitle">Configure todos os parâmetros do sistema aqui</p>
      </div>

      {message && (
        <div className={`message message-${message.type}`}>
          {message.type === 'success' ? <CheckCircle size={18} /> : <AlertCircle size={18} />}
          <span>{message.text}</span>
        </div>
      )}

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'easy' ? 'active' : ''}`}
          onClick={() => setActiveTab('easy')}
        >
          Configuração Fácil
        </button>
        <button
          className={`tab ${activeTab === 'advanced' ? 'active' : ''}`}
          onClick={() => setActiveTab('advanced')}
        >
          Configuração Avançada
        </button>
      </div>

      <div className="settings-content">
        {activeTab === 'easy' ? (
          <EasySettings settings={settings} onChange={handleChange} />
        ) : (
          <AdvancedSettings settings={settings} onChange={handleChange} />
        )}
      </div>

      <div className="settings-actions">
        <button className="btn btn-secondary" onClick={loadSettings} disabled={saving}>
          <RefreshCw size={16} />
          Restaurar
        </button>
        <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
          <Save size={16} />
          {saving ? 'Salvando...' : 'Salvar Configurações'}
        </button>
      </div>
    </div>
  );
};

// ========== ABA FÁCIL ==========
const EasySettings = ({ settings, onChange }) => {
  return (
    <div className="settings-section">
      <div className="section-group">
        <h3 className="section-title">📍 Dados do Imóvel</h3>
        <p className="section-description">
          Informações básicas sobre o apartamento
        </p>

        <div className="form-grid">
          <div className="form-field">
            <label className="label">Nome do Imóvel</label>
            <input
              type="text"
              className="input"
              value={settings.propertyName}
              onChange={(e) => onChange('propertyName', e.target.value)}
              placeholder="Ex: Apartamento 2 Quartos - Centro"
            />
          </div>

          <div className="form-field">
            <label className="label">Endereço Completo</label>
            <input
              type="text"
              className="input"
              value={settings.propertyAddress}
              onChange={(e) => onChange('propertyAddress', e.target.value)}
              placeholder="Rua, Número, Bairro, CEP, Cidade - Estado"
            />
          </div>

          <div className="form-field">
            <label className="label">Máximo de Hóspedes</label>
            <input
              type="number"
              className="input"
              value={settings.maxGuests}
              onChange={(e) => onChange('maxGuests', parseInt(e.target.value))}
              min="1"
              max="20"
            />
          </div>
        </div>
      </div>

      <div className="section-group">
        <h3 className="section-title">🏢 Dados do Condomínio</h3>
        <p className="section-description">
          Informações para geração de documentos de autorização
        </p>

        <div className="form-grid">
          <div className="form-field">
            <label className="label">Nome do Condomínio</label>
            <input
              type="text"
              className="input"
              value={settings.condoName}
              onChange={(e) => onChange('condoName', e.target.value)}
              placeholder="Ex: Condomínio Residencial Exemplo"
            />
          </div>

          <div className="form-field">
            <label className="label">Nome da Administração</label>
            <input
              type="text"
              className="input"
              value={settings.condoAdminName}
              onChange={(e) => onChange('condoAdminName', e.target.value)}
              placeholder="Ex: Administradora XYZ Ltda"
            />
          </div>
        </div>
      </div>

      <div className="section-group">
        <h3 className="section-title">🔗 Conexão com Plataformas</h3>
        <p className="section-description">
          URLs de sincronização do calendário (iCal)
        </p>

        <div className="info-box">
          <p><strong>Como obter as URLs:</strong></p>
          <ul>
            <li><strong>Airbnb:</strong> Vá em Calendário → Disponibilidade → Exportar calendário</li>
            <li><strong>Booking:</strong> Vá em Calendário → Sincronização → Link de exportação iCal</li>
          </ul>
        </div>

        <div className="form-grid">
          <div className="form-field">
            <label className="label">URL iCal do Airbnb</label>
            <input
              type="url"
              className="input"
              value={settings.airbnbIcalUrl}
              onChange={(e) => onChange('airbnbIcalUrl', e.target.value)}
              placeholder="https://www.airbnb.com/calendar/ical/XXXXXXX.ics"
            />
          </div>

          <div className="form-field">
            <label className="label">URL iCal do Booking.com</label>
            <input
              type="url"
              className="input"
              value={settings.bookingIcalUrl}
              onChange={(e) => onChange('bookingIcalUrl', e.target.value)}
              placeholder="https://admin.booking.com/hotel/hoteladmin/ical/XXXXXXX.ics"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// ========== ABA AVANÇADA ==========
const AdvancedSettings = ({ settings, onChange }) => {
  return (
    <div className="settings-section">
      <div className="section-group">
        <h3 className="section-title">⚙️ Sincronização</h3>
        <p className="section-description">
          Controle de frequência de atualização dos calendários
        </p>

        <div className="form-grid">
          <div className="form-field">
            <label className="label">Intervalo de Sincronização (minutos)</label>
            <input
              type="number"
              className="input"
              value={settings.syncIntervalMinutes}
              onChange={(e) => onChange('syncIntervalMinutes', parseInt(e.target.value))}
              min="5"
              max="1440"
            />
            <small className="field-help">
              Frequência de atualização automática (recomendado: 30 minutos)
            </small>
          </div>
        </div>
      </div>

      <div className="section-group">
        <h3 className="section-title">📱 Telegram Bot (MVP2)</h3>
        <p className="section-description">
          Configurações para notificações via Telegram
        </p>

        <div className="info-box warning">
          <p><strong>⚠️ Funcionalidade do MVP2</strong></p>
          <p>As notificações via Telegram serão implementadas na próxima versão.</p>
        </div>

        <div className="form-grid">
          <div className="form-field">
            <label className="label">Token do Bot</label>
            <input
              type="text"
              className="input"
              value={settings.telegramBotToken}
              onChange={(e) => onChange('telegramBotToken', e.target.value)}
              placeholder="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
              disabled
            />
            <small className="field-help">
              Obtenha em: @BotFather no Telegram
            </small>
          </div>

          <div className="form-field">
            <label className="label">IDs de Usuários Admin</label>
            <input
              type="text"
              className="input"
              value={settings.telegramAdminUserIds}
              onChange={(e) => onChange('telegramAdminUserIds', e.target.value)}
              placeholder="123456789,987654321"
              disabled
            />
            <small className="field-help">
              IDs separados por vírgula. Obtenha em: @userinfobot
            </small>
          </div>
        </div>
      </div>

      <div className="section-group">
        <h3 className="section-title">🎛️ Funcionalidades</h3>
        <p className="section-description">
          Ative ou desative recursos do sistema
        </p>

        <div className="form-grid">
          <div className="form-field checkbox-field">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.enableConflictNotifications}
                onChange={(e) => onChange('enableConflictNotifications', e.target.checked)}
              />
              <span>Notificações de Conflitos</span>
            </label>
            <small className="field-help">
              Enviar alertas quando conflitos de reserva forem detectados
            </small>
          </div>

          <div className="form-field checkbox-field">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.enableAutoDocumentGeneration}
                onChange={(e) => onChange('enableAutoDocumentGeneration', e.target.value)}
                disabled
              />
              <span>Geração Automática de Documentos (MVP2)</span>
            </label>
            <small className="field-help">
              Gerar automaticamente documentos de autorização do condomínio
            </small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
