CREATE PROCEDURE CreateLocationAndEvent 
    @LocationName VARCHAR(255),
    @LatLong VARCHAR(255),
    @EventName VARCHAR(255),
    @EventStartTime DATETIME,
    @ApiID VARCHAR(255),
    @NewLocationID INT OUTPUT,
    @NewEventID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;  -- Prevents unnecessary result sets

    -- Insert location if it does not exist
    IF NOT EXISTS (SELECT 1 FROM Location WHERE Location_Name = @LocationName)
    BEGIN
        INSERT INTO Location (Location_Name, Location_LatLong) 
        VALUES (@LocationName, @LatLong);
        SET @NewLocationID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        SELECT @NewLocationID = Location_ID FROM Location WHERE Location_Name = @LocationName;
    END

    -- Insert event if it does not exist (only check API_ID)
    IF NOT EXISTS (SELECT 1 FROM Event WHERE API_ID = @ApiID)
    BEGIN
        INSERT INTO Event (Event_Name, Event_Start_Time, API_ID, Location_ID) 
        VALUES (@EventName, @EventStartTime, @ApiID, @NewLocationID);
        SET @NewEventID = SCOPE_IDENTITY();
    END
    ELSE
    BEGIN
        SELECT @NewEventID = Event_ID FROM Event WHERE API_ID = @ApiID;
    END

    -- Return the inserted IDs
    SELECT @NewLocationID AS NewLocationID, @NewEventID AS NewEventID;
END;
