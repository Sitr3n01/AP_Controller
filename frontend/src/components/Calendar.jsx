import { useState } from 'react';
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon } from 'lucide-react';
import './Calendar.css';

const DAYS_OF_WEEK = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
const MONTHS = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
];

const CalendarComponent = ({ events = [], onEventClick, currentDate = new Date() }) => {
  const [selectedDate, setSelectedDate] = useState(currentDate);

  const year = selectedDate.getFullYear();
  const month = selectedDate.getMonth();

  // Navegar para mês anterior
  const previousMonth = () => {
    setSelectedDate(new Date(year, month - 1, 1));
  };

  // Navegar para próximo mês
  const nextMonth = () => {
    setSelectedDate(new Date(year, month + 1, 1));
  };

  // Voltar para hoje
  const goToToday = () => {
    setSelectedDate(new Date());
  };

  // Gerar dias do calendário
  const getDaysInMonth = () => {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    const days = [];

    // Dias do mês anterior (para preencher a primeira semana)
    const prevMonthLastDay = new Date(year, month, 0).getDate();
    for (let i = startingDayOfWeek - 1; i >= 0; i--) {
      days.push({
        date: new Date(year, month - 1, prevMonthLastDay - i),
        isCurrentMonth: false,
      });
    }

    // Dias do mês atual
    for (let day = 1; day <= daysInMonth; day++) {
      days.push({
        date: new Date(year, month, day),
        isCurrentMonth: true,
      });
    }

    // Dias do próximo mês (para preencher a última semana)
    const remainingDays = 42 - days.length; // 6 semanas * 7 dias
    for (let day = 1; day <= remainingDays; day++) {
      days.push({
        date: new Date(year, month + 1, day),
        isCurrentMonth: false,
      });
    }

    return days;
  };

  // Obter eventos para um dia específico
  const getEventsForDay = (date) => {
    return events.filter(event => {
      const eventStart = new Date(event.check_in_date);
      const eventEnd = new Date(event.check_out_date);
      const dayStart = new Date(date);
      dayStart.setHours(0, 0, 0, 0);
      const dayEnd = new Date(date);
      dayEnd.setHours(23, 59, 59, 999);

      return (eventStart <= dayEnd && eventEnd >= dayStart);
    });
  };

  // Verificar se é hoje
  const isToday = (date) => {
    const today = new Date();
    return (
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear()
    );
  };

  const days = getDaysInMonth();

  return (
    <div className="calendar-widget">
      <div className="calendar-header">
        <h2 className="calendar-title">
          <CalendarIcon size={24} />
          {MONTHS[month]} {year}
        </h2>
        <div className="calendar-nav">
          <button className="btn btn-secondary btn-sm" onClick={goToToday}>
            Hoje
          </button>
          <button className="btn btn-secondary btn-icon" onClick={previousMonth}>
            <ChevronLeft size={18} />
          </button>
          <button className="btn btn-secondary btn-icon" onClick={nextMonth}>
            <ChevronRight size={18} />
          </button>
        </div>
      </div>

      <div className="calendar-grid">
        {/* Cabeçalho dos dias da semana */}
        {DAYS_OF_WEEK.map(day => (
          <div key={day} className="calendar-day-header">
            {day}
          </div>
        ))}

        {/* Dias do mês */}
        {days.map((day, index) => {
          const dayEvents = getEventsForDay(day.date);
          const isCurrentDay = isToday(day.date);

          return (
            <div
              key={index}
              className={`calendar-day ${
                !day.isCurrentMonth ? 'other-month' : ''
              } ${isCurrentDay ? 'today' : ''} ${
                dayEvents.length > 0 ? 'has-events' : ''
              }`}
            >
              <div className="day-number">{day.date.getDate()}</div>
              <div className="day-events">
                {dayEvents.slice(0, 3).map((event, idx) => (
                  <div
                    key={idx}
                    className={`calendar-event event-${event.platform}`}
                    onClick={() => onEventClick && onEventClick(event)}
                    title={`${event.guest_name} - ${event.platform}`}
                  >
                    <span className="event-guest">{event.guest_name}</span>
                  </div>
                ))}
                {dayEvents.length > 3 && (
                  <div className="event-more">
                    +{dayEvents.length - 3} mais
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Legenda */}
      <div className="calendar-legend">
        <div className="legend-item">
          <span className="legend-dot event-airbnb"></span>
          Airbnb
        </div>
        <div className="legend-item">
          <span className="legend-dot event-booking"></span>
          Booking.com
        </div>
        <div className="legend-item">
          <span className="legend-dot event-manual"></span>
          Manual
        </div>
      </div>
    </div>
  );
};

export default CalendarComponent;
