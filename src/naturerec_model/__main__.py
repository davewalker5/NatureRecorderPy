from naturerec_model.model.base import Base

# To ensure the tables are all created correctly, the entity class definitions must be imported before updating
# the database, even if these definitions aren't used directly
from naturerec_model.model import Location
from naturerec_model.model import Category
from naturerec_model.model import Species
from naturerec_model.model import Sighting
from naturerec_model.model import StatusScheme
from naturerec_model.model import StatusRating
from naturerec_model.model import SpeciesStatusRating
from naturerec_model.model import JobStatus
from naturerec_model.model import User

# Create/update the database. For details on where the SQLite database file is located, see the comments in the
# _get_db_path() function in database.py
from naturerec_model.model import Engine
Base.metadata.create_all(Engine)
