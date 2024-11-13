#!/usr/bin/python3

"""
Main app module to start Flask for the API
"""

from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views.index import app_views
from models import storage

# Initialize Flask
app = Flask(__name__)
app.url_map.strict_slashes = False

# Register the blueprint with the prefix
app.register_blueprint(app_views, url_prefix='/api/v1')

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers['Content-Type'] = 'application/json'
    return response

@app.teardown_appcontext
def teardown_db(exception=None):
    """Closes storage on teardown"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
