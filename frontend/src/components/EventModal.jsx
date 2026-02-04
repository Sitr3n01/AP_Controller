import { X, Calendar, User, Users, DollarSign, MapPin, Clock } from 'lucide-react';
import { formatDateFull } from '../utils/formatters';
import './EventModal.css';

const EventModal = ({ event, onClose }) => {
  if (!event) return null;

  // formatDate → usando formatDateFull de ../utils/formatters

  const getPlatformColor = (platform) => {
    const colors = {
      airbnb: 'danger',
      booking: 'info',
      manual: 'secondary',
    };
    return colors[platform] || 'secondary';
  };

  const getPlatformName = (platform) => {
    const names = {
      airbnb: 'Airbnb',
      booking: 'Booking.com',
      manual: 'Manual',
    };
    return names[platform] || platform;
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <h2>Detalhes da Reserva</h2>
            <span className={`badge badge-${getPlatformColor(event.platform)}`}>
              {getPlatformName(event.platform)}
            </span>
          </div>
          <button className="modal-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          <div className="event-detail-section">
            <div className="detail-item">
              <div className="detail-icon">
                <User size={18} />
              </div>
              <div className="detail-content">
                <span className="detail-label">Hóspede</span>
                <span className="detail-value">{event.guest_name}</span>
              </div>
            </div>

            {event.guest_email && (
              <div className="detail-item">
                <div className="detail-icon">
                  <MapPin size={18} />
                </div>
                <div className="detail-content">
                  <span className="detail-label">Email</span>
                  <span className="detail-value">{event.guest_email}</span>
                </div>
              </div>
            )}

            {event.guest_phone && (
              <div className="detail-item">
                <div className="detail-icon">
                  <Clock size={18} />
                </div>
                <div className="detail-content">
                  <span className="detail-label">Telefone</span>
                  <span className="detail-value">{event.guest_phone}</span>
                </div>
              </div>
            )}

            <div className="detail-item">
              <div className="detail-icon">
                <Users size={18} />
              </div>
              <div className="detail-content">
                <span className="detail-label">Número de Hóspedes</span>
                <span className="detail-value">{event.guest_count || 1}</span>
              </div>
            </div>
          </div>

          <div className="event-detail-section">
            <h3 className="section-subtitle">Período</h3>

            <div className="detail-item">
              <div className="detail-icon">
                <Calendar size={18} />
              </div>
              <div className="detail-content">
                <span className="detail-label">Check-in</span>
                <span className="detail-value">
                  {formatDateFull(event.check_in_date)}
                </span>
              </div>
            </div>

            <div className="detail-item">
              <div className="detail-icon">
                <Calendar size={18} />
              </div>
              <div className="detail-content">
                <span className="detail-label">Check-out</span>
                <span className="detail-value">
                  {formatDateFull(event.check_out_date)}
                </span>
              </div>
            </div>

            <div className="detail-item">
              <div className="detail-icon">
                <Clock size={18} />
              </div>
              <div className="detail-content">
                <span className="detail-label">Duração</span>
                <span className="detail-value">
                  {event.nights_count} {event.nights_count === 1 ? 'noite' : 'noites'}
                </span>
              </div>
            </div>
          </div>

          {event.total_price && (
            <div className="event-detail-section">
              <h3 className="section-subtitle">Valor</h3>

              <div className="detail-item">
                <div className="detail-icon">
                  <DollarSign size={18} />
                </div>
                <div className="detail-content">
                  <span className="detail-label">Total</span>
                  <span className="detail-value price">
                    {new Intl.NumberFormat('pt-BR', {
                      style: 'currency',
                      currency: event.currency || 'BRL'
                    }).format(event.total_price)}
                  </span>
                </div>
              </div>
            </div>
          )}

          {event.external_id && (
            <div className="event-detail-section">
              <h3 className="section-subtitle">Informações Técnicas</h3>

              <div className="detail-item">
                <div className="detail-content">
                  <span className="detail-label">ID Externo</span>
                  <span className="detail-value code">{event.external_id}</span>
                </div>
              </div>

              <div className="detail-item">
                <div className="detail-content">
                  <span className="detail-label">Status</span>
                  <span className={`badge badge-${getStatusColor(event.status)}`}>
                    {getStatusName(event.status)}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
};

const getStatusColor = (status) => {
  const colors = {
    confirmed: 'success',
    cancelled: 'danger',
    completed: 'secondary',
    blocked: 'warning',
  };
  return colors[status] || 'secondary';
};

const getStatusName = (status) => {
  const names = {
    confirmed: 'Confirmada',
    cancelled: 'Cancelada',
    completed: 'Concluída',
    blocked: 'Bloqueada',
  };
  return names[status] || status;
};

export default EventModal;
