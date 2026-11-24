# 兴趣分享平台 API 接口文档

## 通用说明
- 基础地址: `http://127.0.0.1:5000`
- 需要登录的接口，必须在请求头（Headers）中携带：`Authorization: Bearer <token>`
- 返回格式均为 JSON，包含 `code` (200为成功), `msg` (提示), `data` (数据)

## 1. 用户认证
- **注册**：`POST /api/register`
  参数：`{"username": "xxx", "password": "xxx", "interests": [1, 2]}` (interests选填)
- **登录**：`POST /api/login`
  参数：`{"username": "xxx", "password": "xxx"}`
  返回：包含 `token`
- **退出**：`POST /api/logout` (需认证)

## 2. 用户信息
- **获取个人信息**：`GET /api/user/profile` (需认证)
- **修改个人信息**：`PUT /api/user/profile` (需认证)
  参数：`{"nickname": "昵称", "avatar_url": "头像链接", "bio": "签名"}`

## 3. 兴趣模块
- **获取预设兴趣**：`GET /api/interests`
- **搜索兴趣**：`GET /api/interests/search?q=关键字`
- **创建自定义兴趣**：`POST /api/interests` (需认证) 参数：`{"name": "新兴趣"}`
- **加入兴趣**：`POST /api/interests/{id}/join` (需认证)
- **退出兴趣**：`DELETE /api/interests/{id}/quit` (需认证)

## 4. 分享模块
- **发布分享/推荐/避雷**：`POST /api/shares` (需认证)
  参数：`{"title": "标题", "content": "内容", "interest_id": 1, "share_type": 1, "rating": {"target_name": "对象", "score": 5}}` 
  *(注：share_type 0=体验, 1=推荐, 2=避雷)*
- **分享列表**：`GET /api/shares?page=1&page_size=10&share_type=1` (无需认证也可看)