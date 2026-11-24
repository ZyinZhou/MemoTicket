USE InterestDB;
GO

IF COL_LENGTH('dbo.Interests', 'IsCustom') IS NULL
BEGIN
    ALTER TABLE dbo.Interests ADD IsCustom BIT NOT NULL CONSTRAINT DF_Interests_IsCustom DEFAULT (0);
END;
GO

IF COL_LENGTH('dbo.Interests', 'CreatedBy') IS NULL
BEGIN
    ALTER TABLE dbo.Interests ADD CreatedBy INT NULL;
END;
GO

IF COL_LENGTH('dbo.Interests', 'CreatedAt') IS NULL
BEGIN
    ALTER TABLE dbo.Interests ADD CreatedAt DATETIME2(0) NULL;
END;
GO

IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_Interests_CreatedBy_Users')
BEGIN
    ALTER TABLE dbo.Interests ADD CONSTRAINT FK_Interests_CreatedBy_Users
        FOREIGN KEY (CreatedBy) REFERENCES dbo.Users(UserId);
END;
GO
