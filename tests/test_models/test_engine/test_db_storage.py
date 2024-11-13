#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
from datetime import datetime
import inspect
from unittest.mock import Base
import zbackburnermodels
from zbackburnermodels.engine import db_storage
from zbackburnermodels.amenity import Amenity
from zbackburnermodels.base_model import BaseModel
from zbackburnermodels.city import City
from zbackburnermodels.place import Place
from zbackburnermodels.review import Review
from zbackburnermodels.state import State
from zbackburnermodels.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the test class"""
        os.environ['HBNB_MYSQL_USER'] = 'hbnb_test'
        os.environ['HBNB_MYSQL_PWD'] = 'hbnb_test_pwd'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'
        os.environ['HBNB_ENV'] = 'test'

        cls.storage = DBStorage()
        cls.storage.reload()
        Base.metadata.create_all(cls.storage.__engine)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(zbackburnermodels.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(zbackburnermodels.storage.all()), dict)

    @unittest.skipIf(zbackburnermodels.storage_t != 'db', "not testing db storage")
    def test_returns_obj(self):
        """Test that get returns an existing object """
        state = State(name="California")
        state.save()
        first_state_obj = list(zbackburnermodels.storage.all("State").values())[0]
        state_obj = zbackburnermodels.storage.get("State", first_state_obj.id)
        self.assertIs(first_state_obj, state_obj)

    @unittest.skipIf(zbackburnermodels.storage_t != 'db', "not testing db storage")
    def test_returns_none(self):
        """Test that get returns None for nonexisting object """
        state_obj = zbackburnermodels.storage.get("State", "IDONTEXIST")
        self.assertIsNone(state_obj)

    @unittest.skipIf(zbackburnermodels.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(zbackburnermodels.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(zbackburnermodels.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(zbackburnermodels.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count is properly return """
        objs = zbackburnermodels.storage.all()
        self.assertEqual(len(objs), zbackburnermodels.storage.count())
        state_objs = zbackburnermodels.storage.all("State")
        self.assertEqual(len(state_objs), zbackburnermodels.storage.count("State"))
        no_objs = zbackburnermodels.storage.all("Any")
        self.assertEqual(len(no_objs), zbackburnermodels.storage.count("Any"))
