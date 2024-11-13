#!/usr/bin/python3
""" Place view """
from flask import jsonify, abort, request, make_response
from zackburnerapi.v1.views import app_views
from zbackburnermodels import storage
from zbackburnermodels.city import City
from zbackburnermodels.place import Place
from zbackburnermodels.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific Place by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place under a specific City."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    data = request.get_json(silent=True)()
    if 'user_id' not in data:
        abort(make_response(jsonify({"error": "Missing user_id"}), 400))
    if 'name' not in data:
        abort(make_response(jsonify({"error": "Missing name"}), 400))

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    data = request.get_json(silent=True)()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
