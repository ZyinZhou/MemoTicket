-- ============================================================
-- 票根接口测试数据（E：后端开发2 票根管理）
-- 使用方式：先在 InterestDB 中执行 ticket_schema.sql 建表，
--           再执行本文件插入测试数据，之后用 Postman 调用接口验证
-- 注意：UserId、InterestId 需改为实际存在的ID（可查 Users、Interests 表）
--       重复执行会产生重复记录，需先清理 Tickets、TicketInterests
-- ============================================================

-- 测试票根1：电影，字段齐全，关联两个兴趣
INSERT INTO dbo.Tickets (UserId, Title, Type, Rating, Memo, EventDate, Venue)
VALUES (1, N'电影《奥本海默》IMAX', N'电影', 5, N'音效震撼，值得二刷', '2026-09-15', N'万达影城');

-- 测试票根2：剧本杀，无关联兴趣
INSERT INTO dbo.Tickets (UserId, Title, Type, Rating, Memo, EventDate, Venue)
VALUES (1, N'剧本杀《青川怪谈》', N'剧本杀', 4, N'推理节奏紧凑', '2026-10-05', N'迷之屋体验馆');

-- 测试票根3：类型、评分、日期、地点、笔记均缺省，验证可空字段
INSERT INTO dbo.Tickets (UserId, Title)
VALUES (2, N'故宫博物院特展');

-- 票根兴趣关联（票根1 关联两个兴趣；票根3 关联一个兴趣）
INSERT INTO dbo.TicketInterests (TicketId, InterestId) VALUES (1, 1);
INSERT INTO dbo.TicketInterests (TicketId, InterestId) VALUES (1, 2);
INSERT INTO dbo.TicketInterests (TicketId, InterestId) VALUES (3, 1);

-- 接口测试示例（Postman，请求头均需 Authorization: Bearer <登录接口返回的token>）
-- 1) 创建 POST http://127.0.0.1:5000/api/tickets
-- {
--   "title": "测试票根",
--   "type": "电影",
--   "rating": 5,
--   "content": "接口测试",
--   "event_date": "2026-11-20",
--   "venue": "测试场馆",
--   "interests": [1, 2]
-- }
-- 2) 列表 GET http://127.0.0.1:5000/api/tickets
-- 3) 详情 GET http://127.0.0.1:5000/api/tickets/1
-- 4) 修改 PUT http://127.0.0.1:5000/api/tickets/1
-- {
--   "title": "电影《奥本海默》IMAX",
--   "type": "电影",
--   "rating": 4,
--   "content": "重看一遍，依然推荐",
--   "interests": [2]
-- }
-- 5) 删除 DELETE http://127.0.0.1:5000/api/tickets/1
