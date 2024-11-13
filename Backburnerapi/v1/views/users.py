#!/usr/bin/python3
""" User view """
from flask import jsonify, abort, request, make_response
from Backburnerapi.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects."""
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object with the given ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object with the given ID."""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a new User object."""
    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    if 'email' not in request.get_json():
        abort(make_response(jsonify({"error": "Missing email"}), 400))

    if 'password' not in request.get_json():
        abort(make_response(jsonify({"error": "Missing password"}), 400))

    data = request.get_json(silent=True)()
    instance = User(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User object with the given ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json(silent=True)()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
