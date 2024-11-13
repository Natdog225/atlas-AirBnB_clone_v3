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
        
        # Get all defined tables from Base.metadata
        defined_tables = {table.name.lower(): table for table in Base.metadata.sorted_tables}
        
        for table_name in classes.keys():
            table_name_lower = table_name.lower()
            
            if table_name_lower not in defined_tables:
                logger.warning(f"Table {table_name} is not defined in Base.metadata")
                continue
            
            if not inspector.has_table(table_name_lower):
                logger.info(f"Creating table {table_name}")
                try:
                    defined_tables[table_name_lower].create(self.__engine)
                    logger.info(f"Table {table_name} created successfully")
                except Exception as e:
                    logger.error(f"Failed to create table {table_name}: {str(e)}")

    def get(self, cls, id):
        """Retrieves an object based on the class name and its ID."""
        if cls is None or cls not in classes or id is None or type(id) is not str:
            return None
        cls = classes[cls]
        objs = self.__session.query(cls).filter(cls.id == id)
        if objs is None:
            return None
        return objs.first()

    def count(self, cls=None):
        """Retrieves the total number of object based on the class name."""
        count = 0
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    count += 1
        return count

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()
