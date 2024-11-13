#!/usr/bin/python3

"""
Main app module to start Flask for the API
"""

# No need to import HTTPException here
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

# Initialize Flask
app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

storage.reload()

@app.teardown_appcontext
def teardown_db(exception=None):
    """Closes storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error=None):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
