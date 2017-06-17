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


@users_blueprint.route('/users/new/', methods=['POST'])
def users_route():
	first_name = utils.get_field(request, 'first_name', required=True)
	last_name = utils.get_field(request, 'last_name', required=True)
	email = utils.get_field(request, 'email', required=True)
	password = utils.get_field(request, 'password', required=True)

	password = generate_password_hash(password, 12)
	first_name = utils.to_name(first_name)
	last_name = utils.to_name(last_name)
	email = email.lower()

	row = utils.update_query(queries.new_user, (first_name, last_name, email, password.decode('UTF-8')), fetch=True)

	result = {
		'user_id': row[0][0],
		'email': email,
		'first_name': first_name,
		'last_name': last_name,
	}

	return jsonify(result=result)
