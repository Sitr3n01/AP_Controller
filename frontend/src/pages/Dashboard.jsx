import { useState, useEffect } from 'react';
import {
  Calendar as CalendarIcon,
  AlertTriangle,
  TrendingUp,
  RefreshCw,
  DollarSign,
  Users,
  CheckCircle,
  Clock
} from 'lucide-react';
import { statisticsAPI, conflictsAPI, bookingsAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [conflicts, setConflicts] = useState(null);
  const [upcomingBookings, setUpcomingBookings] = useState([]);
  const [todayCheckins, setTodayCheckins] = useState([]);
  const [todayCheckouts, setTodayCheckouts] = useState([]);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const [statsResponse, conflictsResponse, bookingsResponse] = await Promise.all([
        statisticsAPI.getDashboard(1), // property_id = 1
        conflictsAPI.getSummary(1),
        bookingsAPI.getUpcoming({ property_id: 1, limit: 5 }),
      ]);

      setStats(statsResponse.data);
      setConflicts(conflictsResponse.data);
      setUpcomingBookings(bookingsResponse.data?.bookings || []);

      // Filtrar check-ins e check-outs de hoje
      const today = new Date().toISOString().split('T')[0];
      const allBookings = bookingsResponse.data?.bookings || [];
      setTodayCheckins(allBookings.filter(b => b.check_in_date?.split('T')[0] === today));
      setTodayCheckouts(allBookings.filter(b => b.check_out_date?.split('T')[0] === today));
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="loading-state">
          <RefreshCw className="spin" size={32} />
          <p>Carregando dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <h1>Dashboard</h1>
          <p className="subtitle">Visão geral do seu apartamento</p>
        </div>
        <button className="btn btn-primary" onClick={loadDashboard}>
          <RefreshCw size={16} />
          Atualizar
        </button>
      </div>

      {/* Cards de estatísticas principais */}
      <div className="stats-grid">
        <StatCard
          title="Total de Reservas"
          value={stats?.total_bookings || 0}
          icon={<CalendarIcon size={24} />}
          color="primary"
        />
        <StatCard
          title="Reservas Ativas"
          value={stats?.active_bookings || 0}
          icon={<CheckCircle size={24} />}
          color="success"
        />
        <StatCard
          title="Conflitos Ativos"
          value={conflicts?.total || 0}
          icon={<AlertTriangle size={24} />}
          color={conflicts?.total > 0 ? 'danger' : 'success'}
          warning={conflicts?.total > 0}
        />
        <StatCard
          title="Taxa de Ocupação"
          value={`${stats?.occupancy_rate || 0}%`}
          icon={<TrendingUp size={24} />}
          color="info"
        />
      </div>

      {/* Cards de estatísticas secundárias */}
      <div className="stats-grid-secondary">
        <StatCardSmall
          title="Receita Mensal"
          value={formatCurrency(stats?.monthly_revenue || 0)}
          icon={<DollarSign size={20} />}
          color="success"
        />
        <StatCardSmall
          title="Média de Hóspedes"
          value={stats?.avg_guests || 0}
          icon={<Users size={20} />}
          color="info"
        />
        <StatCardSmall
          title="Check-ins Hoje"
          value={todayCheckins.length}
          icon={<Clock size={20} />}
          color="primary"
        />
        <StatCardSmall
          title="Check-outs Hoje"
          value={todayCheckouts.length}
          icon={<Clock size={20} />}
          color="primary"
        />
      </div>

      {/* Check-ins e Check-outs de Hoje */}
      {(todayCheckins.length > 0 || todayCheckouts.length > 0) && (
        <div className="section">
          <div className="today-activities">
            {todayCheckins.length > 0 && (
              <div className="activity-column">
                <h3 className="activity-title">
                  <Clock size={18} />
                  Check-ins Hoje ({todayCheckins.length})
                </h3>
                <div className="activity-list">
                  {todayCheckins.map((booking) => (
                    <div key={booking.id} className="activity-card checkin">
                      <div className="activity-header">
                        <span className="guest-name">{booking.guest_name}</span>
                        <span className={`badge badge-${getPlatformColor(booking.platform)}`}>
                          {booking.platform}
                        </span>
                      </div>
                      <div className="activity-info">
                        <Users size={14} />
                        <span>{booking.guest_count} hóspede{booking.guest_count !== 1 ? 's' : ''}</span>
                        <span className="separator">•</span>
                        <span>{booking.nights_count} noite{booking.nights_count !== 1 ? 's' : ''}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {todayCheckouts.length > 0 && (
              <div className="activity-column">
                <h3 className="activity-title">
                  <Clock size={18} />
                  Check-outs Hoje ({todayCheckouts.length})
                </h3>
                <div className="activity-list">
                  {todayCheckouts.map((booking) => (
                    <div key={booking.id} className="activity-card checkout">
                      <div className="activity-header">
                        <span className="guest-name">{booking.guest_name}</span>
                        <span className={`badge badge-${getPlatformColor(booking.platform)}`}>
                          {booking.platform}
                        </span>
                      </div>
                      <div className="activity-info">
                        <span>Liberar apartamento</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Próximas reservas */}
      {upcomingBookings.length > 0 && (
        <div className="section">
          <h2 className="section-title">Próximas Reservas (5 dias)</h2>
          <div className="reservations-list">
            {upcomingBookings.slice(0, 5).map((booking) => (
              <div key={booking.id} className="reservation-card">
                <div className="reservation-header">
                  <span className="guest-name">{booking.guest_name}</span>
                  <span className={`badge badge-${getPlatformColor(booking.platform)}`}>
                    {booking.platform}
                  </span>
                </div>
                <div className="reservation-dates">
                  <CalendarIcon size={14} />
                  <span>{formatDate(booking.check_in_date)} até {formatDate(booking.check_out_date)}</span>
                  <span className="nights">({booking.nights_count} noite{booking.nights_count !== 1 ? 's' : ''})</span>
                </div>
                <div className="reservation-details">
                  <span className="detail-item">
                    <Users size={14} />
                    {booking.guest_count} hóspede{booking.guest_count !== 1 ? 's' : ''}
                  </span>
                  {booking.total_price && (
                    <span className="detail-item">
                      <DollarSign size={14} />
                      {formatCurrency(booking.total_price)}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Alertas de conflitos */}
      {conflicts && conflicts.total > 0 && (
        <div className="section">
          <div className="alert alert-warning">
            <AlertTriangle size={20} />
            <div>
              <strong>Atenção! {conflicts.total} conflito(s) detectado(s)</strong>
              <p>
                {conflicts.duplicates > 0 && `${conflicts.duplicates} duplicata(s), `}
                {conflicts.overlaps > 0 && `${conflicts.overlaps} sobreposição(ões)`}
              </p>
              <p className="alert-action">
                Veja a aba <strong>Conflitos</strong> para mais detalhes e resolução.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Informações do sistema */}
      {stats && (
        <div className="section">
          <h2 className="section-title">Informações do Sistema</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Última Sincronização</span>
              <span className="info-value">{formatDateTime(stats.last_sync)}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Próxima Sincronização</span>
              <span className="info-value">{formatDateTime(stats.next_sync)}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Check-ins Hoje</span>
              <span className="info-value">{stats.today_checkins || 0}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Check-outs Hoje</span>
              <span className="info-value">{stats.today_checkouts || 0}</span>
            </div>
          </div>
        </div>
      )}

      {/* Estado vazio */}
      {stats && stats.total_bookings === 0 && (
        <div className="empty-state">
          <CalendarIcon size={48} />
          <h3>Nenhuma reserva encontrada</h3>
          <p>Configure as URLs dos calendários nas Configurações para começar a sincronizar.</p>
        </div>
      )}
    </div>
  );
};

const StatCard = ({ title, value, icon, color, warning }) => {
  return (
    <div className={`stat-card stat-card-${color} ${warning ? 'warning' : ''}`}>
      <div className="stat-icon">{icon}</div>
      <div className="stat-content">
        <p className="stat-title">{title}</p>
        <p className="stat-value">{value}</p>
      </div>
    </div>
  );
};

const StatCardSmall = ({ title, value, icon, color }) => {
  return (
    <div className={`stat-card-small stat-card-${color}`}>
      <div className="stat-icon-small">{icon}</div>
      <div className="stat-content-small">
        <p className="stat-title-small">{title}</p>
        <p className="stat-value-small">{value}</p>
      </div>
    </div>
  );
};

// Utilitários
const getPlatformColor = (platform) => {
  const colors = {
    airbnb: 'danger',
    booking: 'info',
    manual: 'secondary',
  };
  return colors[platform] || 'secondary';
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' });
};

const formatDateTime = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString('pt-BR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const formatCurrency = (value) => {
  if (!value) return 'R$ 0,00';
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};

export default Dashboard;
