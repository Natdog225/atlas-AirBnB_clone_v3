#!/usr/bin/python3
""" Amenity view """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects."""
    all_amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in all_amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a specific Amenity by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(make_response(jsonify({"error": "Not found"}), 404))
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(make_response(jsonify({"error": "Not found"}), 404))
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity."""
    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))
    if 'name' not in request.get_json():
        abort(make_response(jsonify({"error": "Missing name"}), 400))
    data = request.get_json(silent=True)()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(make_response(jsonify({"error": "Not found"}), 404))

    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json(silent=True)()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
