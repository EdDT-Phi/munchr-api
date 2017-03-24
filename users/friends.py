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


def get_friends(user_id):
	resp = utils.select_query(queries.view_friends % user_id)
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


def new_friend(user_id1, user_id2):

	if user_id1 == user_id2:
		return jsonify(error='cannot befriend self')

	# if user_id1 is None or user_id2 is None:
		# return jsonify(error='must provide valid user_ids')

	# Verfiy users exist
	resp = utils.select_query(queries.verify_users % (user_id1, user_id2))
	if len(resp) != 2:
		return jsonify(error='one or both user_ids do not exist')

	# Verify users not friends
	resp = utils.select_query(queries.check_not_already_friends % (user_id1, user_id2))
	if len(resp) != 0:
		return jsonify(error='users already friends')

	# Add friend
	utils.update_query(queries.add_friend, (user_id1, user_id2))

	return jsonify(success=True)

def get_friends(user_id):
	resp = utils.select_query(queries.view_friends % user_id)
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


def new_friend(user_id1, user_id2):

	if user_id1 == user_id2:
		return jsonify(error='cannot befriend self')

	# if user_id1 is None or user_id2 is None:
		# return jsonify(error='must provide valid user_ids')

	# Verfiy users exist
	resp = utils.select_query(queries.verify_users % (user_id1, user_id2))
	if len(resp) != 2:
		return jsonify(error='one or both user_ids do not exist')

	# Verify users not friends
	resp = utils.select_query(queries.check_not_already_friends % (user_id1, user_id2))
	if len(resp) != 0:
		return jsonify(error='users already friends')

	# Add friend
	utils.update_query(queries.add_friend, (user_id1, user_id2))

	return jsonify(success=True)

