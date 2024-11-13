#!/usr/bin/python3
"""Index file for reasons"""
from flask import jsonify
from Backburnerapi.v1.views import app_views
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """I know it seems crazy, but this defines the status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def some_stats():
    """ number of each object """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
