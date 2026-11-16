import request from '../utils/request'

// 获取兴趣列表
export const getInterestListApi = () => {
  return request.get('/api/interests')
}

export const createInterestApi = name => request.post('/api/interests', { name })
export const updateInterestApi = (id, name) => request.put(`/api/interests/${id}`, { name })
export const deleteInterestApi = id => request.delete(`/api/interests/${id}`)
