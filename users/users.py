import json

from flask import jsonify, Response, Blueprint, request, render_template
from flask_bcrypt import generate_password_hash, check_password_hash

from utils import queries, utils


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/login/', methods=['GET', 'POST'])
def users_login():
	if request.method == 'GET':
		return render_template('login.html')

	email = utils.get_field(request, 'email', required=True)
	password = utils.get_field(request, 'password', required=True)
	return login(email, password)



@users_blueprint.route('/users/search/', methods=['GET', 'POST'])
def users_search():
	if request.method == 'GET':
		return render_template('search.html')

	query = utils.get_field(request, 'query', required=True)
	user_id = utils.get_num(request, 'user_id', required=True)
	return search_users(query, user_id)


@users_blueprint.route('/users/', methods=['GET', 'POST'])
@users_blueprint.route('/users/<int:user_id>')
def users_route(user_id=None):
	if request.method == 'POST':
		first_name = utils.get_field(request, 'first_name', required=True)
		last_name = utils.get_field(request, 'last_name', required=True)
		email = utils.get_field(request, 'email', required=True)
		password = utils.get_field(request, 'password', required=True)

		return new_user(first_name, last_name, email, password)

	if user_id is None:
		return get_all_users()

	return get_user(user_id)


@users_blueprint.route('/users/facebook', methods=['POST'])
def users_facebook_login():
	first_name = utils.get_field(request, 'first_name', required=True)
	last_name = utils.get_field(request, 'last_name', required=True)
	email = utils.get_field(request, 'email', required=True)
	fb_id = utils.get_field(request, 'fb_id', required=True)
	photo = utils.get_field(request, 'photo', required=True)
	friends = utils.get_list(request, 'friends', required=True)

	return login_facebook(first_name, last_name, email, fb_id, photo, friends)



def login(email, password):

	email = email.strip().lower()

	db_pass = utils.select_query(queries.check_login, (email,))
	if len(db_pass) == 0:
		return jsonify(error='email not in database')
	if not check_password_hash(db_pass[0][0], password):
		return jsonify(error='incorrect password')

	result = {
		'user_id': db_pass[0][1],
		'email': db_pass[0][2],
		'fb_id': db_pass[0][3],
		'photo': db_pass[0][4],
		'first_name': db_pass[0][5],
		'last_name': db_pass[0][6],
	}

	return jsonify(result=result)


def new_user(first_name, last_name, email, password):
	print(first_name, last_name, email, password)

	password = generate_password_hash(password, 12)
	first_name = utils.to_name(first_name)
	last_name = utils.to_name(last_name)
	email = email.lower()

	row = utils.update_query(queries.new_user % (first_name, last_name, email, password.decode('UTF-8')), fetch=True)

	result = {
		'user_id': row[0][0],
		'email': email,
		'first_name': first_name,
		'last_name': last_name,
	}

	return jsonify(result=result)

def login_facebook(first_name, last_name, email, fb_id, photo, friends):
	first_name = utils.to_name(first_name)
	last_name = utils.to_name(last_name)
	email = email.lower()

	check_login = utils.select_query(queries.show_user_email, (email,))

	if len(check_login) != 0:
		check_login = check_login[0]
		fb_f_name = check_login[0]
		fb_l_name = check_login[1]
		fb_fb_id = check_login[2]
		fb_email = check_login[3]
		user_id = check_login[4]
		if fb_fb_id != None and fb_fb_id != fb_id:
			return jsonify(error='Another FB user is using that email')

		if fb_f_name != first_name or fb_l_name != last_name:
			row = utils.update_query(queries.update_user, (first_name, last_name, fb_id, photo, email,), fetch=True)
			user_id = row[0][0]
	else:
		row = utils.update_query(queries.new_fb_user, (first_name, last_name, fb_id, email, photo,), fetch=True)
		user_id = row[0][0]


	rows = utils.select_query(queries.fb_to_user_id, (tuple(friends), user_id,))
	friend_ids = [row[0] for row in rows]

	cont = ','.join(['(%s, %d), (%d, %s)' % (friend, user_id, user_id, friend) for friend in friend_ids])

	if len(friend_ids) > 0:
		utils.update_query(queries.facebook_friends + cont)

	result = {
		'user_id': user_id,
		'email': email,
		'fb_id': fb_id,
		'photo': photo,
		'first_name': first_name,
		'last_name': last_name,
	}
	return jsonify(result=result)


def search_users(query, user_id):

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
	utils.to_name(query), utils.to_name(query), query, utils.to_name(query), utils.to_name(query)))
	utils.add_rows_to_list(rows, results, ('user_id', 'first_name', 'last_name', 'email'))
	return Response(json.dumps(results), mimetype='application/json')


def get_all_users():
	rows = utils.select_query(queries.show_all_users)
	result = []
	utils.add_rows_to_list(rows, result, ('first_name', 'last_name', 'fb_id', 'email', 'user_id'))
	return Response(json.dumps(result),  mimetype='application/json')


def get_user(user_id):
	rows = utils.select_query(queries.show_user % user_id)
	if len(rows) == 0:
		return jsonify(error='No user with that id')
	result = []
	utils.add_rows_to_list(rows, result, ('first_name', 'last_name', 'fb_id', 'email'))
	return Response(json.dumps(result),  mimetype='application/json')
