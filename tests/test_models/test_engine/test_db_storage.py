#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import pycodestyle as pep8
import unittest


DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['test_engine/test_db_storage.py'])
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


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objs = models.storage.all()
        self.assertGreaterEqual(len(all_objs), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        initial_count = models.storage.count(State)
        state = State(name="Test State")
        models.storage.new(state)
        models.storage.save()
        self.assertEqual(models.storage.count(State), initial_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        state = State(name="Another Test State")
        models.storage.new(state)
        models.storage.save()
        saved_state = models.storage.get(State, state.id)
        self.assertIsNotNone(saved_state)
        self.assertEqual(saved_state.name, "Another Test State")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves the correct object based on class and id"""
        state = State(name="Unique Test State")
        models.storage.new(state)
        models.storage.save()
        retrieved_state = models.storage.get(State, state.id)
        self.assertEqual(retrieved_state, state)
        self.assertEqual(retrieved_state.name, "Unique Test State")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_nonexistent(self):
        """Test that get returns None when an object is not found"""
        self.assertIsNone(models.storage.get(State, "nonexistent_id"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the correct count of objects in storage"""
        initial_count = models.storage.count()
        new_state = State(name="Count Test State")
        models.storage.new(new_state)
        models.storage.save()
        self.assertEqual(models.storage.count(), initial_count + 1)
        models.storage.delete(new_state)
        models.storage.save()
        self.assertEqual(models.storage.count(), initial_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_specific_class(self):
        """Test that count returns the correct count for a specific class"""
        initial_state_count = models.storage.count(State)
        state = State(name="State Count Test")
        models.storage.new(state)
        models.storage.save()
        self.assertEqual(models.storage.count(State), initial_state_count + 1)
        models.storage.delete(state)
        models.storage.save()
        self.assertEqual(models.storage.count(State), initial_state_count)


if __name__ == "__main__":
    unittest.main()
