\# MemoTicket Beta 阶段接口规范



\## 1. 通用约定



\- 服务地址：`http://127.0.0.1:5000`

\- 成功响应格式：`{"code": 200, "msg": "查询成功", "data": ...}`

\- 需要登录的接口在请求头传递：`Authorization: Bearer <token>`

\- 新增 Beta 接口的字段使用 camelCase；不修改 Alpha 已存在接口的字段命名。



\## 2. 按兴趣查询社区动态



\- 请求方式：`GET`

\- 请求路径：`/api/community-posts`

\- 鉴权：当前为公共浏览接口，无需登录。

\- 用途：获取指定兴趣下的社区动态，按创建时间倒序排列。



\### 查询参数



| 参数 | 类型 | 必填 | 说明 |

| --- | --- | --- | --- |

| `interestId` | integer | 是 | 兴趣编号，必须为正整数 |



\### 成功响应示例



```json

{

&#x20; "code": 200,

&#x20; "msg": "查询成功",

&#x20; "data": \[

&#x20;   {

&#x20;     "id": 2,

&#x20;     "userId": 1,

&#x20;     "authorName": "ZyinChou",

&#x20;     "interestId": 1,

&#x20;     "content": "动态内容",

&#x20;     "createTime": "2026-11-24 12:33:23.160000",

&#x20;     "updateTime": null,

&#x20;     "ticket": null

&#x20;   }

&#x20; ]

}
```

### `ticket` 字段

`ticket` 为可空对象：

- 未关联票根时为 `null`。
- 关联票根时返回 `id`、`title`、`type`、`eventDate`、`venue`。
- 若关联票根后来被删除，数据库将关联设为 `NULL`，动态仍保留。

### 错误响应

| 场景 | HTTP 状态码 | `code` | `msg` |
| --- | ---: | ---: | --- |
| 缺少或非法 `interestId` | 400 | 400 | 兴趣ID必须为正整数或缺少参数提示 |
| 兴趣不存在 | 404 | 404 | 兴趣不存在 |
| 数据库或服务器异常 | 500 | 500 | 错误信息 |

## 3. 数据关联规则

- `CommunityPosts.InterestId` 必填，外键关联 `Interests.InterestId`。
- `CommunityPosts.UserId` 必填，外键关联 `Users.UserId`。
- `CommunityPosts.TicketId` 可空，外键关联 `Tickets.TicketId`。
- 删除票根时使用 `ON DELETE SET NULL`，不会删除已发布的社区动态。
- 社区查询使用索引 `IX_CommunityPosts_InterestId_CreateTime`，以支持按兴趣、按时间倒序读取。

