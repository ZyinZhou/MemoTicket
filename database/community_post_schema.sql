USE InterestDB;
GO

-- Beta：兴趣社区动态表
-- 可重复执行；不修改 Alpha 阶段已有表和数据。
IF OBJECT_ID('dbo.CommunityPosts', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.CommunityPosts (
        PostId      INT IDENTITY(1,1) PRIMARY KEY,
        UserId      INT NOT NULL,
        InterestId  INT NOT NULL,
        TicketId    INT NULL,
        Content     NVARCHAR(1000) NOT NULL,
        CreateTime  DATETIME NOT NULL DEFAULT GETDATE(),
        UpdateTime  DATETIME NULL,

        CONSTRAINT FK_CommunityPosts_Users
            FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId),

        CONSTRAINT FK_CommunityPosts_Interests
            FOREIGN KEY (InterestId) REFERENCES dbo.Interests(InterestId),

        CONSTRAINT FK_CommunityPosts_Tickets
            FOREIGN KEY (TicketId) REFERENCES dbo.Tickets(TicketId)
            ON DELETE SET NULL,

        CONSTRAINT CK_CommunityPosts_Content_NotEmpty
            CHECK (LEN(LTRIM(RTRIM(Content))) > 0)
    );
END;
GO

-- 为“按兴趣、按最新时间查看动态”的基础查询建立索引。
IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_CommunityPosts_InterestId_CreateTime'
      AND object_id = OBJECT_ID('dbo.CommunityPosts')
)
BEGIN
    CREATE INDEX IX_CommunityPosts_InterestId_CreateTime
        ON dbo.CommunityPosts (InterestId, CreateTime DESC, PostId DESC);
END;
GO