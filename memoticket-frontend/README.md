# MemoTicket 前端

记录并分享每一次值得回忆的体验：兴趣社区、体验分享、票根管理。

技术栈：Vue 3（`<script setup>`）+ Vite + Vue Router + Element Plus + Axios。

## 启动

```bash
npm install
npm run dev      # 开发环境，默认 http://localhost:5173
npm run build    # 生产构建
```

后端默认地址为 `http://127.0.0.1:5000`，可在 `src/utils/request.js` 中调整。

## 社区与分享模块

| 路由 | 说明 | 登录 |
| --- | --- | --- |
| `/community` | 兴趣社区首页：数据概览、兴趣分类、热门分享、社区公约 | 否 |
| `/community/feed` | 社区动态列表：关键词搜索、兴趣筛选、最新/最热排序、分页 | 否 |
| `/share/create` | 发布体验分享：表单校验 + 实时预览 | 是 |
| `/share/:id` | 分享详情：正文、关联票根、点赞/收藏、评论 | 否（互动需登录） |
| `/interests` | 旧入口，重定向到 `/community` | 否 |

相关文件：

```
src/api/community.js               社区接口封装（含演示模式开关）
src/mock/community.js              本地演示数据（localStorage 持久化）
src/components/CommunityPage.vue   社区公共布局与导航
src/components/ShareCard.vue       动态卡片（列表与预览复用）
src/views/CommunityHome.vue        兴趣社区首页
src/views/CommunityFeed.vue        社区动态列表
src/views/ShareCreate.vue          发布体验分享
src/views/ShareDetail.vue          分享详情
src/utils/format.js                相对时间与摘要格式化
```

### 演示模式（后端接口未就绪时）

`src/api/community.js` 中的 `COMMUNITY_DEMO_MODE = true` 会使用本地演示数据，
无需后端即可完整浏览、点赞、评论、发布，发布后的内容在刷新后仍然保留。

- 演示数据存于 `localStorage` 的 `memoticket_community_demo_v2`，清空该键可重置；
- 后端社区接口就绪后，把开关改为 `false`，即可切换到真实请求，页面代码无需改动。

### 后端接口约定

演示模式封装了以下接口，返回结构统一为 `{ code: 200, msg, data }`：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/community/overview` | 首页聚合：`{ stats, interests, hot }` |
| GET | `/api/community/feed` | 动态列表，参数 `interestId`、`sort=latest｜hot`、`keyword`、`page`、`pageSize`，返回 `{ list, total, page, pageSize }` |
| GET | `/api/community/shares/:id` | 分享详情 |
| POST | `/api/community/shares` | 发布分享：`{ title, content, interestId, ticketId, rating, tags, images }` |
| POST | `/api/community/shares/:id/like` | 点赞 / 取消点赞 |
| POST | `/api/community/shares/:id/favorite` | 收藏 / 取消收藏 |
| GET | `/api/community/shares/:id/comments` | 评论列表 |
| POST | `/api/community/shares/:id/comments` | 发表评论：`{ content }` |

动态对象字段：`id`、`title`、`content`、`author{id,nickname,color}`、`interestId`、`interestName`、
`rating`、`tags`、`images`、`ticket{id,title,type,eventDate,venue}`、`likeCount`、`favoriteCount`、
`commentCount`、`liked`、`favorited`、`createTime`。

### 登录与回跳

`/share/create` 等需要登录的页面由路由守卫拦截，跳转登录页时带上 `redirect` 参数，
登录成功后自动回到原页面（`src/router/index.js`、`src/views/Login.vue`）。
