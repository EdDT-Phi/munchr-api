# Friends queries
verify_users = 'SELECT user_id FROM users WHERE user_id=%d OR user_id=%d'
check_not_already_friends = 'SELECT user_id1, user_id2 FROM friends WHERE user_id1=%d AND user_id2=%d'
add_friend = 'INSERT INTO friends (user_id1, user_id2) VALUES (%d, %d)'

view_friends = 'SELECT user_id, first_name, last_name FROM friends JOIN users ON user_id = user_id2 WHERE user_id1 = %d'
added_me = 'SELECT user_id, first_name, last_name FROM friends JOIN users ON user_id = user_id1 WHERE user_id2 = %d %s'

# Search queries
search_friends = 'SELECT user_id, first_name, last_name, email FROM friends JOIN users ON user_id2 = user_id ' \
                 'WHERE user_id1 = %d AND (first_name = \'%s\' OR last_name = \'%s\'OR email LIKE \'%s%%\' ' \
                 'OR first_name LIKE \'%s%%\' OR last_name LIKE \'%s%%\')'
search_all = 'SELECT user_id, first_name, last_name, email FROM users ' \
             'WHERE (first_name = \'%s\' OR last_name = \'%s\'OR email LIKE \'%s%%\' ' \
             'OR first_name LIKE \'%s%%\' OR last_name LIKE \'%s%%\')'

# User Queries
new_user = 'INSERT INTO users (first_name, last_name, fb_id, email, password) ' \
           'VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'
show_all_users = 'SELECT first_name, last_name, fb_id, email, user_id from users ORDER BY user_id DESC'
show_user = 'SELECT first_name, last_name, fb_id, email from users WHERE user_id = %d'

check_login = 'SELECT password, user_id, email, fb_id, photo_url, first_name, last_name FROM users WHERE email = \'%s\''
