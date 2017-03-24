from flask import Blueprint, render_template, request
from utils import queries, utils
from restaurants.restaurants import get_details_obj
from restaurants.filters import filters

ratings_blueprint = Blueprint('ratings', __name__)

@ratings_blueprint.route('/users/rating')
def user_rating():
	