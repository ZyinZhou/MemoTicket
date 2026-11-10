-- 创建数据库
CREATE DATABASE InterestDB;
GO

-- 切换到刚刚创建的数据库
USE InterestDB;
GO

-- 1. 用户表 (Users)
CREATE TABLE Users (
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL UNIQUE,   -- 用户名唯一，防重复注册
    PasswordHash NVARCHAR(255) NOT NULL,     -- 只存密码哈希，不存明文
    CreatedAt DATETIME DEFAULT GETDATE()     -- 自动记录注册时间
);
GO

-- 2. 预设兴趣表 (Interests)
CREATE TABLE Interests (
    InterestId INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(50) NOT NULL UNIQUE        -- 兴趣名称唯一
);
GO

-- 3. 用户-兴趣 关联表 (多对多关系)
CREATE TABLE UserInterests (
    UserId INT NOT NULL,
    InterestId INT NOT NULL,
    PRIMARY KEY (UserId, InterestId),
    FOREIGN KEY (UserId) REFERENCES Users(UserId) ON DELETE CASCADE,
    FOREIGN KEY (InterestId) REFERENCES Interests(InterestId) ON DELETE CASCADE
);
GO

-- 4. 插入预设的 8 个兴趣数据
INSERT INTO Interests (Name) VALUES 
(N'阅读'), (N'音乐'), (N'运动'), (N'电影'), 
(N'旅游'), (N'游戏'), (N'编程'), (N'美食');
GO