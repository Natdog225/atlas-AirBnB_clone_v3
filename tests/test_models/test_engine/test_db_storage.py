#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
from unittest.mock import Base
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
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
        cls.storage = DBStorage()
        cls.storage.reload()

    def setUp(self):
        """Set up for each test"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Tear down for each test"""
        self.storage.__session.rollback()

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
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        try:
            self.assertIs(type(models.storage.all()), dict)
        except Exception as e:
            print(f"Exception occurred: {e}")
            self.fail(f"Exception occurred: {e}")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get properly retrieves one object, on class and ID"""
        storage = DBStorage()
        storage.reload()
        for key, value in classes.items():
            obj = value()
            storage.new(obj)
            storage.save()
            test_obj = storage.get(value, obj.id)
            self.assertIsNotNone(test_obj)
            self.assertEqual(obj.id, test_obj.id)
            self.assertEqual(obj.__class__, test_obj.__class__)
            self.assertEqual(obj.to_dict(), test_obj.to_dict())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count properly counts the number of objects in storage"""
        storage = DBStorage()
        storage.reload()
        count = 0
        for value in classes.values():
            obj = value()
            storage.new(obj)
            storage.save()
            count += 1
        self.assertEqual(count, storage.count())
        self.assertEqual(storage.count(State), 1)
        self.assertEqual(storage.count(City), 1)
        self.assertEqual(storage.count(Amenity), 1)
        self.assertEqual(storage.count(Place), 1)
        self.assertEqual(storage.count(Review), 1)
