from flask import Blueprint, render_template, request, jsonify
from utils import queries, utils
from restaurants.restaurants import get_details_obj
from restaurants.filters import filters
from datetime import datetime

ratings_blueprint = Blueprint('ratings', __name__)

@ratings_blueprint.route('/users/rating/', methods=['POST'])
def user_rating():
	user_id = utils.get_field(request, 'user_id', required=True)
	res_id = utils.get_field(request, 'res_id', required=True)
	liked = utils.get_field(request, 'liked', required=True)
	specific = utils.get_field(request, 'specific')

	utils.update_query(queries.store_new_rating, (user_id, res_id, liked, specific, datetime.now(),))

	return jsonify(result={'success': True})

@ratings_blueprint.route('/users/activity/friends/<int:user_id>')
def get_friends_activity(user_id):
	ratings = utils.select_query(queries.get_friends_activity, (user_id,))
	results = []
	utils.add_rows_to_list(ratings, results, ('first_name', 'last_name', 'photo_url', 'liked', 'res_name', 'review_date', 'user_id'))

	for i in range(len(results)):
		results[i]['review_date'] = time_to_text(datetime.now() - results[i]['review_date'])

		# if user_id == results[i]['user_id']:
		# 	results[i]['first_name'] = 'You'
		# 	results[i]['last_name'] = ''

		# del results[i]['user_id']

	return jsonify(results=results)

@ratings_blueprint.route('/users/activity/<int:user_id>')
def get_activity(user_id):
	ratings = utils.select_query(queries.get_activity, (user_id,))
	results = []
	utils.add_rows_to_list(ratings, results, ('first_name', 'last_name', 'photo_url', 'liked', 'res_name', 'review_date'))

	for i in range(len(results)):
		results[i]['review_date'] = time_to_text(datetime.now() - results[i]['review_date'])
		

		# if user_id == results[i]['user_id']:
		# 	results[i]['first_name'] = 'You'
		# 	results[i]['last_name'] = ''

		# del results[i]['user_id']

	return jsonify(results=results)

def time_to_text(ago):
	if ago.days > 1:
		return '%d days ago' % ago.days
	elif ago.days == 1:
		return 'Yesterday'
	elif ago.seconds >= 60*60:
		hrs = ago.seconds // (60*60)
		sing = 'hour'
		if hrs > 1:
			sing += 's'
		return '%d %s ago' % (hrs, sing)
	elif ago.seconds > 60:
		return 'A few minutes ago'
	else:
		return 'A few seconds ago'	
