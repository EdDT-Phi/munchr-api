import os
from flask import jsonify, Blueprint, render_template, request

from users.friends import get_friend_requests
from utils import queries, utils


recommendations_blueprint = Blueprint('recommendations', __name__)


@recommendations_blueprint.route('/notifications/<int:user_id>')
def notifications(user_id):
	requests = get_friend_requests(user_id)

	recommendations = []
	rows = utils.select_query(queries.get_recommendations, (user_id,));
	utils.add_rows_to_list(rows, recommendations, ('first_name', 'last_name', 'photo_url', 'user_id', 'res_id', 'res_name'))

	return jsonify(results={'requests': requests, 'recommendations': recommendations})
    