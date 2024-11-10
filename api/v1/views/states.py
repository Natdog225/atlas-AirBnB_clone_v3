#!/usr/bin/python3
#!/usr/bin/python3
""" States view """
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from sqlalchemy import func
import traceback


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State """
    try:
        if request.content_type != 'application/json':
            return make_response(jsonify({"error": "Content-Type must be application/json"}), 400)

        try:
            data = request.get_json()
        except Exception:
            return make_response(jsonify({"error": "Invalid JSON"}), 400)

        if not data:
            return make_response(jsonify({"error": "Empty JSON"}), 400)

        if 'name' not in data:
            return make_response(jsonify({"error": "Missing name"}), 400)

        existing_state = storage.session.query(State).filter(
            func.lower(State.name) == func.lower(data['name'])
        ).first()

        if existing_state:
            return make_response(jsonify({"error": f"A state named '{data['name']}' already exists."}), 400)

        instance = State(**data)
        
        try:
            instance.save()
        except Exception as e:
            return make_response(jsonify({
                "error": f"Failed to save state: {str(e)}",
                "details": traceback.format_exc()
            }), 500)

        return make_response(jsonify(instance.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({
            "error": str(e),
            "details": traceback.format_exc()
        }), 500)



@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
