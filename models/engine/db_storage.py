#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        logger.info("Initializing DBStorage...")
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB))
        
        logger.info("Creating tables...")
        Base.metadata.create_all(self.__engine)
        
        logger.info("Initializing session...")
        self.reload()
        
        logger.info("Verifying table existence...")
        self.verify_tables_existence()

    def verify_tables_existence(self):
        """Check if tables exist and create them if they don't"""
        inspector = sqlalchemy.inspect(self.__engine)
        
        for table_name in classes.keys():
            table_name_lower = table_name.lower()
            
            if not inspector.has_table(table_name_lower):
                logger.info(f"Creating table {table_name}")
                try:
                    Base.metadata.tables[table_name_lower].create(self.__engine)
                    logger.info(f"Table {table_name} created successfully")
                except Exception as e:
                    logger.error(f"Failed to create table {table_name}: {str(e)}")

    # ... (rest of the methods remain the same)

    def save(self):
        """Commit all changes of the current database session"""
        try:
            self.__session.commit()
        except Exception as e:
            logger.error(f"Failed to commit changes: {str(e)}")
            self.__session.rollback()

    def close(self):
        """Call remove() method on the private session attribute"""
        try:
            self.__session.remove()
        except Exception as e:
            logger.error(f"Failed to close session: {str(e)}")
