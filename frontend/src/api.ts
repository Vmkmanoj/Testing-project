import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default api;

// ── Auth ──
export const authApi = {
  login: (data: { email: string; password: string }) => api.post('/auth/login', data),
  register: (data: object) => api.post('/auth/register', data),
  me: () => api.get('/employees/me'),
};

// ── Employees ──
export const employeeApi = {
  getAll: () => api.get('/employees/'),
  getManagers: () => api.get('/employees/managers'),
  getById: (id: string) => api.get(`/employees/${id}`),
  update: (id: string, data: object) => api.patch(`/employees/${id}`, data),
  delete: (id: string) => api.delete(`/employees/${id}`),
};

// ── Clients ──
export const clientApi = {
  getAll: () => api.get('/clients/'),
  getById: (id: string) => api.get(`/clients/${id}`),
  create: (data: object) => api.post('/clients/', data),
  update: (id: string, data: object) => api.patch(`/clients/${id}`, data),
  delete: (id: string) => api.delete(`/clients/${id}`),
};

// ── Projects ──
export const projectApi = {
  create: (data: object) => api.post('/project/create', data),
  createTeam: (data: object) => api.post('/project/team', data),
  getAll: () => api.get('/project/projects'),
};

// ── Teams ──
export const teamApi = {
  assign: (data: object) => api.post('/assign/team', data),
  getAll: () => api.get('/project/teams'),
};

// ── Leave Types ──
export const leaveTypeApi = {
  getAll: () => api.get('/leave-types/'),
  getById: (id: string) => api.get(`/leave-types/${id}`),
  create: (data: object) => api.post('/leave-types/', data),
  update: (id: string, data: object) => api.patch(`/leave-types/${id}`, data),
  delete: (id: string) => api.delete(`/leave-types/${id}`),
};

// ── Leave Balances ──
export const leaveBalanceApi = {
  getMy: () => api.get('/leave-balances/me'),
  create: (data: object) => api.post('/leave-balances/', data),
};

// ── Leave Requests ──
export const leaveRequestApi = {
  create: (data: object) => api.post('/leave-requests/', data),
  getMy: (page: number = 1, limit: number = 10) => api.get(`/leave-requests/me?page=${page}&limit=${limit}`),
  getAll: (page: number = 1, limit: number = 10) => api.get(`/leave-requests/?page=${page}&limit=${limit}`),
  action: (id: string, data: { action: string; comment?: string }) =>
    api.patch(`/leave-requests/${id}/action`, data),
};

// ── AI Agent ──
export const agentApi = {
  chat: (data: { message: string; history: { role: string; content: string }[] }) =>
    api.post('/agent/chat', data),
    uploadPdf: (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      return api.post('/agent/upload-pdf', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    },
    getPolicies: () => api.get('/agent/policies'),
    deletePolicy: (id: string) => api.delete(`/agent/policies/${id}`),
  };

