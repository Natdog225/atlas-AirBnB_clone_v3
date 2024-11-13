#!/usr/bin/python3
"""
cities.py

This module defines the routes for handling
city-related operations in the Flask API. It provides
the following functionalities:

1. **GET /api/v1/states/<state_id>/cities**: gets citys from one state.
2. **GET /api/v1/cities/<city_id>**: details for specific city by its ID.
3. **DELETE /api/v1/cities/<city_id>**: Deletes a city by its ID.
4. **POST /api/v1/states/<state_id>/cities**: Creates a new city.
5. **PUT /api/v1/cities/<city_id>**: Updates an existing city.

Each route interacts with the database using
the `storage` object to fetch, create, or modify city data.
"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")

    city = City(name=data['name'], state_id=state_id)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
