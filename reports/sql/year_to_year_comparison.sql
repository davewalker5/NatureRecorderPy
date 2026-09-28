SELECT      STRFTIME( '%m', s.Date ) AS "Month",
            SUM( IFNULL( s.Number, 1 ) ) AS "Sightings"
FROM        SIGHTINGS s
INNER JOIN  SPECIES sp ON sp.Id = s.SpeciesId
INNER JOIN  CATEGORIES c ON c.Id = sp.CategoryId
INNER JOIN  LOCATIONS l ON l.Id = s.LocationId
WHERE       l.Name = '$LOCATION'
AND         CAST( STRFTIME( '%Y', s.Date ) AS INTEGER) = $YEAR
AND         c.Name LIKE '%$CATEGORY%'
AND         sp.Name LIKE '%$SPECIES%'
GROUP BY    STRFTIME( '%m', s.Date );
