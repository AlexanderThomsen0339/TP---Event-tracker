USE [Event_Tracker]
GO
/****** Object:  StoredProcedure [dbo].[GetEventsWithinRadius]    Script Date: 03-03-2025 09:30:15 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[GetEventsWithinRadius]
    @user_latitude FLOAT,
    @user_longitude FLOAT,
    @radius_km FLOAT
AS
BEGIN
    -- Select statement to fetch events within the specified radius in KM
    SELECT 
        e.Event_ID, 
        e.Event_Name, 
        e.Event_Start_Time, 
        l.Location_Name
    FROM 
        Events e  -- Ændret fra Event til Events
    JOIN 
        Locations l ON e.Location_ID = l.Location_ID  -- Ændret fra Location til Locations
    WHERE 
        geography::Point(@user_latitude, @user_longitude, 4326).STDistance(
            geography::Point(
                CAST(SUBSTRING(l.Location_LatLong, 1, CHARINDEX(',', l.Location_LatLong) - 1) AS FLOAT),
                CAST(SUBSTRING(l.Location_LatLong, CHARINDEX(',', l.Location_LatLong) + 1, LEN(l.Location_LatLong)) AS FLOAT), 
                4326)
        ) <= (@radius_km * 1000);
END;
