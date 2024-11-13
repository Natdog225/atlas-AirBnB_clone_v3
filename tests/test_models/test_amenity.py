#!/usr/bin/python3
"""
Contains the TestAmenityDocs classes
"""

from datetime import datetime
import inspect
import models
from models import amenity
from models.amenity import Amenity
from models.base_model import BaseModel
import pycodestyle as pep8
import unittest
from api.v1.app import app
from models import storage
from flask import Flask


class TestAmenityDocs(unittest.TestCase):
    """Tests to check the documentation and style of Amenity class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.amenity_f = inspect.getmembers(Amenity, inspect.isfunction)

    def test_pep8_conformance_amenity(self):
        """Test that models/amenity.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_amenity(self):
        """Test that tests/test_models/test_amenity.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['tests/test_models/test_amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenity_module_docstring(self):
        """Test for the amenity.py module docstring"""
        self.assertIsNot(amenity.__doc__, None,
                         "amenity.py needs a docstring")
        self.assertTrue(len(amenity.__doc__) >= 1,
                        "amenity.py needs a docstring")

    def test_amenity_class_docstring(self):
        """Test for the Amenity class docstring"""
        self.assertIsNot(Amenity.__doc__, None,
                         "Amenity class needs a docstring")
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "Amenity class needs a docstring")

    def test_amenity_func_docstrings(self):
        """Test for the presence of docstrings in Amenity methods"""
        for func in self.amenity_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestAmenity(unittest.TestCase):
    """Test the Amenity class"""

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel"""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name_attr(self):
        """Test that Amenity has attribute name, and it's an empty string"""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))
        if models.storage_t == 'db':
            self.assertEqual(amenity.name, None)
        else:
            self.assertEqual(amenity.name, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attrs"""
        am = Amenity()
        new_d = am.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in am.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        am = Amenity()
        new_d = am.to_dict()
        self.assertEqual(new_d["__class__"], "Amenity")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], am.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], am.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output"""
        amenity = Amenity()
        string = "[Amenity] ({}) {}".format(amenity.id, amenity.__dict__)
        self.assertEqual(string, str(amenity))


class TestAmenityAPI(unittest.TestCase):
    """Test API endpoints related to Amenity."""

    @classmethod
    def setUpClass(cls):
        """Set up Flask test client and resources for testing."""
        app.testing = True
        cls.client = app.test_client()

    def setUp(self):
        """Initialize test context and create a test amenity object."""
        self.ctx = app.app_context()
        self.ctx.push()
        storage.reload()

        # Create a test amenity
        self.amenity = Amenity(name="Test Amenity")
        storage.new(self.amenity)
        storage.save()

    def tearDown(self):
        """Remove test context and delete the test amenity object."""
        storage.delete(self.amenity)
        storage.save()
        self.ctx.pop()

    def test_get_amenities(self):
        """Test GET /api/v1/amenities returns all amenities."""
        response = self.client.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_amenity(self):
        """Test GET /api/v1/amenities/<amenity_id> for a specific amenity."""
        response = self.client.get(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Test Amenity")

    def test_get_amenity_not_found(self):
        """Test GET /api/v1/amenities/<amenity_id> with a non-existent ID."""
        response = self.client.get('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        """Test DELETE /api/v1/amenities/<amenity_id> to delete an amenity."""
        response = self.client.delete(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

    def test_delete_amenity_not_found(self):
        """Test DELETE /api/v1/amenities/<amenity_id> with a non-existent ID"""
        response = self.client.delete('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        """Test POST /api/v1/amenities to create a new amenity."""
        headers = {"Content-Type": "application/json"}
        data = {"name": "New Amenity"}
        response = self.client.post(
            '/api/v1/amenities', json=data, headers=headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "New Amenity")

        # Clean up
        new_amenity = storage.get(Amenity, response.json['id'])
        storage.delete(new_amenity)
        storage.save()

    def test_create_amenity_missing_name(self):
        """Test POST /api/v1/amenities with missing 'name' field."""
        headers = {"Content-Type": "application/json"}
        response = self.client.post(
            '/api/v1/amenities', json={}, headers=headers
        )
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Missing name", error_message.get("error", ""))

    def test_create_amenity_invalid_json(self):
        """Test POST /api/v1/amenities with invalid JSON."""
        headers = {"Content-Type": "application/json"}
        response = self.client.post(
            '/api/v1/amenities', data="invalid_json", headers=headers
        )
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Not a JSON", error_message.get("error", ""))

    def test_update_amenity(self):
        """Test PUT /api/v1/amenities/<amenity_id> to update an amenity."""
        headers = {"Content-Type": "application/json"}
        data = {"name": "Updated Amenity"}
        response = self.client.put(
            f'/api/v1/amenities/{self.amenity.id}', json=data, headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Amenity")

    def test_update_amenity_not_found(self):
        """Test PUT /api/v1/amenities/<amenity_id> with a non-existent ID."""
        headers = {"Content-Type": "application/json"}
        data = {"name": "Updated Amenity"}
        response = self.client.put(
            '/api/v1/amenities/invalid_id', json=data, headers=headers
        )
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_invalid_json(self):
        """Test PUT /api/v1/amenities/<amenity_id> with invalid JSON."""
        headers = {"Content-Type": "application/json"}
        response = self.client.put(
           f'amenities/{self.amenity.id}', data="invalid_json", headers=headers
        )
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Not a JSON", error_message.get("error", ""))


if __name__ == '__main__':
    unittest.main()
