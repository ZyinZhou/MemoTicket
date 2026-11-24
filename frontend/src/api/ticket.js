// JavaScript source code
import request from '../utils/request'

export const getTicketListApi = (params) => request.get('/api/tickets', { params })
export const getTicketDetailApi = (id) => request.get(`/api/tickets/${id}`)
export const createTicketApi = (data) => request.post('/api/tickets', data)
export const updateTicketApi = (id, data) => request.put(`/api/tickets/${id}`, data)
export const deleteTicketApi = (id) => request.delete(`/api/tickets/${id}`)