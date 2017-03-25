# Friends queries
verify_users = 'SELECT user_id FROM users WHERE user_id=%d OR user_id=%d'
check_not_already_friends = 'SELECT user_id1, user_id2 FROM friends WHERE user_id1=%d AND user_id2=%d'
add_friend = 'INSERT INTO friends (user_id1, user_id2) VALUES (%d, %d)'

view_friends = 'SELECT user_id, first_name, last_name FROM friends JOIN users ON user_id = user_id2 WHERE user_id1 = %d'
added_me = 'SELECT user_id, first_name, last_name FROM friends JOIN users ON user_id = user_id1 WHERE user_id2 = %d %s'

# Search queries
# search_friends = 'SELECT user_id, first_name, last_name, email FROM friends JOIN users ON user_id2 = user_id ' \
#                  'WHERE user_id1 = %d AND (first_name = %s OR last_name = %sOR email LIKE %s%% ' \
#                  'OR first_name LIKE %s%% OR last_name LIKE %s%%)'
# search_all = 'SELECT user_id, first_name, last_name, email FROM users ' \
#              'WHERE (first_name = %s OR last_name = %sOR email LIKE %s%% ' \
#              'OR first_name LIKE %s%% OR last_name LIKE %s%%)'

# User Queries
new_user = 'INSERT INTO users (first_name, last_name, email, password) ' \
           'VALUES (%s, %s, %s, %s) RETURNING user_id'
new_fb_user = 'INSERT INTO users (first_name, last_name, fb_id, email, photo_url) ' \
           'VALUES (%s, %s, %s, %s, %s) RETURNING user_id'
update_user = 'UPDATE users SET first_name = %s, last_name = %s, fb_id = %s, photo = %s WHERE email = %s RETURNING user_id'
show_all_users = 'SELECT first_name, last_name, fb_id, email, user_id from users ORDER BY user_id DESC'
show_user_id = 'SELECT first_name, last_name, fb_id, email from users WHERE user_id = %d'
show_user_email = 'SELECT first_name, last_name, fb_id, email from users WHERE email = %s'

check_login = 'SELECT password, user_id, email, fb_id, photo_url, first_name, last_name FROM users WHERE email = %s'

# Cuisine QA
store_seen_ids = 'INSERT INTO restaurants (res_id, res_name) SELECT %(id)s, %(name)s WHERE NOT EXISTS (SELECT res_id FROM restaurants where res_id = %(id)s);'
null_cuisines = 'SELECT res_id FROM restaurants WHERE cuisine IS NULL LIMIT 1'
update_cuisines = 'UPDATE restaurants SET cuisine = %s WHERE res_id = %s'

# User Ratings
store_new_rating = 'INSERT INTO user_ratings (user_id, res_id, liked, specific, review_date) VALUES (%s, %s, %s, %s, %s);'
get_activity = 'SELECT first_name, last_name, photo_url, liked, res_name, review_date, users.user_id FROM user_ratings JOIN users ON user_ratings.user_id = users.user_id JOIN restaurants ON user_ratings.res_id = restaurants.res_id'