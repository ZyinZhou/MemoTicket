# MemoTicket 后端接口文档 (Alpha 阶段)

**后端运行地址**：`http://127.0.0.1:5000`
*(注：已配置跨域 CORS，前端直接发 Axios 请求即可)*

---

## 1. 获取预设兴趣列表

* **请求方式**：GET
* **请求路径**：`/api/interests`
* **请求参数**：无

**返回成功示例：**

<pre><code>{
  "code": 200,
  "data": [
    {"id": 1, "name": "阅读"},
    {"id": 2, "name": "音乐"}
  ]
}</code></pre>

---

## 2. 用户注册

* **请求方式**：POST
* **请求路径**：`/api/register`
* **请求体 (JSON)**：

<pre><code>{
  "username": "zhangsan",
  "password": "123456",
  "interests": [1, 2]
}</code></pre>

*(注：`interests` 为用户勾选的兴趣ID数组，如果没有选传 `[]`)*

**返回成功示例：**

<pre><code>{ "code": 200, "msg": "注册成功" }</code></pre>

**返回失败示例：**

<pre><code>{ "code": 400, "msg": "用户名已存在" }</code></pre>

---

## 3. 用户登录

* **请求方式**：POST
* **请求路径**：`/api/login`
* **请求体 (JSON)**：

<pre><code>{
  "username": "zhangsan",
  "password": "123456"
}</code></pre>

**返回成功示例：**

<pre><code>{
  "code": 200,
  "msg": "登录成功",
  "user_id": 1,
  "token": "eyJ1c2VyX2lkIjoxfQ..."
}</code></pre>

*(注：前端拿到 `token` 后请存入 `localStorage`，供路由守卫使用)*

**返回失败示例：**

<pre><code>{ "code": 400, "msg": "用户名或密码错误" }</code></pre>

---

## 4. 创建票根

* **请求方式**：POST
* **请求路径**：`/api/tickets`
* **请求头**：`Authorization: Bearer <token>`（登录接口返回的 token）
* **请求体 (JSON)**：

<pre><code>{
  "title": "电影《奥本海默》",
  "type": "电影",
  "rating": 5,
  "content": "音效震撼，值得二刷",
  "event_date": "2026-09-15",
  "venue": "万达影城",
  "interests": [1, 2]
}</code></pre>

*(注：`title` 必填，不超过 100 字；`type` 可选，取值限 电影/书籍/剧本杀/密室/旅游；`rating` 可选，1-5 整数；`content` 可选，体验笔记，不超过 500 字，兼容入参 `memo`；`event_date` 可选，格式 `YYYY-MM-DD`；`venue` 可选，不超过 100 字；`interests` 可选，兴趣ID数组)*

**返回成功示例：**

<pre><code>{
  "code": 200,
  "msg": "创建成功",
  "data": {
    "id": 1,
    "createTime": "2026-11-15 10:00:00"
  }
}</code></pre>

**返回失败示例：**

<pre><code>{ "code": 400, "msg": "票根标题不能为空" }</code></pre>

<pre><code>{ "code": 400, "msg": "票根类型只能为：电影、书籍、剧本杀、密室、旅游" }</code></pre>

<pre><code>{ "code": 400, "msg": "评分必须为1-5的整数" }</code></pre>

<pre><code>{ "code": 401, "msg": "未登录或登录已过期" }</code></pre>

---

## 5. 查询个人票根列表

* **请求方式**：GET
* **请求路径**：`/api/tickets`
* **请求头**：`Authorization: Bearer <token>`
* **请求参数**：无
* **说明**：返回当前用户创建的全部票根，按创建时间倒序；字段名与前端列表页一致

**返回成功示例：**

<pre><code>{
  "code": 200,
  "msg": "查询成功",
  "data": [
    {
      "id": 1,
      "userId": 1,
      "title": "电影《奥本海默》",
      "type": "电影",
      "rating": 5,
      "content": "音效震撼，值得二刷",
      "eventDate": "2026-09-15",
      "venue": "万达影城",
      "createTime": "2026-11-15 10:00:00",
      "interests": [1, 2]
    }
  ]
}</code></pre>

**返回失败示例：**

<pre><code>{ "code": 401, "msg": "未登录或登录已过期" }</code></pre>

---

## 6. 查询票根详情

* **请求方式**：GET
* **请求路径**：`/api/tickets/{id}`
* **请求头**：`Authorization: Bearer <token>`
* **说明**：仅票根创建者可查看

**返回成功示例：**

<pre><code>{
  "code": 200,
  "msg": "查询成功",
  "data": {
    "id": 1,
    "userId": 1,
    "title": "电影《奥本海默》",
    "type": "电影",
    "rating": 5,
    "content": "音效震撼，值得二刷",
    "eventDate": "2026-09-15",
    "venue": "万达影城",
    "createTime": "2026-11-15 10:00:00",
    "interests": [1, 2]
  }
}</code></pre>

**返回失败示例：**

<pre><code>{ "code": 401, "msg": "未登录或登录已过期" }</code></pre>

<pre><code>{ "code": 403, "msg": "无权操作该票根" }</code></pre>

