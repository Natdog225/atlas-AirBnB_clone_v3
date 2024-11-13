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
    from zbackburnermodels.engine.db_storage import DBStorage
    storage = DBStorage()
    logger.info("Using DBStorage")
else:
    from zbackburnermodels.engine.file_storage import FileStorage
    storage = FileStorage()
    logger.info("Using FileStorage")

# Reload storage to ensure tables are created
storage.reload()
logger.info("Storage reloaded successfully")

# Import all models to ensure they're registered with SQLAlchemy
from zbackburnermodels.amenity import Amenity
from zbackburnermodels.base_model import BaseModel
from zbackburnermodels.city import City
from zbackburnermodels.place import Place
from zbackburnermodels.review import Review
from zbackburnermodels.state import State
from zbackburnermodels.user import User

logger.info("All models imported successfully")
