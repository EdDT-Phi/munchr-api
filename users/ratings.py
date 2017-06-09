from flask import Blueprint, render_template, request, jsonify
from utils import queries, utils
from restaurants.restaurants import get_details_obj
from restaurants.filters import filters
from users.friends import are_friends, requested, get_friends_list

ratings_blueprint = Blueprint('ratings', __name__)

@ratings_blueprint.route('/users/rating/', methods=['POST'])
def user_rating():
	rating_id = utils.get_num(request, 'rating_id', required=True)
	user_id = utils.get_num(request, 'user_id', required=True)
	liked = utils.get_field(request, 'liked', required=True)
	specific = utils.get_field(request, 'specific')

	# save rating
	utils.update_query(queries.rate_munch, (liked, specific, rating_id))

	# recommend to friends
	if liked:
		friends = get_friends_list(user_id)
		items = ','.join(['(%s, %s,\'%s\')' % (user_id, friend['user_id'], res_id) for friend in friends])
		utils.update_query(queries.new_recommendation + items)

	return jsonify(result={'success': True})


@ratings_blueprint.route('/users/munch/', methods=['POST'])
def user_munch():
	user_id = utils.get_field(request, 'user_id', required=True)
	res_id = utils.get_field(request, 'res_id', required=True)

	# save rating
	utils.update_query(queries.store_new_munch, (user_id, res_id))

	return jsonify(result={'success': True})


@ratings_blueprint.route('/users/activity/friends/<int:user_id>')
def get_friends_activity(user_id):
	ratings = utils.select_query(queries.get_friends_activity, (user_id,))
	results = []
	utils.add_rows_to_list(ratings, results, ('first_name', 'last_name', 'photo_url', 'liked', 'res_name', 'res_id', 'review_date', 'user_id'))

	for i in range(len(results)):
		results[i]['review_date'] = utils.time_to_text(results[i]['review_date'])

	return jsonify(results=results)

@ratings_blueprint.route('/users/activity/<int:user_id>/<int:other_id>')
def get_activity(user_id, other_id):
	result = {
		'activity': [],
		'type': None
	}


	if user_id == other_id:
		result['type'] = 'self'
	elif are_friends(user_id, other_id):
		result['type'] = 'friend'

	if result['type'] is not None:
		ratings = utils.select_query(queries.get_activity, (other_id,))
		utils.add_rows_to_list(ratings, result['activity'], ('rating_id', 'first_name', 'last_name', 'photo_url', 'liked', 'res_name', 'res_id', 'review_date'))

		for i in range(len(result['activity'])):
			result['activity'][i]['review_date'] = utils.time_to_text(result['activity'][i]['review_date'])

	else:
		result['type'] = str(requested(user_id, other_id))

	return jsonify(result=result)
