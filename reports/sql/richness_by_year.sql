SELECT l.Name AS 'Location', l.Latitude, l.Longitude, sp.Name AS 'Species', DATE( s.Date ) AS 'Date'
FROM SIGHTINGS s
INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId
INNER JOIN CATEGORIES c ON c.Id = sp.CategoryId
INNER JOIN LOCATIONS l ON l.Id = s.LocationId
WHERE l.Country = '$COUNTRY'
AND l.Latitude IS NOT NULL
AND l.Longitude IS NOT NULL
AND s.Date LIKE '$YEAR-%';
