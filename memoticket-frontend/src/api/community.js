// ============================================================
// 社区 · 体验分享 API
// ------------------------------------------------------------
// COMMUNITY_DEMO_MODE = true 时使用 src/mock/community.js 中的
// 本地演示数据（数据存在 localStorage，刷新后仍在），后端接口
// 就绪后改成 false 即切换到真实请求，页面代码无需改动。
//
// 约定的后端接口：
//   GET  /api/community/overview          社区首页聚合数据
//        -> { code, data: { stats, interests, hot } }
//   GET  /api/community/feed             动态列表
//        参数: interestId, sort(latest|hot), keyword, page, pageSize
//        -> { code, data: { list, total, page, pageSize } }
//   GET  /api/community/shares/:id       分享详情
//   POST /api/community/shares           发布分享
//        body: { title, content, interestId, ticketId, rating, tags, images }
//   POST /api/community/shares/:id/like      点赞 / 取消点赞
//   POST /api/community/shares/:id/favorite  收藏 / 取消收藏
//   GET  /api/community/shares/:id/comments  评论列表
//   POST /api/community/shares/:id/comments  发表评论 { content }
// ============================================================

import request from '../utils/request'
import { getInterestListApi } from './interest'
import { getTicketListApi } from './ticket'
import {
  DEMO_INTERESTS,
  DEMO_TICKETS,
  demoOverview,
  demoFeed,
  demoShareDetail,
  demoCreateShare,
  demoToggleLike,
  demoToggleFavorite,
  demoComments,
  demoAddComment
} from '../mock/community'

// 演示开关：后端社区接口就绪后改为 false
export const COMMUNITY_DEMO_MODE = true

const delay = (data, ms = 220) =>
  new Promise((resolve) => {
    // 深拷贝：模拟网络序列化，避免页面直接持有演示数据的引用
    const payload = data === undefined || data === null ? data : JSON.parse(JSON.stringify(data))
    setTimeout(() => resolve({ code: 200, msg: 'ok', data: payload }), ms)
  })

// 首页聚合数据：统计 + 兴趣分类 + 热门分享
export const getCommunityOverviewApi = () => {
  if (COMMUNITY_DEMO_MODE) return delay(demoOverview())
  return request.get('/api/community/overview')
}

// 动态列表
export const getFeedListApi = (params = {}) => {
  if (COMMUNITY_DEMO_MODE) return delay(demoFeed(params))
  return request.get('/api/community/feed', { params })
}

// 分享详情
export const getShareDetailApi = (id) => {
  if (COMMUNITY_DEMO_MODE) return delay(demoShareDetail(id))
  return request.get(`/api/community/shares/${id}`)
}

// 发布分享
export const createShareApi = (payload) => {
  if (COMMUNITY_DEMO_MODE) return delay(demoCreateShare(payload), 420)
  return request.post('/api/community/shares', payload)
}

// 点赞 / 取消点赞
export const toggleShareLikeApi = (id) => {
  if (COMMUNITY_DEMO_MODE) return delay(demoToggleLike(id), 120)
  return request.post(`/api/community/shares/${id}/like`)
}

// 收藏 / 取消收藏
export const toggleShareFavoriteApi = (id) => {
  if (COMMUNITY_DEMO_MODE) return delay(demoToggleFavorite(id), 120)
  return request.post(`/api/community/shares/${id}/favorite`)
}

// 评论列表
export const getCommentListApi = (id) => {
  if (COMMUNITY_DEMO_MODE) return delay(demoComments(id))
  return request.get(`/api/community/shares/${id}/comments`)
}

// 发表评论
export const createCommentApi = (id, content) => {
  if (COMMUNITY_DEMO_MODE) return delay(demoAddComment(id, content), 260)
  return request.post(`/api/community/shares/${id}/comments`, { content })
}

// 兴趣分类（发布页下拉框复用兴趣接口）
export const getCommunityInterestsApi = () => {
  if (COMMUNITY_DEMO_MODE) return delay(DEMO_INTERESTS)
  return getInterestListApi()
}

// 可关联的票根（发布页下拉框复用票夹接口）
export const getShareableTicketsApi = () => {
  if (COMMUNITY_DEMO_MODE) return delay(DEMO_TICKETS)
  return getTicketListApi()
}
