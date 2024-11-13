#!/usr/bin/python3
"""
Module for handling State related routes in the API.
This module includes routes for retrieving, creating,
updating, and deleting State objects.
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a specific State object by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)  # Consider returning a JSON error response
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)  # Consider returning a JSON error response
    storage.delete(state)
    storage.save()
    return jsonify({}), 200  # No need for make_response here


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    data = request.get_json(silent=True)
    if data is None:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    if 'name' not in data:
        abort(make_response(jsonify({"error": "Missing name"}), 400))
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates an existing State object by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)  # Consider returning a JSON error response

    data = request.get_json(silent=True)
    if not data:
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    state.save()
    return make_response(jsonify(state.to_dict()), 200)
