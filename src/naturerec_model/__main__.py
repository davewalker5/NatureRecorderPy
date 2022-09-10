from src.naturerec_model.model.base import Base

# To ensure the tables are all created correctly, the entity class definitions must be imported before updating
# the database, even if these definitions aren't used directly
from src.naturerec_model.model import Location
from src.naturerec_model.model import Category
from src.naturerec_model.model import Species
from src.naturerec_model.model import Sighting
from src.naturerec_model.model import StatusScheme
from src.naturerec_model.model import StatusRating
from src.naturerec_model.model import SpeciesStatusRating
from src.naturerec_model.model import JobStatus
from src.naturerec_model.model import User

# Create/update the database. For details on where the SQLite database file is located, see the comments in the
# _get_db_path() function in database.py
from src.naturerec_model.model import Engine
Base.metadata.create_all(Engine)
