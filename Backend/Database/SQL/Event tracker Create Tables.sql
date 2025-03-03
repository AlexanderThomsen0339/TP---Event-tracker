CREATE DATABASE Event_Tracker;

USE Event_Tracker;

CREATE TABLE Users (
    User_ID INT PRIMARY KEY IDENTITY(1,1),
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE Locations (
    Location_ID INT PRIMARY KEY IDENTITY(1,1),
    Location_Name VARCHAR(255) NOT NULL,
    Location_LatLong VARCHAR(255) NOT NULL
);

CREATE TABLE Events (
    Event_ID INT PRIMARY KEY IDENTITY(1,1),
    Event_Name VARCHAR(255) NOT NULL,
    Event_Start_Time DATETIME NOT NULL,
    Location_ID INT NOT NULL,
    API_ID VARCHAR(255) UNIQUE NOT NULL,
    FOREIGN KEY (Location_ID) REFERENCES Locations(Location_ID)
);

CREATE TABLE UserEvents (
    User_event_ID INT PRIMARY KEY IDENTITY(1,1),
    User_ID INT NOT NULL,
    Event_ID INT NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Event_ID) REFERENCES Events(Event_ID)
);