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
