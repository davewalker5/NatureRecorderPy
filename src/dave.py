import datetime
from naturerec_model.logic import list_sightings
from pprint import pprint as pp

from_date = datetime.date(2021, 12, 13)
to_date = datetime.date(2021, 12, 14)
location_id = None
species_id = 2

sightings = list_sightings(from_date=from_date,
                           to_date=to_date,
                           location_id=location_id,
                           species_id=species_id)

for sighting in sightings:
    print(sighting)
    print(sighting.location)
    print(sighting.species)