<pre><code>{ "code": 404, "msg": "票根不存在" }</code></pre>

---

## 7. 修改票根

* **请求方式**：PUT
* **请求路径**：`/api/tickets/{id}`
* **请求头**：`Authorization: Bearer <token>`
* **请求体 (JSON)**：

<pre><code>{
  "title": "电影《奥本海默》",
  "type": "电影",
  "rating": 4,
  "content": "重看一遍，依然推荐",
  "interests": [2]
}</code></pre>

*(注：未提交的字段沿用原票根的值；`interests` 传入时整体替换原有兴趣关联，不传则保持不变；仅票根创建者可修改)*

**返回成功示例：**

<pre><code>{ "code": 200, "msg": "修改成功" }</code></pre>

**返回失败示例：**

<pre><code>{ "code": 400, "msg": "日期格式应为 YYYY-MM-DD" }</code></pre>

<pre><code>{ "code": 403, "msg": "无权操作该票根" }</code></pre>

<pre><code>{ "code": 404, "msg": "票根不存在" }</code></pre>

---

## 8. 删除票根

* **请求方式**：DELETE
* **请求路径**：`/api/tickets/{id}`
* **请求头**：`Authorization: Bearer <token>`
* **说明**：仅票根创建者可删除，删除时同步清理其兴趣关联记录

**返回成功示例：**

<pre><code>{ "code": 200, "msg": "删除成功" }</code></pre>

**返回失败示例：**

<pre><code>{ "code": 401, "msg": "未登录或登录已过期" }</code></pre>

<pre><code>{ "code": 403, "msg": "无权操作该票根" }</code></pre>

<pre><code>{ "code": 404, "msg": "票根不存在" }</code></pre>

---

## 9. 创建组队活动

* **请求方式**：POST
* **请求路径**：`/api/activities`
* **请求头**：`Authorization: Bearer <token>`（仅登录用户可创建）
* **请求体 (JSON)**：

<pre><code>{
  "title": "周末剧本杀组队",
  "description": "缺两位推理爱好者，新手友好",
  "event_date": "2026-11-22",
  "venue": "迷之屋体验馆",
  "capacity": 4
}</code></pre>

*(注：`title` 必填，不超过 100 字；`description` 可选，不超过 500 字；`event_date` 可选，格式 `YYYY-MM-DD`，兼容入参 `eventDate`；`venue` 可选，不超过 100 字；`capacity` 必填，正整数)*

**返回成功示例：**

<pre><code>{
  "code": 200,
  "msg": "创建成功",
  "data": {
    "id": 1,
    "createTime": "2026-11-18 10:00:00"
  }
}</code></pre>

**返回失败示例：**

<pre><code>{ "code": 400, "msg": "活动标题不能为空" }</code></pre>

<pre><code>{ "code": 400, "msg": "人数上限必须为正整数" }</code></pre>

<pre><code>{ "code": 401, "msg": "未登录或登录已过期" }</code></pre>

---

## 10. 组队活动列表

* **请求方式**：GET
* **请求路径**：`/api/activities`
* **请求参数**：无
* **说明**：可匿名浏览；返回全部活动，附带报名人数；有活动时间的按时间升序，同日按创建时间倒序，无活动时间的排在最后

**返回字段说明：**

| 字段 | 类型 | 说明 |
|---|---|---|
| id | 整数 | 活动编号 |
| userId | 整数 | 发起人 ID |
| title | 字符串 | 活动标题 |
| description | 字符串/null | 活动描述 |
| eventDate | 字符串/null | 活动时间 |
| venue | 字符串/null | 活动地点 |
| capacity | 整数 | 人数上限 |
| status | 字符串 | 活动状态：招募中 / 已关闭 |
| signupCount | 整数 | 当前报名人数 |
| createTime | 字符串 | 创建时间 |

*(注：`signupCount` 统计申请表全部记录；后续接入申请审批流后按审批状态统计)*

**返回成功示例：**

<pre><code>{
  "code": 200,
  "msg": "查询成功",
  "data": [
    {
      "id": 1,
      "userId": 1,
      "title": "周末剧本杀组队",
      "description": "缺两位推理爱好者，新手友好",
      "eventDate": "2026-11-22",
      "venue": "迷之屋体验馆",
      "capacity": 4,
      "status": "招募中",
      "signupCount": 1,
      "createTime": "2026-11-18 10:00:00"
    }
  ]
}</code></pre>

---

## 11. 组队活动详情

* **请求方式**：GET
* **请求路径**：`/api/activities/{id}`
* **说明**：可匿名浏览，返回活动完整信息与当前报名人数

**返回成功示例：**

<pre><code>{
  "code": 200,
  "msg": "查询成功",
  "data": {
    "id": 1,
    "userId": 1,
    "title": "周末剧本杀组队",
    "description": "缺两位推理爱好者，新手友好",
    "eventDate": "2026-11-22",
    "venue": "迷之屋体验馆",
    "capacity": 4,
    "status": "招募中",
    "signupCount": 1,
    "createTime": "2026-11-18 10:00:00"
  }
}</code></pre>

**返回失败示例：**

<pre><code>{ "code": 404, "msg": "活动不存在" }</code></pre>
