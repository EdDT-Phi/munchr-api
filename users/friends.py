import json
from flask import jsonify, Response, Blueprint, request, render_template
from utils import queries, utils

friends_blueprint = Blueprint('friends', __name__)

@friends_blueprint.route('/friends/delete/', methods=['POST'])
def delete_friend():
	user_id1 = utils.get_num(request, 'user_id1', required=True)
	user_id2 = utils.get_num(request, 'user_id2', required=True)
	utils.update_query(queries.remove_friend, {'u1': user_id1, 'u2': user_id2})

	return jsonify(success=True)


@friends_blueprint.route('/friends/', methods=['POST'])
@friends_blueprint.route('/friends/<int:user_id>')
def friends(user_id=None):
	if user_id is not None:
		friends = get_friends_list(user_id)

		requests = get_friend_requests(user_id)
		return jsonify(result={'friends': friends, 'requests': requests})

	user_from_id = utils.get_num(request, 'user_from_id', required=True)
	user_to_id = utils.get_num(request, 'user_to_id', required=True)

	utils.update_query(queries.friend_request, (user_from_id, user_to_id))

	return jsonify(success=True)

@friends_blueprint.route('/friends/respond/', methods=['POST'])
def friends_respond():
	user_id = utils.get_num(request, 'user_id', required=True)
	oth_id = utils.get_num(request, 'oth_id', required=True)
	response = utils.get_boolean(request, 'response', required=True)

	# delete request
	utils.update_query(queries.delete_request, (oth_id, user_id))
	if response:
		# add friend
		utils.update_query(queries.accept_request, {'user_id1': user_id, 'user_id2': oth_id})

	return friends(user_id)

def are_friends(user_id1, user_id2):
	rows = utils.select_query(queries.are_friends, (user_id1, user_id2))
	return len(rows) != 0

def requested(user_id1, user_id2):
	rows = utils.select_query(queries.requested, {'u1': user_id1, 'u2': user_id2})
	if len(rows) == 0:
		return None

	row = rows[0]
	if row[0] == user_id1:
		return 'requester'
	return 'requested'

def get_friend_requests(user_id):
	requests = []
	rows = utils.select_query(queries.view_friend_requests, (user_id,))
	utils.add_rows_to_list(rows, requests, ('user_id', 'first_name', 'last_name', 'photo_url'))
	return requests

def get_friends_list(user_id):
	friends = []
	rows = utils.select_query(queries.view_friends, (user_id,))
	utils.add_rows_to_list(rows, friends, ('user_id', 'first_name', 'last_name', 'photo_url'))
	return friends