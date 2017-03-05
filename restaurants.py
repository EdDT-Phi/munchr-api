import requests
import os
from flask import jsonify
import utils
from filters import filters

google_base = 'https://maps.googleapis.com/maps/api/place/'
# minprice and maxprice and opennow
google_details = google_base + 'details/json?placeid=%s&key=%s'
google_search = google_base + 'nearbysearch/json?type=restaurant&language=en&rankby=prominence&'\
	'key=%s&location=%f,%f&radius=%d&keyword=%s'
google_photos = 'https://maps.googleapis.com/maps/api/place/photo?key=%s&photoreference=%s&maxheight=800&maxwidth=800'
google_key = os.environ.get('GOOGLE_KEY')

zomato_base = 'https://developers.zomato.com/api/v2.1/'
zomato_search = zomato_base + 'search?lat=%s&lon=%s&radius=%d&start=%d&count=%d'
zomato_reviews = zomato_base + 'reviews?res_id=%d'
zomato_cuisines = zomato_base + 'cuisines?lat=%s&lon=%s'
zomato_key = os.environ.get('ZOMATO_KEY')

bing_images = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?q=%s&count=5'
bing_key = os.environ.get('BING_KEY')

# zomato_cuisine_ids = {}
# zomato_category_ids = {
# 	'Delivery': '1',
# 	'Dine-out': '2',
# 	'Nightlife': '3',
# 	'Catching-up': '4',
# 	'Takeaway': '5',
# 	'Cafes': '6',
# 	'Daily Menus': '7',
# 	'Breakfast': '8',
# 	'Lunch': '9',
# 	'Dinner': '10',
# 	'Pubs & Bars': '11',
# 	'Premium Delivery': '12',
# 	'Pocket Friendly Delivery': '13',
# 	'Clubs & Lounges': '14'
# }

def get_reviews(res_id):
	headers = {
		'user-key': zomato_key
	}
	resp = requests.get(zomato_reviews % res_id, headers=headers)
	data = resp.json()

	results = []
	for review in data['user_reviews']:
		review = review['review']
		results.append({
				'rating': review['rating'],
				'review_text': review['review_text'],
				'review_time_friendly': review['review_time_friendly']
			})

	return jsonify(results=results)

def get_details(res_id):

	query = google_details % (res_id, google_key);
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

	return jsonify(results=results)


def get_photos(query):
	headers = {
		'Ocp-Apim-Subscription-Key': bing_key
	}
	resp = requests.get(bing_images % query, headers=headers)
	data = resp.json()


	results = [img['contentUrl'] for img in data['value']]

	return jsonify(results=results)


def get_filters(lat, lng):
	headers = {
		'user-key': os.environ.get('ZOMATO_KEY')
	}
	resp = requests.get(zomato_cuisines % (lat, lng), headers=headers)
	data = resp.json()
	results = []
	for cuisine in data['cuisines']:
		results.append(cuisine['cuisine']['cuisine_name'])
		# zomato_cuisine_ids[cuisine['cuisine']['cuisine_name']] = str(cuisine['cuisine']['cuisine_id'])

	return jsonify(results=results)


def get_restaurants2(lat, lng, rad, price, limit=5, offset=0, cuisines=[], categories=[]):
	if cuisines is None: cuisines = []
	if categories is None: categories = []
	
	query = google_search % (google_key, float(lat), float(lng), rad*1000, '%20'.join(cuisines+categories))

	# zomato takes readius in meters
	resp = requests.get(query)


	print(query)

	data = resp.json()


	results = []
	for restaurant in data['results'][:7]:
		r = restaurant
		if 'photos' not in r: continue

		# print(r['location']['latitude'])
		# print(r['location']['longitude'])

		results.append({
			'id': r['place_id'],
			'photo': google_photos % (google_key, restaurant['photos'][0]['photo_reference']),
			'name': r['name'],
			'cuisines': r['types'],
			# 'cost': r['average_cost_for_two'],
			'location': {
				'locality': r['vicinity'],
				'address': r['vicinity'],
				'lat': r['geometry']['location']['lat'],
				'lon': r['geometry']['location']['lng']
			},
			'rating': r['rating'],
			'distance': utils.haversine(float(lat), float(lng), r['geometry']['location']['lat'], r['geometry']['location']['lng'])
		})

	return jsonify(results=results)

def get_restaurants(lat, lng, rad, price, limit=5, offset=0, cuisines=None, categories=None):
	# TODO add to database. if no results, query db
	print('args: ', lat, lng, rad, price, cuisines, categories)

	# resp = requests.get(google_url % (lat, lng, rad, kwrd, min_price, max_price, key))
	query = zomato_search  % (lat, lng, rad * 1000, offset, limit)

	if cuisines is not None:
		query += '&cuisines=' + ','.join([zomato_cuisine_ids[cuisine.strip()] for cuisine in cuisines])
	if categories is not None:
		query += '&category=' + ','.join([zomato_category_ids[category.strip()] for category in categories])

	# call zomato api
	headers = {
		'user-key': zomato_key
	}

	# zomato takes readius in meters
	resp = requests.get(query, headers=headers)


	print(query)

	data = resp.json()
	# print(data)

	results = []
	for restaurant in data['restaurants']:
		r = restaurant['restaurant']
		if r['featured_image'] == '': continue

		# print(r['location']['latitude'])
		# print(r['location']['longitude'])

		results.append({
			'id': r['id'],
			'photo': r['featured_image'],  # photos_url % (key, restaurant['photos'][0]['photo_reference']),
			'name': r['name'],
			'cuisines': r['cuisines'],
			'cost': r['average_cost_for_two'],
			'location': {
				'locality': r['location']['locality'],
				'address': r['location']['address'],
				'lat': r['location']['latitude'],
				'lon': r['location']['longitude']
			},
			'rating': r['user_rating']['aggregate_rating'],
			'distance': utils.haversine(float(lat), float(lng), float(r['location']['latitude']), float(r['location']['longitude']))
		})

	return jsonify(results=results)


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
