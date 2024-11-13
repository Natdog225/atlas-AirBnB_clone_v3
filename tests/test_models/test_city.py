#!/usr/bin/python3
"""
Contains the TestCityDocs and TestCityAPI classes
"""

from datetime import datetime
import inspect
from api.v1.app import app
from models.state import State
from models.city import City
from models import storage
import pycodestyle as pep8
import unittest


class TestCityDocs(unittest.TestCase):
    """Tests to check the documentation and style of City class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.city_f = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance_city(self):
        """Test that models/city.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_city(self):
        """Test that tests/test_models/test_city.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['tests/test_models/test_city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_city_module_docstring(self):
        """Test for the city.py module docstring"""
        self.assertIsNot(City.__doc__, None,
                         "city.py needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1,
                        "city.py needs a docstring")

    def test_city_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(City.__doc__, None,
                         "City class needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1,
                        "City class needs a docstring")


class TestCityAPI(unittest.TestCase):
    """Test API endpoints related to City"""

    @classmethod
    def setUpClass(cls):
        """Set up Flask test client and resources for testing"""
        app.testing = True
        cls.client = app.test_client()

    def setUp(self):
        """Set up test context and initialize data for each test"""
        self.ctx = app.app_context()
        self.ctx.push()
        storage.reload()
        self.state = State(name="TestState")
        storage.new(self.state)
        storage.save()

    def tearDown(self):
        """Tear down test context and remove created data"""
        storage.delete(self.state)
        storage.save()
        self.ctx.pop()

    def test_get_cities_by_state(self):
        """Test GET /api/v1/states/<state_id>/cities"""
        response = self.client.get(f"/api/v1/states/{self.state.id}/cities")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 0)

    def test_get_city(self):
        """Test GET /api/v1/cities/<city_id>"""
        city = City(name="TestCity", state_id=self.state.id)
        storage.new(city)
        storage.save()

        response = self.client.get(f"/api/v1/cities/{city.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "TestCity")

        # Clean up
        storage.delete(city)
        storage.save()

    def test_delete_city(self):
        """Test DELETE /api/v1/cities/<city_id>"""
        city = City(name="TestCityToDelete", state_id=self.state.id)
        storage.new(city)
        storage.save()

        response = self.client.delete(f"/api/v1/cities/{city.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

        # Ensure city was deleted
        response = self.client.get(f"/api/v1/cities/{city.id}")
        self.assertEqual(response.status_code, 404)

    def test_create_city(self):
        """Test POST /api/v1/states/<state_id>/cities"""
        headers = {"Content-Type": "application/json"}
        data = {"name": "NewCity"}

        response = self.client.post(
            f"/api/v1/states/{self.state.id}/cities",
            json=data,
            headers=headers
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "NewCity")
        self.assertEqual(response.json["state_id"], self.state.id)

    def test_create_city_missing_name(self):
        """Test POST /api/v1/states/<state_id>/cities with missing 'name'"""
        headers = {"Content-Type": "application/json"}
        response = self.client.post(
            f'/api/v1/states/{self.state.id}/cities', json={}, headers=headers)
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Missing name", error_message.get("error", ""))

    def test_update_city(self):
        """Test PUT /api/v1/cities/<city_id>"""
        city = City(name="OldCity", state_id=self.state.id)
        storage.new(city)
        storage.save()

        headers = {"Content-Type": "application/json"}
        data = {"name": "UpdatedCity"}

        response = self.client.put(
            f"/api/v1/cities/{city.id}",
            json=data,
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "UpdatedCity")

        # Clean up
        storage.delete(city)
        storage.save()

    def test_update_city_invalid_json(self):
        """Test PUT /api/v1/cities/<city_id> with invalid JSON"""
        city = City(name="CityWithBadData", state_id=self.state.id)
        storage.new(city)
        storage.save()

        headers = {"Content-Type": "application/json"}
        response = self.client.put(
            f"/api/v1/cities/{city.id}",
            data="Invalid JSON",
            headers=headers
        )
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Not a JSON", error_message.get("error", ""))

        # Clean up
        storage.delete(city)
        storage.save()


if __name__ == '__main__':
    unittest.main()
