SELECT (SELECT COUNT(*) FROM LOCATIONS WHERE Name = :location) AS location,
       (SELECT COUNT(*) FROM SPECIES WHERE Name = :species) AS species,
       (SELECT COUNT(*) FROM CATEGORIES WHERE Name = :category) AS category;
