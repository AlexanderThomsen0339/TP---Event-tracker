USE [Event_Tracker]
GO
/****** Object:  StoredProcedure [dbo].[CreateUser]    Script Date: 03-03-2025 09:30:43 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[CreateUser]
    @Username NVARCHAR(255),
    @Password NVARCHAR(255)
AS
BEGIN
    -- Tjek om brugernavnet allerede eksisterer
    IF EXISTS (SELECT 1 FROM Users WHERE Username = @Username)
    BEGIN
        -- Returner en specifik værdi eller en fejlmeddelelse
        RETURN 1; -- 1 kan betyde "Brugernavn findes allerede"
    END
    ELSE
    BEGIN
        -- Indsæt den nye bruger i Users-tabellen
        INSERT INTO Users (Username, Password)
        VALUES (@Username, @Password);

        -- Returner 0 for at indikere succes
        RETURN 0;
    END
END;