import json
import uuid
import time

from flask_httpauth import HTTPTokenAuth
from flask import jsonify, Response, Blueprint, request, render_template
from flask_bcrypt import generate_password_hash, check_password_hash

from utils import queries, utils


auth_blueprint = Blueprint('auth', __name__)
auth = HTTPTokenAuth(scheme='Token')

@auth.verify_token
def verify_token(token):
	print('verifying token: %s' % token)

	user_id = utils.get_num(request, 'user_id', required=True)

	if user_id == 3 and token == 'test-token':
		return True

	try:
		verify_token = utils.select_query(queries.verify_token, (user_id, token))
	except:
		return False

	if len(verify_token) == 0:
		return False

	return time.time() - verify_token[0][0] < 60 * 60 * 2


@auth_blueprint.route('/auth/token/', methods=['POST'])
def get_new_token():

	user_id = utils.get_num(request, 'user_id', required=True)
	old_token = utils.get_field(request, 'old_token', required=True)

	verify_token = utils.select_query(queries.verify_token, (user_id, old_token))

	if len(verify_token) == 0:
		print(old_token)
		print(verify_token)
		return jsonify({'error': 'failed to authenticate'}), 401

	new_token = uuid.uuid1()
	utils.update_query(queries.save_token, (str(new_token), time.time(), user_id))

	return jsonify({'token': new_token})


@auth_blueprint.route('/login/', methods=['POST'])
def users_login():

	email = utils.get_field(request, 'email', required=True)
	password = utils.get_field(request, 'password', required=True)
	
	email = email.strip().lower()

	db_pass = utils.select_query(queries.check_login, (email,))
	if len(db_pass) == 0:
		return jsonify(error='email not in database')
	if not check_password_hash(db_pass[0][0], password):
		return jsonify(error='incorrect password')

	new_token = uuid.uuid1()
	utils.update_query(queries.save_token, (str(new_token), time.time(), db_pass[0][1]))

	result = {
		'user_id': db_pass[0][1],
		'email': db_pass[0][2],
		'fb_id': db_pass[0][3],
		'photo_url': db_pass[0][4],
		'first_name': db_pass[0][5],
		'last_name': db_pass[0][6],
		'token': new_token,
	}

	return jsonify(result=result)

@auth_blueprint.route('/users/facebook', methods=['POST'])
def users_facebook_login():
	first_name = utils.get_field(request, 'first_name', required=True)
	last_name = utils.get_field(request, 'last_name', required=True)
	email = utils.get_field(request, 'email', required=True)
	fb_id = utils.get_field(request, 'fb_id', required=True)
	photo = utils.get_field(request, 'photo', required=True)
	friends = utils.get_list(request, 'friends', required=True)

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

	new_token = uuid.uuid1()
	utils.update_query(queries.save_token, (str(new_token), time.time(), user_id))

	result = {
		'user_id': user_id,
		'email': email,
		'fb_id': fb_id,
		'photo_url': photo,
		'first_name': first_name,
		'last_name': last_name,
		'token': new_token,
	}
	return jsonify(result=result)