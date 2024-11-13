#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from Backburnerapi.v1.views.index import * #wildcard thing it wanted
from Backburnerapi.v1.views.states import *
from Backburnerapi.v1.views.cities import *
from Backburnerapi.v1.views.amenities import *
from Backburnerapi.v1.views.users import *
from Backburnerapi.v1.views.places import *
from Backburnerapi.v1.views.places_reviews import *