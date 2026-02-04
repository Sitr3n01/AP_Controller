/**
 * Utilitários de formatação centralizados.
 * Evita duplicação de funções formatDate/formatDateTime/formatCurrency em cada página.
 */

/**
 * Formata data curta: "15 de jan."
 */
export const formatDateShort = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' });
};

/**
 * Formata data completa: "15 de janeiro de 2025"
 */
export const formatDateFull = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
};

/**
 * Formata data + hora: "15 de jan., 14:30"
 */
export const formatDateTime = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString('pt-BR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Formata data + hora + ano: "15 de jan. de 2025, 14:30"
 */
export const formatDateTimeFull = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Formata timestamp relativo: "Agora", "Há 5 min", "Há 2h", "Há 3d"
 */
export const formatRelativeTime = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return 'Agora';
  if (diffMin < 60) return `Há ${diffMin} min`;
  const diffH = Math.floor(diffMin / 60);
  if (diffH < 24) return `Há ${diffH}h`;
  const diffD = Math.floor(diffH / 24);
  if (diffD < 7) return `Há ${diffD}d`;
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
};

/**
 * Formata moeda BRL: "R$ 1.234,56"
 */
export const formatCurrency = (value) => {
  if (!value) return 'R$ 0,00';
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};

/**
 * Formata moeda BRL abreviada: "R$ 1,2k"
 */
export const formatCurrencyShort = (value) => {
  if (!value) return 'R$ 0';
  if (value >= 1000) {
    return `R$ ${(value / 1000).toFixed(1)}k`;
  }
  return `R$ ${value}`;
};

/**
 * Formata mês de string "YYYY-MM": "jan./25"
 */
export const formatMonth = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString + '-01');
  return date.toLocaleDateString('pt-BR', { month: 'short', year: '2-digit' });
};
