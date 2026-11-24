-- 切换到目标数据库
USE InterestDB;
GO

-- 1. 用户表加字段
ALTER TABLE Users ADD 
    Nickname NVARCHAR(50) NULL, 
    AvatarUrl NVARCHAR(500) NULL,
    Bio NVARCHAR(200) NULL, 
    UpdatedAt DATETIME DEFAULT GETDATE(),
    TokenNonce NVARCHAR(64) NULL;
GO

-- 为已有用户生成默认的 TokenNonce
UPDATE Users SET TokenNonce = CONVERT(NVARCHAR(64), NEWID()) WHERE TokenNonce IS NULL;
GO

-- 2. 兴趣表加字段
ALTER TABLE Interests ADD 
    IsPreset BIT DEFAULT 1, 
    CreatedBy INT NULL;
GO

-- 3. 分享表
CREATE TABLE Shares (
    ShareId INT IDENTITY(1,1) PRIMARY KEY,
    UserId INT NOT NULL,
    Title NVARCHAR(100) NOT NULL,
    Content NVARCHAR(MAX) NOT NULL,
    InterestId INT NULL,
    ShareType TINYINT DEFAULT 0,
    CreatedAt DATETIME DEFAULT GETDATE(),
    IsDeleted BIT DEFAULT 0,
    FOREIGN KEY (UserId) REFERENCES Users(UserId),
    FOREIGN KEY (InterestId) REFERENCES Interests(InterestId)
);
GO

-- 4. 推荐/避雷扩展表
CREATE TABLE ShareRatings (
    RatingId INT IDENTITY(1,1) PRIMARY KEY,
    ShareId INT NOT NULL UNIQUE,
    TargetName NVARCHAR(100) NOT NULL,
    Score TINYINT NULL,
    FOREIGN KEY (ShareId) REFERENCES Shares(ShareId) ON DELETE CASCADE
);
GO