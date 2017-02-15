import utils
import requests
import os
from flask import jsonify

radius_conv = {1: 1000, 2: 5000, 3: 10000}
# google_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=%d&keyword=%s&
# minprice=%d&maxprice=%dtype=restaurant&opennow=true&key=%s'
# photos_url = 'https://maps.googleapis.com/maps/api/place/photo?key=%s&photoreference=%s&maxheight=800&maxwidth=800'
zomato_search = 'https://developers.zomato.com/api/v2.1/search?lat=%s&lon=%s&radius=%d&sort=%s'
zomato_categories = 'https://developers.zomato.com/api/v2.1/categories'
zomato_cuisines = 'https://developers.zomato.com/api/v2.1/cuisines?lat=%s&lon=%s'


def filters_object(lat=30.3, lng=-97.7):
	headers = {
		'user-key': os.environ.get('ZOMATO_KEY')
	}
	resp = requests.get(zomato_cuisines % (lat, lng), headers=headers)
	data = resp.json()
	results = {
		'cuisines': []
	}
	for cuisine in data['cuisines']:
		results['cuisines'].append(cuisine['cuisine']['cuisine_name'])

	results['categories'] = get_categories()
	return results


def get_filters(lat=30.3, lng=-97.7):
	return jsonify(results=filters_object(lat, lng))


def get_categories():
	headers = {
		'user-key': os.environ.get('ZOMATO_KEY')
	}
	resp = requests.get(zomato_categories, headers=headers)
	data = resp.json()
	results = []
	for category in data['categories']:
		results.append(category['categories']['name'])

	return results


def get_restaurants(lat, lng, rad, cuisines, categories, price):

	# call google api
	# rad = radius_conv[rad]
	# resp = requests.get(google_url % (lat, lng, rad, kwrd, min_price, max_price, key))

	# call zomato api
	headers = {
		'user-key': os.environ.get('ZOMATO_KEY')
	}
	resp = requests.get(zomato_search % (lat, lng, rad, 'price'), headers=headers)

	data = resp.json()
	print(data)

	results = []
	for restaurant in data['restaurants']:
		r = restaurant['restaurant']
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
			'rating': r['user_rating']['aggregate_rating']

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
