import request from '../utils/request'

// 获取兴趣列表
export const getInterestListApi = () => {
  return request.get('/api/interests')
}