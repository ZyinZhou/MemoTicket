// JavaScript source code
import request from '../utils/request'

export const loginApi = (data) => request.post('/api/login', data)
export const registerApi = (data) => request.post('/api/register', data)
export const getUserInfoApi = () => request.get('/api/user/profile')
export const updateUserInfoApi = (data) => request.put('/api/user/profile', data)