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

    @staticmethod
    def gender_name(gender):
        """
        Return the name for a specified gender enum value

        :return: The name corresponding to the specified gender
        """
        names = ["Unknown", "Male", "Female", "Both"]
        return names[gender]

    @staticmethod
    def gender_map():
        """
        Return a dictionary of gender value/name mappings

        :return: Dictionary of gender value/name mappings
        """
        names = ["Unknown", "Male", "Female", "Both"]
        return {g: names[g] for g in range(0, 4)}
