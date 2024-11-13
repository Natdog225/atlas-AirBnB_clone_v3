#!/usr/bin/python3
"""
initialize the models package
"""

import logging
from os import getenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    logger.info("Using DBStorage")
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    logger.info("Using FileStorage")

# Reload storage to ensure tables are created
storage.reload()
logger.info("Storage reloaded successfully")

# Import all models to ensure they're registered with SQLAlchemy
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

logger.info("All models imported successfully")
