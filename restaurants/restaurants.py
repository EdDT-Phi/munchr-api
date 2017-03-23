import requests
import os
from flask import jsonify

from utils import queries, utils
from restaurants.filters import filters

google_base = 'https://maps.googleapis.com/maps/api/place/'
# minprice and maxprice and opennow
google_details = google_base + 'details/json?placeid=%s&key=%s'
google_search = google_base + 'nearbysearch/json?type=restaurant&language=en&rankby=prominence&'\
	'key=%s&location=%f,%f&radius=%d&keyword=%s'
google_photos = 'https://maps.googleapis.com/maps/api/place/photo?key=%s&photoreference=%s&maxheight=800&maxwidth=800'
google_key = os.environ.get('GOOGLE_KEY')

bing_images = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?q=%s&count=5'
bing_key = os.environ.get('BING_KEY')


def get_filters():
	return jsonify(results=filters)


def get_details_obj(res_id):
	query = google_details % (res_id, google_key)
	print(query)

	resp = requests.get(query)
	data = resp.json()['result']

	results = {
		'reviews': [],
		'photos': [],
		'phone': data['formatted_phone_number'],
		'opennow': data['opening_hours']['open_now'],
		'website': data['website'],
		'price': -1,
		'name': data['name']
	}


	if 'price_level' in data:
		results['price'] = data['price_level']

	for review in data['reviews']:
		results['reviews'].append({
				'rating': review['rating'],
				'review_text': review['text'],
				'review_time_friendly': review['time']
			})
	for photo in data['photos']:
		results['photos'].append(google_photos % (google_key, photo['photo_reference']))

	return results


def get_details(res_id):
	results = get_details_obj(res_id)
	return jsonify(results=results)


def get_restaurants(lat, lng, rad, price, cuisines):
	if cuisines is None: cuisines = []

	lists = []
	rad *= 1000
	if len(cuisines) == 0:
		cuisines = ['food']

	for cuisine in cuisines:
		query = google_search  % (google_key, lat, lng, rad, cuisine)
		lists.append(get_restaurants_by_cusine(query, lat, lng))

	results = []
	for i in range(max([len(lst) for lst in lists])):
		for lst in lists:
			if i < len(lst):
				results.append(lst[i])

	return jsonify(results=results)


def get_restaurants_by_cusine(query, lat, lng):
	print(query)

	resp = requests.get(query)
	data = resp.json()

	for res in data['results']:
		utils.update_query(queries.store_seen_ids, {'id': res['place_id']})

	results = []
	for restaurant in data['results'][0:5]:
		r = restaurant
		if 'photos' not in r: continue

		results.append({
			'id': r['place_id'],
			'photo': google_photos % (google_key, restaurant['photos'][0]['photo_reference']),
			'name': r['name'],
			'location': {
				'address': r['vicinity'],
				'lat': r['geometry']['location']['lat'],
				'lon': r['geometry']['location']['lng']
			},
			'price_level': -1 if 'price_level' not in r else r['price_level'],
			'rating': -1 if 'rating' not in r else r['rating'],
			'distance': utils.haversine(float(lat), float(lng), r['geometry']['location']['lat'], r['geometry']['location']['lng'])
		})
	return results


def swipe_restaurant():
	# liked = utils.get_boolean(request, 'liked', required=True)
	# restaurant_id = utils.get_num(request, 'restaurant_id', required=True)
	# user_id = utils.get_num(request, 'user_id', required=True)

	# resp = utils.modify_query(swipe_restaurant % ())
	return jsonify(success=True)


def rate_restaurant():
	# restaurant_id = utils.get_num(request, 'restaurant_id', required=True)
	# user_id = utils.get_num(request, 'user_id', required=True)
	# overall_rating = utils.get_num(request, 'overall_rating', 1, 5, required=True)
	# food_rating = utils.get_num(request, 'food_rating', 1, 5)
	# value_rating = utils.get_num(request, 'value_rating', 1, 5)
	# service_rating = utils.get_num(request, 'service_rating', 1, 5)
	# location_rating = utils.get_num(request, 'location_rating', 1, 5)
	# atmosphere_rating = utils.get_num(request, 'atmosphere_rating', 1, 5)

	# resp = utils.modify_query(rate_restaurant % ())
	return jsonify(success=True)
