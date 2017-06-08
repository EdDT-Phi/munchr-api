import requests
import os
from flask import jsonify, Blueprint, render_template, request
import datetime
import random

from utils import queries, utils
from restaurants.filters import filters
from restaurants.stars import is_starred, get_all_starred

google_base = 'https://maps.googleapis.com/maps/api/place/'
# minprice and maxprice and opennow
google_details = google_base + 'details/json?placeid=%s&key=%s'
google_search = google_base + 'nearbysearch/json?type=restaurant&key=%s&location=%f,%f&radius=%d&keyword=%s'
google_photos = google_base + 'photo?key=%s&photoreference=%s&maxheight=800&maxwidth=800'
google_text_search = google_base + 'textsearch/json?type=restaurant&radius=50000&key=%s&query=%s&location=%f,%f'
google_key = os.environ.get('GOOGLE_KEY')

# bing_images = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?q=%s&count=5'
# bing_key = os.environ.get('BING_KEY')


restaurants_blueprint = Blueprint('restaurants', __name__)


@restaurants_blueprint.route('/restaurants/filters/')
def get_filters():
	return jsonify(results=filters)

@restaurants_blueprint.route('/restaurants/search/', methods=['POST'])
def search_restaurants():

	lat = utils.get_float(request, 'lat', required=True)
	lng = utils.get_float(request, 'lng', required=True)
	query = utils.get_field(request, 'query', required=True)

	query = google_text_search % (google_key, query, lat, lng)
	print(query)

	resp = requests.get(query)
	data = resp.json()['results']

	results = []
	for res in data:
		results.append({
			'res_id': res['place_id'],
			'name': res['name'],
			'photo_url': google_photos % (google_key, res['photos'][0]['photo_reference']),
			'address': res['formatted_address']
			})
	return jsonify(results=results)

@restaurants_blueprint.route('/restaurants/details/', methods=['POST'])
def get_details():

	lat = utils.get_float(request, 'lat', required=True)
	lng = utils.get_float(request, 'lng', required=True)
	user_id = utils.get_num(request, 'user_id', required=True)
	res_id = utils.get_field(request, 'res_id', required=True)

	result = get_details_obj(user_id, res_id, lat, lng)
	return jsonify(result=result)


@restaurants_blueprint.route('/restaurants/', methods=['GET', 'POST'])
def get_restaurants():
	if request.method == 'GET':
		# return render_template('html', data=get_filters(30.3, -97.7))
		return render_template('html')

	lat = utils.get_float(request, 'lat', required=True)
	lng = utils.get_float(request, 'long', required=True)
	rad = utils.get_num(request, 'radius', 1, 20, required=True)
	cuisines = utils.get_list(request, 'cuisines')
	price = utils.get_num(request, 'price', required=True)
	user_id = utils.get_num(request, 'user_id', required=True)

	return get_restaurants(lat, lng, rad, price, cuisines, user_id)


def get_details_obj(user_id, res_id, lat, lng):
	query = google_details % (res_id, google_key)
	print(query)

	resp = requests.get(query)
	data = resp.json()['result']

	result = {
		'res_id': data['place_id'],
		'reviews': [],
		'photos': [],
		'phone': data['formatted_phone_number'],
		'website': data['website'],
		'price': -1,
		'name': data['name'],
		'rating': data['rating'],
		'location': {
			'address': data['vicinity'],
			'lat': data['geometry']['location']['lat'],
			'lng': data['geometry']['location']['lng'],
			'distance': utils.haversine(lat, lng, data['geometry']['location']['lat'],data['geometry']['location']['lng'])
		}
	}

	if 'opening_hours' in data:
		result['opennow'] = data['opening_hours']['open_now'],

	if 'price_level' in data:
		result['price'] = data['price_level']

	for review in data['reviews']:
		if review['rating'] > 3:
			result['reviews'].append({
					'rating': review['rating'],
					'review_text': review['text'],
					'review_time_friendly': format_time(review['time'])
				})
	for photo in data['photos']:
		result['photos'].append(google_photos % (google_key, photo['photo_reference']))

	result['starred'] = is_starred(user_id, res_id)
	return result

def format_time(time):
	return utils.time_to_text(datetime.datetime.fromtimestamp(time))


def get_restaurants(lat, lng, rad, price, cuisines, user_id):
	if cuisines is None: cuisines = []

	lists = []
	rad *= 1000
	if len(cuisines) == 0:
		cuisines = ['food']

	for cuisine in cuisines:
		query = google_search  % (google_key, lat, lng, rad, cuisine)
		lists.append(get_restaurants_by_cusine(query, lat, lng))

	results = []
	starred = get_all_starred(user_id)
	for i in range(max([len(lst) for lst in lists])):
		for lst in lists:
			if i < len(lst):
				res = lst[i]
				res['starred'] = (res['res_id'] in starred)
				results.append(lst[i])



	return jsonify(results=results)


def get_restaurants_by_cusine(query, lat, lng):
	print(query)

	resp = requests.get(query)
	data = resp.json()

	for res in data['results']:
		utils.update_query(queries.store_seen_ids, {'id': res['place_id'], 'name': res['name']})

	results = []
	for restaurant in data['results'][0:5]:
		r = restaurant
		if 'photos' not in r: continue

		e = random.randint(0, 2)
		mock_restaurants = ['The HighTower', 'Cool Beans']
		if e == 0:
			evidence = 'Because you liked %s' % mock_restaurants[random.randint(0, len(mock_restaurants)-1)]
		elif e == 1:
			evidence = 'Because %d of your friends liked this' % random.randint(2, 10)
		elif e == 2:
			evidence = 'Because users with similar taste liked this'

		results.append({
			'res_id': r['place_id'],
			'photo': google_photos % (google_key, restaurant['photos'][0]['photo_reference']),
			'name': r['name'],
			'location': {
				'address': r['vicinity'],
				'lat': r['geometry']['location']['lat'],
				'lon': r['geometry']['location']['lng']
			},
			'price_level': -1 if 'price_level' not in r else r['price_level'],
			'rating': -1 if 'rating' not in r else r['rating'],
			'distance': utils.haversine(float(lat), float(lng), r['geometry']['location']['lat'], r['geometry']['location']['lng']),
			'evidence': evidence
		})
	return results
