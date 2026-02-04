import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// ========== BOOKINGS ==========
export const bookingsAPI = {
  getAll: (params = {}) => api.get('/bookings', { params }),
  getById: (id) => api.get(`/bookings/${id}`),
  create: (data) => api.post('/bookings', data),
  update: (id, data) => api.put(`/bookings/${id}`, data),
  delete: (id) => api.delete(`/bookings/${id}`),
  getUpcoming: (params = {}) => api.get('/bookings/upcoming', { params }),
};

// ========== CALENDAR ==========
export const calendarAPI = {
  getEvents: (params) => api.get('/calendar/events', { params }),
  sync: () => api.post('/calendar/sync'),
  getSources: (propertyId) => api.get('/calendar/sources', { params: { property_id: propertyId } }),
};

// ========== CONFLICTS ==========
export const conflictsAPI = {
  getAll: (params) => api.get('/conflicts', { params }),
  getSummary: (propertyId) => api.get('/conflicts/summary', { params: { property_id: propertyId } }),
  resolve: (id, notes) => api.post(`/conflicts/${id}/resolve`, { resolution_notes: notes }),
  detect: (propertyId) => api.post('/conflicts/detect', null, { params: { property_id: propertyId } }),
};

// ========== STATISTICS ==========
export const statisticsAPI = {
  getDashboard: (propertyId) => api.get('/statistics/dashboard', { params: { property_id: propertyId } }),
  getOccupancy: (params) => api.get('/statistics/occupancy', { params }),
  getRevenue: (params) => api.get('/statistics/revenue', { params }),
  getPlatforms: (params) => api.get('/statistics/platforms', { params }),
};

// ========== SYNC ACTIONS ==========
export const syncActionsAPI = {
  getAll: (params) => api.get('/sync-actions', { params }),
  markDone: (id) => api.post(`/sync-actions/${id}/mark-done`),
  dismiss: (id) => api.post(`/sync-actions/${id}/dismiss`),
};

// ========== SYSTEM INFO ==========
export const systemAPI = {
  getInfo: () => api.get('/info'),
  getHealth: () => api.get('/health'),
};

// ========== SETTINGS (para futuro endpoint de configurações) ==========
export const settingsAPI = {
  // Placeholder para quando criarmos endpoints de configuração
  getAll: () => {
    // Por enquanto retorna dados do /api/info
    return systemAPI.getInfo();
  },
  update: (data) => {
    // TODO: Criar endpoint no backend para salvar configurações
    console.log('Settings update (placeholder):', data);
    return Promise.resolve({ data: { success: true } });
  },
};

export default api;
