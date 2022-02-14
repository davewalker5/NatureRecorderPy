PRAGMA foreign_keys = 0;

CREATE TABLE TempSightings AS SELECT * FROM Sightings;

DROP TABLE Sightings;

CREATE TABLE Sightings (
    Id         INTEGER NOT NULL
                       CONSTRAINT PK_Sightings PRIMARY KEY AUTOINCREMENT,
    LocationId INTEGER NOT NULL,
    SpeciesId  INTEGER NOT NULL,
    Date       TEXT    NOT NULL,
    Number     INTEGER,
    WithYoung  INTEGER NOT NULL
                       DEFAULT 0,
    Gender     INTEGER NOT NULL
                       DEFAULT 0,
    CONSTRAINT FK_Sightings_Locations_LocationId FOREIGN KEY (
        LocationId
    )
    REFERENCES Locations (Id) ON DELETE CASCADE,
    CONSTRAINT FK_Sightings_Species_SpeciesId FOREIGN KEY (
        SpeciesId
    )
    REFERENCES Species (Id) ON DELETE CASCADE
);

INSERT INTO Sightings (
                          Id,
                          LocationId,
                          SpeciesId,
                          Date,
                          Number,
                          WithYoung,
                          Gender
                      )
                      SELECT Id,
                             LocationId,
                             SpeciesId,
                             Date,
                             Number,
                             WithYoung,
                             Gender
                        FROM TempSightings;

DROP TABLE TempSightings;

CREATE INDEX IX_Sightings_LocationId ON Sightings (
    "LocationId"
);

CREATE INDEX IX_Sightings_SpeciesId ON Sightings (
    "SpeciesId"
);

PRAGMA foreign_keys = 1;
