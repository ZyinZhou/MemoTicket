-- ============================================================
-- 组队活动接口测试数据（E：后端开发2 组队活动管理）
-- 使用方式：先在 InterestDB 中执行 team_schema.sql 建表，
--           再执行本文件插入测试数据，之后用 Postman 调用接口验证
-- 注意：UserId 需改为实际存在的ID（可查 Users 表）
--       重复执行会产生重复记录，需先清理 TeamActivityApplications、TeamActivities
-- ============================================================

-- 测试活动1：字段齐全，发起人 UserId=1
INSERT INTO dbo.TeamActivities (UserId, Title, Description, EventDate, Venue, Capacity, Status)
VALUES (1, N'周末剧本杀组队', N'缺两位推理爱好者，新手友好', '2026-11-22', N'迷之屋体验馆', 4, N'招募中');

-- 测试活动2：仅标题与人数上限，验证可空字段
INSERT INTO dbo.TeamActivities (UserId, Title, Capacity)
VALUES (2, N'羽毛球约球', 6);

-- 报名记录：活动1 报名者 UserId=2；活动2 报名者 UserId=1
INSERT INTO dbo.TeamActivityApplications (ActivityId, UserId, Status)
VALUES (1, 2, N'待处理');
INSERT INTO dbo.TeamActivityApplications (ActivityId, UserId, Status)
VALUES (2, 1, N'待处理');

-- 接口测试示例（Postman）
-- 1) 创建 POST http://127.0.0.1:5000/api/activities
--    请求头：Authorization: Bearer <登录接口返回的token>
-- {
--   "title": "周末徒步组队",
--   "description": "环海岸线徒步，欢迎新手",
--   "event_date": "2026-11-29",
--   "venue": "石老人海滩",
--   "capacity": 5
-- }
-- 2) 列表 GET http://127.0.0.1:5000/api/activities
-- 3) 详情 GET http://127.0.0.1:5000/api/activities/1
