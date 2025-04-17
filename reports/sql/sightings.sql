SELECT l.Name AS 'Location', sp.Name AS 'Species', sp.Name AS 'Category', DATE( s.Date ) AS 'Date', IFNULL( s.Number, 1 ) AS 'Count'
FROM SIGHTINGS s
INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId
INNER JOIN CATEGORIES c ON c.Id = sp.CategoryId
INNER JOIN LOCATIONS l ON l.Id = s.LocationId
WHERE l.Name IN ( $LOCATION )
AND s.Date LIKE '$YEAR-%'
AND sp.Name LIKE '%$SPECIES%'
AND c.Name = "$CATEGORY";
