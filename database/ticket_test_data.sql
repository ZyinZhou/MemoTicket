-- ============================================================
-- 票根接口测试数据（E：后端开发2 票根管理）
-- 使用方式：先在 InterestDB 中执行 ticket_schema.sql 建表，
--           再执行本文件插入测试数据，之后用 Postman 调用接口验证
-- 注意：UserId、InterestId 需改为实际存在的ID（可查 Users、Interests 表）
-- ============================================================

-- 测试票根1：演唱会（字段齐全）
INSERT INTO dbo.Tickets (UserId, Title, EventDate, Venue, Memo)
VALUES (1, N'五月天演唱会', '2026-10-01', N'国家体育场（鸟巢）', N'和同好一起看的，全程跟唱');

-- 测试票根2：电影（无关联兴趣）
INSERT INTO dbo.Tickets (UserId, Title, EventDate, Venue, Memo)
VALUES (1, N'《奥本海默》IMAX', '2026-09-15', N'万达影城', N'音效震撼，值得二刷');

-- 测试票根3：展览（日期、地点、描述缺省，验证可空字段）
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
--   "event_date": "2026-11-20",
--   "venue": "测试场馆",
--   "memo": "接口测试",
--   "interests": [1, 2]
-- }
-- 2) 列表 GET http://127.0.0.1:5000/api/tickets
-- 3) 详情 GET http://127.0.0.1:5000/api/tickets/1
-- 4) 修改 PUT http://127.0.0.1:5000/api/tickets/1
-- {
--   "title": "五月天演唱会（改）",
--   "event_date": "2026-10-01",
--   "venue": "国家体育场（鸟巢）",
--   "memo": "第一次看演唱会",
--   "interests": [2]
-- }
-- 5) 删除 DELETE http://127.0.0.1:5000/api/tickets/1
