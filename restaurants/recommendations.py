import os
from flask import jsonify, Blueprint, render_template, request

from users.ratings import get_unrated
from users.friends import get_friend_requests
from utils import queries, utils
from auth import auth

recommendations_blueprint = Blueprint('recommendations', __name__)


@recommendations_blueprint.route('/notifications/', methods=['POST'])
@auth.login_required
def notifications():

	user_id = utils.get_num(request, 'user_id', required=True)

	requests = get_friend_requests(user_id)

	recommendations = []
	rows = utils.select_query(queries.get_recommendations, (user_id,));
	utils.add_rows_to_list(rows, recommendations, ('first_name', 'last_name', 'photo_url', 'user_id', 'res_id', 'res_name'))

	ratings = get_unrated(user_id)

	return jsonify(results={'requests': requests, 'recommendations': recommendations, 'ratings': ratings})


@recommendations_blueprint.route('/notifications/dismiss/', methods=['POST'])
@auth.login_required
def delete_recommendation():

	user_id = utils.get_num(request, 'user_id', required=True)
	user_from_id = utils.get_num(request, 'user_from_id', required=True)
	res_id = utils.get_field(request, 'res_id', required=True)

	utils.update_query(queries.delete_recommendation, (user_from_id, user_id, res_id));
	return jsonify(success=True)

