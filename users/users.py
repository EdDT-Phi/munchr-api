import json

from flask import jsonify, Response, Blueprint, request, render_template
from flask_bcrypt import generate_password_hash, check_password_hash

from utils import queries, utils
from auth import auth


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users/search/', methods=['POST'])
@auth.login_required
def users_search():

	user_id = utils.get_num(request, 'user_id', required=True)
	query = utils.get_field(request, 'query', required=True)

	query = query.lower()
	results = []
	# search among friends
	# rows = utils.select_query(
	# search_friends %
	# (user_id, utils.to_name(query), utils.to_name(query), query, utils.to_name(query), utils.to_name(query)))
	# add_rows_to_list(rows, results, ('user_id', 'first_name', 'last_name', 'email'))

	# search among friends' friends

	# search among all users
	rows = utils.select_query(queries.search_all, (
		utils.to_name(query),
		utils.to_name(query),
		query + '%',
		utils.to_name(query) + '%',
		utils.to_name(query) + '%'))
	utils.add_rows_to_list(rows, results, ('user_id', 'first_name', 'last_name', 'photo_url'))
	return jsonify(results=results)
