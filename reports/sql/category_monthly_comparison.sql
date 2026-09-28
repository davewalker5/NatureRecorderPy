-- Count records, not the number of individuals observed.
SELECT CAST(STRFTIME('%Y', s.Date) AS INTEGER) AS "Year",
       CAST(STRFTIME('%m', s.Date) AS INTEGER) AS "Month",
       COUNT(s.Id) AS "Sightings"
FROM SIGHTINGS s
INNER JOIN LOCATIONS l ON l.Id = s.LocationId
INNER JOIN SPECIES sp ON sp.Id = s.SpeciesId
INNER JOIN CATEGORIES c ON c.Id = sp.CategoryId
WHERE l.Name = :location
AND CAST(STRFTIME('%Y', s.Date) AS INTEGER) IN (:year, :comparison_year)
AND c.Name = :category
GROUP BY STRFTIME('%Y', s.Date), STRFTIME('%m', s.Date)
ORDER BY "Year", "Month";
