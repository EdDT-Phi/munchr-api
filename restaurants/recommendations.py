import os
from flask import jsonify, Blueprint, render_template, request

from users.friends import get_friend_requests
from utils import queries, utils


recommendations_blueprint = Blueprint('recommendations', __name__)


@recommendations_blueprint.route('/restaurants/notifications/<int:user_id>')
def notifications(user_id):
	requests = get_friend_requests(user_id)

	return jsonify(results={'requests': requests})
    