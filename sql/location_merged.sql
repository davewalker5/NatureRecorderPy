-- Auditing columns are currently unused but early implementation introduced an issue with
-- pre existing records. The sighting date has always been correct. This fixes the audit
-- column issue
UPDATE SIGHTINGS SET Date_Created = Date WHERE Date_Created < Date;
UPDATE SIGHTINGS SET Date_Updated = Date_Created WHERE Date_Updated < Date_Created;

-- Location merger generated apparent duplicate records at a location - this identifes them
SELECT DISTINCT s.Id,
                s.Date,
                s.LocationId,
                s.SpeciesId,
                SUM( s.Number ) AS "Count",
                COUNT( s. Id ) AS "Records"
FROM            SIGHTINGS s
GROUP BY        s.Date,
                s.LocationId,
                s.SpeciesId
HAVING          COUNT( s.Id ) > 1
ORDER BY        COUNT( s.Id ) DESC;

/*
The "location rollup" addressed the issue of locations being too granular making the data too cumbersome to maintain. That basically meant reassigning the location ID on records for which the location was being merged with another adjacent location.

However, this resulted in duplicate records for some date/location/species combinations, e.g.

Id	LocationId	SpeciesId	Date	Number	WithYoung	Gender	Notes	Created_By	Updated_By	Date_Created	Date_Updated
4448	11	106	2001-05-07 00:00:00		0	0		0	0	2001-05-07 00:00:00	2001-05-07 00:00:00
4449	11	106	2001-05-07 00:00:00		0	0		0	0	2001-05-07 00:00:00	2001-05-07 00:00:00
4920	11	106	2001-05-07 00:00:00		0	0		0	0	2001-05-07 00:00:00	2001-05-07 00:00:00
4923	11	106	2001-05-07 00:00:00		0	0		0	0	2001-05-07 00:00:00	2001-05-07 00:00:00

Date/Location/Species duplicate groups can be identified using the preceding query.

These should be rolled up into one record per duplicate group, applying the following logic:

- The data should be merged into the first record in each duplicate group as follows:
    - WithYoung will either be 0 or 1 :
        If any records in a duplicate group have it set to 1 -> 1 in the merged record
    - Gender may be 0, 1 or 2 :
        If 1+ records in a duplicate group have it set to 3 -> 3 in the merged record
        If 1+ records in a duplicate group have it set to 1 AND 1+ records have it set to 2 -> 3 in the merged record
        If 1+ records in a duplicate group have it set to 1 AND the rest have it set to 0 -> 1 in the merged record
        If 1+ records in a duplicate group have it set to 2 AND the rest have it set to 0 -> 2 in the merged record
        Else set it to 0
    - Notes should be a concatenation for records in each duplicate group
    - If any records in te
    - Number should be the sum across the records in each duplicate group, using 1 for the number in the individual records if the recorder number is NULL or 0
- The *other* records in the group should then be deleted
*/
