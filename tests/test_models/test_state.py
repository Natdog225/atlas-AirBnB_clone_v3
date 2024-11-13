#!/usr/bin/python3
"""
Contains the TestStateDocs, TestState classes, and API tests.
"""

import unittest
import inspect
import pycodestyle as pep8
from api.v1.app import app
from models import storage
from models import state
from models.state import State


class TestStateDocs(unittest.TestCase):
    """Tests to check the documentation and style of State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_f = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state(self):
        """Test that models/state.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_state(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_state_module_docstring(self):
        """Test for the state.py module docstring"""
        self.assertIsNot(state.__doc__, None,
                         "state.py needs a docstring")
        self.assertTrue(len(state.__doc__) >= 1,
                        "state.py needs a docstring")

    def test_state_class_docstring(self):
        """Test for the State class docstring"""
        self.assertIsNot(State.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_func_docstrings(self):
        """Test for the presence of docstrings in State methods"""
        for func in self.state_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestStateAPI(unittest.TestCase):
    """Test the State API endpoints"""

    @classmethod
    def setUpClass(cls):
        """Set up Flask test client for State API tests"""
        app.testing = True
        cls.client = app.test_client()

    def test_create_state_missing_name(self):
        """Test POST /api/v1/states with missing 'name' field in JSON"""
        headers = {"Content-Type": "application/json"}
        response = self.client.post('/api/v1/states', json={}, headers=headers)
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Missing name", error_message.get("description", ""))

    def test_create_state_invalid_json(self):
        """Test POST /api/v1/states with invalid JSON"""
        headers = {"Content-Type": "application/json"}
        response = self.client.post(
            '/api/v1/states', data="invalid_json", headers=headers)
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Not a JSON", error_message.get("description", ""))

    def test_update_state_invalid_json(self):
        """Test PUT /api/v1/states/<state_id> with invalid JSON"""
        state = State(name="Initial State")
        storage.new(state)
        storage.save()

        headers = {"Content-Type": "application/json"}
        response = self.client.put(
            f'/api/v1/states/{state.id}', data="invalid_json", headers=headers)
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Not a JSON", error_message.get("description", ""))

        # Clean up
        storage.delete(state)
        storage.save()

    def test_update_state_missing_name(self):
        """Test PUT /api/v1/states/<state_id> without name in JSON"""
        state = State(name="Initial State")
        storage.new(state)
        storage.save()

        headers = {"Content-Type": "application/json"}
        response = self.client.put(
            f'/api/v1/states/{state.id}', json={}, headers=headers)
        self.assertEqual(response.status_code, 400)
        error_message = response.get_json(silent=True) or {}
        self.assertIn("Missing name", error_message.get("description", ""))

        # Clean up
        storage.delete(state)
        storage.save()


if __name__ == '__main__':
    unittest.main()
