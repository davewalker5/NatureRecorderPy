-- Check comparison-year availability and location coverage before applying a species/category filter.
SELECT CAST(STRFTIME('%Y', s.Date) AS INTEGER) AS "Year",
       MIN(s.Date) AS "First date", MAX(s.Date) AS "Last date"
FROM SIGHTINGS s
INNER JOIN LOCATIONS l ON l.Id = s.LocationId
WHERE l.Name = :location
GROUP BY STRFTIME('%Y', s.Date)
ORDER BY "Year";
