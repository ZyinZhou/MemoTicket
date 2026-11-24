USE InterestDB;
GO
-- ============================================================
-- 组队活动数据表（E：后端开发2 组队活动管理）
-- 数据库：InterestDB（SQL Server）
-- 命名规范：与现有表保持一致（复数、PascalCase）
-- 使用方式：在 InterestDB 中直接执行本文件，可重复执行
-- 前置条件：Users 表须已存在（外键引用 Users.UserId）
-- 说明：表已存在时不重建，不删除既有数据
-- ============================================================

-- 组队活动表：一条记录对应一个组队活动
IF OBJECT_ID('dbo.TeamActivities', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.TeamActivities (
        ActivityId   INT IDENTITY(1,1) PRIMARY KEY,      -- 活动编号，自增主键
        UserId       INT NOT NULL,                       -- 发起人，关联 Users 表
        Title        NVARCHAR(100) NOT NULL,             -- 活动标题（必填）
        Description  NVARCHAR(500) NULL,                  -- 活动描述
        EventDate    DATE NULL,                           -- 活动时间
        Venue        NVARCHAR(100) NULL,                  -- 活动地点
        Capacity     INT NOT NULL,                        -- 人数上限，正整数
        Status       NVARCHAR(20) NOT NULL
                     CONSTRAINT DF_TeamActivities_Status DEFAULT (N'招募中'),  -- 活动状态
        CreateTime   DATETIME NOT NULL DEFAULT GETDATE(), -- 创建时间，默认当前时间
        CONSTRAINT FK_TeamActivities_Users
            FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId),
        CONSTRAINT CK_TeamActivities_Capacity CHECK (Capacity > 0)
    );
END
GO

-- 组队申请表：记录活动与报名用户的关系，同一用户不能重复报名同一活动
IF OBJECT_ID('dbo.TeamActivityApplications', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.TeamActivityApplications (
        ApplicationId INT IDENTITY(1,1) PRIMARY KEY,  -- 申请编号，自增主键
        ActivityId    INT NOT NULL,                   -- 活动编号
        UserId        INT NOT NULL,                   -- 申请者
        Status        NVARCHAR(20) NOT NULL
                      CONSTRAINT DF_TeamActivityApplications_Status DEFAULT (N'待处理'),  -- 申请状态
        CreateTime    DATETIME NOT NULL DEFAULT GETDATE(),  -- 申请时间
        CONSTRAINT UQ_TeamActivityApplications_Activity_User
            UNIQUE (ActivityId, UserId),
        CONSTRAINT FK_TeamActivityApplications_Activities
            FOREIGN KEY (ActivityId) REFERENCES dbo.TeamActivities(ActivityId),
        CONSTRAINT FK_TeamActivityApplications_Users
            FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId)
    );
END
GO
