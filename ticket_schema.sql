-- ============================================================
-- 票根数据表（E：后端开发2 票根管理）
-- 数据库：InterestDB（SQL Server）
-- 命名规范：与现有表保持一致（复数、PascalCase）
-- 使用方式：在 InterestDB 中直接执行本文件建表
-- 前置条件：Users、Interests 表须已存在（两张表的建表脚本未随仓库提供，
--           字段以现有库为准，外键引用 Users.UserId、Interests.InterestId）
-- ============================================================

-- 删除旧表（仅在需要重建时执行，会丢失已有数据）
IF OBJECT_ID('dbo.TicketInterests', 'U') IS NOT NULL DROP TABLE dbo.TicketInterests;
IF OBJECT_ID('dbo.Tickets', 'U') IS NOT NULL DROP TABLE dbo.Tickets;

-- 票根表：一条记录对应一张文娱票根（演唱会/电影/展览等）
-- 字段对应需求文档 3.7.2 数字票根实体：票根编号、创建者、活动名称、日期、地点、描述
CREATE TABLE dbo.Tickets (
    TicketId   INT IDENTITY(1,1) PRIMARY KEY,     -- 票根编号，自增主键
    UserId     INT NOT NULL,                      -- 创建者，关联 Users 表
    Title      NVARCHAR(100) NOT NULL,            -- 活动名称（必填）
    EventDate  DATE NULL,                         -- 活动日期
    Venue      NVARCHAR(100) NULL,                -- 活动地点
    Memo       NVARCHAR(500) NULL,                -- 描述
    CreateTime DATETIME NOT NULL DEFAULT GETDATE(), -- 创建时间，默认当前时间
    CONSTRAINT FK_Tickets_Users FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId)
);

-- 票根兴趣关联表：对应需求文档 3.7.2 票根兴趣关联实体（票根编号、兴趣编号）
-- 复合主键保证同一票根与同一兴趣不会重复关联（3.7.3）
CREATE TABLE dbo.TicketInterests (
    TicketId   INT NOT NULL,                      -- 票根编号
    InterestId INT NOT NULL,                      -- 兴趣编号
    CONSTRAINT PK_TicketInterests PRIMARY KEY (TicketId, InterestId),
    CONSTRAINT FK_TicketInterests_Tickets   FOREIGN KEY (TicketId)   REFERENCES dbo.Tickets(TicketId),
    CONSTRAINT FK_TicketInterests_Interests FOREIGN KEY (InterestId) REFERENCES dbo.Interests(InterestId)
);
