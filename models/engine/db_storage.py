#!/usr/bin/python3
"""
This module contains the DBStorage class, which handles database operations
for the application.
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Interacts with the MySQL database."""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object."""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(HBNB_MYSQL_USER,
                                                HBNB_MYSQL_PWD,
                                                HBNB_MYSQL_HOST,
                                                HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)

        sess_factory = sessionmaker(bind=self.__engine,
                                   expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def all(self, cls=None):
        """Query on the current database session."""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database."""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine,
                                   expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session attribute."""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve one object based on class and ID."""
        if cls in classes.values():
            obj = self.__session.query(cls).get(id)
            if obj:
                print(f"Retrieved object: {obj}")
            else:
                print(f"Object not found: {cls.__name__} with id {id}")
            return obj
        return None


    def count(self, cls=None):
        """Count objects in storage."""
        print(f"Counting objects of type: {cls}")  # Debugging print statement
        if cls is None:
            total_count = 0
            for clss in classes.values():
                total_count += len(self.__session.query(clss).all())
            print(f"Total object count: {total_count}")  # Debugging print statement
            return total_count
        elif cls in classes.values():
            class_count = len(self.__session.query(cls).all())
            print(f"Object count for {cls.__name__}: {class_count}")  # Debugging print statement
            return class_count
        else:
            return 0

    def check_tables(self):
        """Check if tables exist in the database."""
        inspector = inspect(self.__engine)
        for table_name in inspector.get_table_names():
            print(f"Table exists: {table_name}")
