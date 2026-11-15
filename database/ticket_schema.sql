USE InterestDB;
GO
-- ============================================================
-- 票根数据表（E：后端开发2 票根管理）
-- 数据库：InterestDB（SQL Server）
-- 命名规范：与现有表保持一致（复数、PascalCase）
-- 使用方式：在 InterestDB 中直接执行本文件，可重复执行
-- 前置条件：Users、Interests 表须已存在（外键引用 Users.UserId、Interests.InterestId）
-- 说明：表已存在时不重建，仅补充缺失列，不删除既有数据
-- ============================================================

-- 票根表：一条记录对应一张票根（电影/书籍/剧本杀/密室/旅游等）
-- 字段对应需求文档 3.7.2 数字票根实体，另含票根类型与评分
IF OBJECT_ID('dbo.Tickets', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.Tickets (
        TicketId   INT IDENTITY(1,1) PRIMARY KEY,      -- 票根编号，自增主键
        UserId     INT NOT NULL,                       -- 创建者，关联 Users 表
        Title      NVARCHAR(100) NOT NULL,             -- 票根名称（必填）
        Type       NVARCHAR(20) NULL,                  -- 票根类型：电影/书籍/剧本杀/密室/旅游
        Rating     TINYINT NULL,                       -- 评分，1-5 星
        Memo       NVARCHAR(500) NULL,                 -- 体验笔记，接口字段名为 content
        EventDate  DATE NULL,                          -- 活动日期
        Venue      NVARCHAR(100) NULL,                 -- 活动地点
        CreateTime DATETIME NOT NULL DEFAULT GETDATE(), -- 创建时间，默认当前时间
        CONSTRAINT FK_Tickets_Users FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId)
    );
END
GO

-- 已有库补列：Type、Rating 不存在时添加
IF COL_LENGTH('dbo.Tickets', 'Type') IS NULL
    ALTER TABLE dbo.Tickets ADD Type NVARCHAR(20) NULL;
GO
IF COL_LENGTH('dbo.Tickets', 'Rating') IS NULL
    ALTER TABLE dbo.Tickets ADD Rating TINYINT NULL;
GO

-- 票根兴趣关联表：对应需求文档 3.7.2 票根兴趣关联实体（票根编号、兴趣编号）
-- 复合主键保证同一票根与同一兴趣不会重复关联（3.7.3）
IF OBJECT_ID('dbo.TicketInterests', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.TicketInterests (
        TicketId   INT NOT NULL,                       -- 票根编号
        InterestId INT NOT NULL,                       -- 兴趣编号
        CONSTRAINT PK_TicketInterests PRIMARY KEY (TicketId, InterestId),
        CONSTRAINT FK_TicketInterests_Tickets   FOREIGN KEY (TicketId)   REFERENCES dbo.Tickets(TicketId),
        CONSTRAINT FK_TicketInterests_Interests FOREIGN KEY (InterestId) REFERENCES dbo.Interests(InterestId)
    );
END
GO
