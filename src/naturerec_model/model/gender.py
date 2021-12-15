from enum import IntEnum


class Gender(IntEnum):
    """
    Enumeration representing the gender of species seen in a sighting
    """
    #: Sightings where the gender is not known
    UNKNOWN = 0
    #: Sightings where only males were seen
    MALE = 1
    #: Sightings where only females were seen
    FEMALE = 2
    #: Sightings where both males and females were seen
    BOTH = 3
