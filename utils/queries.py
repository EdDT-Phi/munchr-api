# Friends queries
verify_users = 'SELECT user_id FROM users WHERE user_id=%d OR user_id=%d'
are_friends = 'SELECT user_id1, user_id2 FROM friends WHERE user_id1=%s AND user_id2=%s'

add_friend = 'INSERT INTO friends (user_id1, user_id2) VALUES (%d, %d)'
remove_friend = 'DELETE FROM friends WHERE (user_id1 = %(u1)s AND user_id2 = %(u2)s) OR (user_id1 = %(u2)s AND user_id2 = %(u1)s);'
view_friends = 'SELECT user_id, first_name, last_name, photo_url FROM friends JOIN users ON user_id = user_id2 WHERE user_id1 = %s'

view_friend_requests = 'SELECT user_id, first_name, last_name, photo_url FROM friend_requests JOIN users ON user_id = user_from_id WHERE user_to_id = %s'
delete_request = 'DELETE FROM friend_requests WHERE user_from_id = %s AND user_to_id = %s'
friend_request = 'INSERT INTO friend_requests (user_from_id, user_to_id) VALUES (%s, %s)';
accept_request = 'INSERT INTO friends (user_id1, user_id2) VALUES (%(user_id1)s, %(user_id2)s), (%(user_id2)s, %(user_id1)s);'

requested = 'SELECT user_from_id, user_to_id FROM friend_requests WHERE (user_from_id = %(u1)s AND user_to_id = %(u2)s) OR (user_from_id = %(u2)s AND user_to_id = %(u1)s)'
# Search queries
# search_friends = 'SELECT user_id, first_name, last_name, email FROM friends JOIN users ON user_id2 = user_id ' \
#                  'WHERE user_id1 = %d AND (first_name = %s OR last_name = %sOR email LIKE %s%% ' \
#                  'OR first_name LIKE %s%% OR last_name LIKE %s%%)'
search_all = 'SELECT user_id, first_name, last_name, photo_url FROM users ' \
             'WHERE (first_name = %s OR last_name = %s OR email LIKE %s ' \
             'OR first_name LIKE %s OR last_name LIKE %s) LIMIT 10;'

# User Queries
new_user = 'INSERT INTO users (first_name, last_name, email, password) ' \
           'VALUES (%s, %s, %s, %s) RETURNING user_id'
new_fb_user = 'INSERT INTO users (first_name, last_name, fb_id, email, photo_url) ' \
           'VALUES (%s, %s, %s, %s, %s) RETURNING user_id'
update_user = 'UPDATE users SET first_name = %s, last_name = %s, fb_id = %s, photo_url = %s WHERE email = %s RETURNING user_id'

fb_to_user_id = 'SELECT user_id from users where fb_id IN %s AND user_id NOT IN (SELECT user_id2 from friends where user_id1 = %s);'
facebook_friends = 'INSERT INTO friends (user_id1, user_id2) VALUES '

show_all_users = 'SELECT first_name, last_name, fb_id, email, user_id from users ORDER BY user_id DESC'
show_user_id = 'SELECT first_name, last_name, fb_id, email from users WHERE user_id = %d'
show_user_email = 'SELECT first_name, last_name, fb_id, email, user_id from users WHERE email = %s'

# Login
check_login = 'SELECT password, user_id, email, fb_id, photo_url, first_name, last_name FROM users WHERE email = %s'

# Cuisine QA
store_seen_ids = 'INSERT INTO restaurants (res_id, res_name) SELECT %(id)s, %(name)s WHERE NOT EXISTS (SELECT res_id FROM restaurants where res_id = %(id)s);'
null_cuisines = 'SELECT res_id FROM restaurants WHERE cuisine IS NULL LIMIT 1'
update_cuisines = 'UPDATE restaurants SET cuisine = %s WHERE res_id = %s'

# User Ratings
store_new_rating = 'INSERT INTO user_ratings (user_id, res_id, liked, specific, review_date) VALUES (%s, %s, %s, %s, %s);'
get_friends_activity = 'SELECT first_name, last_name, photo_url, liked, res_name, user_ratings.res_id, review_date, user_ratings.user_id FROM user_ratings JOIN friends ON user_ratings.user_id = friends.user_id2 JOIN restaurants ON user_ratings.res_id = restaurants.res_id JOIN users on users.user_id = user_ratings.user_id WHERE friends.user_id1 = %s ORDER BY review_date DESC LIMIT 10;'
get_activity = 'SELECT first_name, last_name, photo_url, liked, res_name, user_ratings.res_id, review_date FROM user_ratings JOIN users ON user_ratings.user_id = users.user_id JOIN restaurants ON user_ratings.res_id = restaurants.res_id WHERE user_ratings.user_id = %s;'

# Recommendations
new_recommendation = 'INSERT INTO recommendations (user_from_id, user_to_id, res_id) VALUES '
get_recommendations = 'SELECT first_name, last_name, photo_url, user_from_id, restaurants.res_id, res_name FROM recommendations  JOIN users on user_from_id = users.user_id JOIN restaurants on recommendations.res_id = restaurants.res_id WHERE user_to_id = %s'
delete_recommendation = 'DELETE FROM recommendations WHERE user_from_id = %s AND user_to_id = %s AND res_id = %s'
