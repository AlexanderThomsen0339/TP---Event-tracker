CREATE PROCEDURE GetUser
    @Username NVARCHAR(255)
AS
BEGIN
    -- Retrieve the username and hashed password
    SELECT Username FROM Users WHERE Username = @Username;
END;
