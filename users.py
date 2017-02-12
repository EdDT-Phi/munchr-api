import json

from flask import jsonify, Response
from flask_bcrypt import generate_password_hash

import queries
import utils


class Users:
	"""docstring for Users"""
	def __init__(self, conn, bcrypt):
		self.conn = conn
		self.bcrypt = bcrypt

	def login(self, email, password):

		db_pass = utils.select_query(queries.check_login % email, self.conn)
		if len(db_pass) == 0:
			return jsonify(error='email not in database')
		if not self.bcrypt.check_password_hash(db_pass[0][0], password):
			return jsonify(error='incorrect password')

		return jsonify(success=True, user_id=db_pass[0][1])

	def new_user(self, first_name, last_name, email, password, fb_id):

		if password is None:
			if fb_id is None: return jsonify(error='password or fb_id required')
		else:
			password = generate_password_hash(password, 12)

		first_name = utils.to_name(first_name)
		last_name = utils.to_name(last_name)
		email = email.lower()

		# print('%s\n%s\n%s\n%s\n%s\n%s' % (first_name, last_name, fb_id, email, password.decode('UTF-8')))
		utils.insert_query(queries.new_user % (first_name, last_name, fb_id, email, password.decode('UTF-8')), self.conn)

		return jsonify(success=True)

	def search_users(self, query, user_id):

		query = query.lower()
		results = []
		# search among friends
		# rows = utils.select_query(
		# search_friends %
		# (user_id, utils.to_name(query), utils.to_name(query), query, utils.to_name(query), utils.to_name(query)))
		# add_rows_to_list(rows, results, ('user_id', 'first_name', 'last_name', 'email'))

		# search among friends' friends

		# search among all users
		rows = utils.select_query(queries.search_all % (
		utils.to_name(query), utils.to_name(query), query, utils.to_name(query), utils.to_name(query)), self.conn)
		utils.add_rows_to_list(rows, results, ('user_id', 'first_name', 'last_name', 'email'))
		return Response(json.dumps(results), mimetype='application/json')

	def get_friends(self, user_id):
		resp = utils.select_query(queries.view_friends % user_id, self.conn)
		friends = []
		utils.add_rows_to_list(resp, friends, ('user_id', 'first_name', 'last_name'))

		print(friends)
		print(','.join([str(friend['user_id']) for friend in friends]))
		if len(friends) == 0:
			ls = ''
		else:
			ls = 'AND NOT (user_id in (%s))' % (','.join([str(friend['user_id']) for friend in friends]))

		resp = utils.select_query(queries.added_me % (user_id, ls))
		non_friends = []
		utils.add_rows_to_list(resp, non_friends, ('user_id', 'first_name', 'last_name'))

		return Response(json.dumps({'friends': friends, 'non_friends': non_friends}), mimetype='application/json')

	def new_friend(self, user_id1, user_id2):

		if user_id1 == user_id2:
			return jsonify(error='cannot befriend self')

		if user_id1 is None or user_id2 is None:
			return jsonify(error='must provide valid user_ids')

		# Verfiy users exist
		resp = utils.select_query(queries.verify_users % (user_id1, user_id2), self.conn)
		if len(resp) != 2:
			return jsonify(error='one or both user_ids do not exist')

		# Verify users not friends
		resp = utils.select_query(queries.check_not_already_friends % (user_id1, user_id2), self.conn)
		if len(resp) != 0:
			return jsonify(error='users already friends')

		# Add friend
		utils.insert_query(queries.add_friend % (user_id1, user_id2), self.conn)

		return jsonify(success=True)

	def get_all_users(self):
		rows = utils.select_query(queries.show_all_users, self.conn)
		result = []
		utils.add_rows_to_list(rows, result, ('first_name', 'last_name', 'fb_id', 'email', 'user_id'))
		return Response(json.dumps(result),  mimetype='application/json')

	def get_user(self, user_id):
		rows = utils.select_query(queries.show_user % user_id, self.conn)
		if len(rows) == 0:
			return jsonify(error='No user with that id')
		result = []
		utils.add_rows_to_list(rows, result, ('first_name', 'last_name', 'fb_id', 'email'))
		return Response(json.dumps(result),  mimetype='application/json')
