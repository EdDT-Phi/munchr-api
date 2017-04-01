import json
from flask import jsonify, Response, Blueprint, request, render_template
from utils import queries, utils

friends_blueprint = Blueprint('friends', __name__)

@friends_blueprint.route('/friends/', methods=['GET', 'POST'])
@friends_blueprint.route('/friends/<int:user_id>')
def friends(user_id=None):
    if user_id is None and request.method == 'GET':
        return render_template('new_friend.html')

    if request.method == 'POST':
        user_id1 = utils.get_num(request, 'user_id1', required=True)
        user_id2 = utils.get_num(request, 'user_id2', required=True)

        return new_friend(user_id1, user_id2)

    return get_friends(user_id)

@friends_blueprint.route('/friends/respond/', methods=['POST'])
def friends_respond():
	user_id = utils.get_num(request, 'user_id', required=True)
	oth_id = utils.get_num(request, 'oth_id', required=True)
	response = utils.get_boolean(request, 'response', required=True)

	return respond_request(response, user_id, oth_id)


def get_friends(user_id):
	friends = []
	rows = utils.select_query(queries.view_friends, (user_id,))
	utils.add_rows_to_list(rows, friends, ('user_id', 'first_name', 'last_name', 'photo_url'))

	requests = []
	rows = utils.select_query(queries.view_friend_requests, (user_id,))
	utils.add_rows_to_list(rows, requests, ('user_id', 'first_name', 'last_name', 'photo_url'))

	return jsonify(result={'friends': friends, 'requests': requests})


def new_friend(user_id1, user_id2):

	if user_id1 == user_id2:
		return jsonify(error='cannot befriend self')

	# if user_id1 is None or user_id2 is None:
		# return jsonify(error='must provide valid user_ids')

	# Verfiy users exist
	resp = utils.select_query(queries.verify_users, (user_id1, user_id2))
	if len(resp) != 2:
		return jsonify(error='one or both user_ids do not exist')

	# Verify users not friends
	resp = utils.select_query(queries.check_not_already_friends, (user_id1, user_id2))
	if len(resp) != 0:
		return jsonify(error='users already friends')

	# Add friend
	utils.update_query(queries.add_friend, (user_id1, user_id2))

	return jsonify(success=True)

def respond_request(response, user_id, oth_id):
	# delete request
	utils.update_query(queries.delete_request, (oth_id, user_id))
	if response:
		# add friend
		utils.update_query(queries.accept_request, {'user_id1': user_id, 'user_id2': oth_id})

	return get_friends(user_id)