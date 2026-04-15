import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, 
})

// Конференции
export const konferentsiyaAPI = {
  getAll: () => api.get('/konferentsiyas/'),
  getById: (id) => api.get(`/konferentsiyas/${id}/`),
  create: (data) => api.post('/konferentsiyas/', data),
  update: (id, data) => api.put(`/konferentsiyas/${id}/`, data),
  delete: (id) => api.delete(`/konferentsiyas/${id}/`),
}

// Участники
export const uchastnikAPI = {
  getAll: (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return api.get(`/uchastniks/${queryString ? '?' + queryString : ''}`)
  },
  getById: (id) => api.get(`/uchastniks/${id}/`),
  create: (data) => api.post('/uchastniks/', data),
  update: (id, data) => api.put(`/uchastniks/${id}/`, data),
  delete: (id) => api.delete(`/uchastniks/${id}/`),
}

// Проживание
export const prozhivanieAPI = {
  getAll: () => api.get('/prozhivanies/'),
  getById: (id) => api.get(`/prozhivanies/${id}/`),
  create: (data) => api.post('/prozhivanies/', data),
  update: (id, data) => api.put(`/prozhivanies/${id}/`, data),
  delete: (id) => api.delete(`/prozhivanies/${id}/`),
}

// Секции
export const sekciyaAPI = {
  getAll: (konferentsiyaId = null) => {
    const url = konferentsiyaId ? `/sekciyas/?konferentsiya=${konferentsiyaId}` : '/sekciyas/'
    return api.get(url)
  },
  getById: (id) => api.get(`/sekciyas/${id}/`),
  create: (data) => api.post('/sekciyas/', data),
  update: (id, data) => api.put(`/sekciyas/${id}/`, data),
  delete: (id) => api.delete(`/sekciyas/${id}/`),
}

// Трансфер
export const transferAPI = {
  getAll: () => api.get('/transfers/'),
  getById: (id) => api.get(`/transfers/${id}/`),
  create: (data) => api.post('/transfers/', data),
  update: (id, data) => api.put(`/transfers/${id}/`, data),
  delete: (id) => api.delete(`/transfers/${id}/`),
}

// Доклады
export const dokladAPI = {
  getAll: () => api.get('/doklads/'),
  
  getById: (id) => api.get(`/doklads/${id}/`),
  
  create: (data, file = null) => {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    if (file) {
      formData.append('file', file)
    }
    return api.post('/doklads/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  update: (id, data, file = null) => {
    const formData = new FormData()
    Object.keys(data).forEach(key => {
      if (data[key] !== null && data[key] !== undefined) {
        formData.append(key, data[key])
      }
    })
    if (file) {
      formData.append('file', file)
    }
    return api.patch(`/doklads/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  delete: (id) => api.delete(`/doklads/${id}/`)
}

// Отказы
export const otkazAPI = {
  getAll: () => api.get('/otkazs/'),
  getById: (id) => api.get(`/otkazs/${id}/`),
  create: (data) => api.post('/otkazs/', data),
  update: (id, data) => api.put(`/otkazs/${id}/`, data),
  delete: (id) => api.delete(`/otkazs/${id}/`),
}

// Программа мероприятия
export const programmaAPI = {
  getAll: () => api.get('/programmas/'),
  getById: (id) => api.get(`/programmas/${id}/`),
  create: (data) => api.post('/programmas/', data),
  update: (id, data) => api.put(`/programmas/${id}/`, data),
  delete: (id) => api.delete(`/programmas/${id}/`),
}

// Контейнер программ
export const programAPI = {
  getAll: () => api.get('/programs/'),
  getById: (id) => api.get(`/programs/${id}/`),
  create: (data) => api.post('/programs/', data),
  update: (id, data) => api.put(`/programs/${id}/`, data),
  delete: (id) => api.delete(`/programs/${id}/`),
}

// Импорт из Excel
export const importAPI = {
  participants: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import/participants/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
}

// Расселение и Логистика
export const settlementAPI = {
  // Проживание
  getAvailable: (konferentsiyaId) => 
    api.get(`/settlement/available/?konferentsiya=${konferentsiyaId}`),
  getAccommodations: (konferentsiyaId) => 
    api.get(`/settlement/accommodations/?konferentsiya=${konferentsiyaId}`),
  settle: (data) => api.post('/settlement/settle/', data),
  vacate: (data) => api.post('/settlement/vacate/', data),

  getTransfersAvailable: (konferentsiyaId) => 
    api.get(`/settlement/transfers_available/?konferentsiya=${konferentsiyaId}`),
  getTransfersAssigned: (konferentsiyaId) => 
    api.get(`/settlement/transfers_assigned/?konferentsiya=${konferentsiyaId}`),
  assignTransfer: (data) => api.post('/settlement/assign_transfer/', data),
  unassignTransfer: (data) => api.post('/settlement/unassign_transfer/', data),
}

export default api