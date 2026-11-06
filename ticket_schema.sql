-- ============================================================
-- 票根数据表（E：后端开发2 票根管理）
-- 数据库：InterestDB（SQL Server）
-- 命名规范：与现有表保持一致（复数、PascalCase）
-- 使用方式：在 InterestDB 中直接执行本文件建表
-- ============================================================

-- 删除旧表（仅在需要重建时执行，会丢失已有数据）
IF OBJECT_ID('dbo.Tickets', 'U') IS NOT NULL DROP TABLE dbo.Tickets;

-- 票根表：一条记录对应一张文娱票根（演唱会/电影/展览等）
CREATE TABLE dbo.Tickets (
    TicketId   INT IDENTITY(1,1) PRIMARY KEY,     -- 票根ID，自增主键
    UserId     INT NOT NULL,                      -- 所属用户ID，关联 Users 表
    Title      NVARCHAR(100) NOT NULL,            -- 票根标题（必填）
    Memo       NVARCHAR(500) NULL,                -- 备注/回忆文字
    CreateTime DATETIME NOT NULL DEFAULT GETDATE(), -- 创建时间，默认当前时间
    CONSTRAINT FK_Tickets_Users FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId)
);
