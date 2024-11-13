#!/usr/bin/python3

"""
Defines routes for index
"""


from flask import jsonify
from api.v1.views import app_views
from zbackburnermodels import storage
from zbackburnermodels.amenity import Amenity
from zbackburnermodels.city import City
from zbackburnermodels.place import Place
from zbackburnermodels.review import Review
from zbackburnermodels.state import State
from zbackburnermodels.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """checks the api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns the counts of each object by type."""
    stats_data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats_data)
