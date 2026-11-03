-- ============================================================
-- 票根接口测试数据（E：后端开发2 票根管理）
-- 使用方式：先在 InterestDB 中执行 ticket_schema.sql 建表，
--           再执行本文件插入测试数据，之后用 Postman 调用创建票根接口验证
-- 注意：UserId 需改为实际存在的用户ID（可在 Users 表中查询）
-- ============================================================

-- 测试票根1：演唱会（含备注）
INSERT INTO dbo.Tickets (UserId, Title, Memo)
VALUES (1, N'五月天演唱会', N'和同好一起看的，全程跟唱');

-- 测试票根2：电影（无备注，验证可空字段）
INSERT INTO dbo.Tickets (UserId, Title)
VALUES (1, N'《奥本海默》IMAX');

-- 创建票根接口测试请求体示例（Postman 中 POST http://127.0.0.1:5000/api/tickets）
-- 请求头：Authorization: Bearer <登录接口返回的token>
-- {
--   "title": "测试票根",
--   "memo": "接口测试"
-- }
