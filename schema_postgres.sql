﻿SELECT first_name, last_name, photo_url, liked, res_name, review_date FROM user_ratings JOIN users ON user_ratings.user_id = users.user_id JOIN restaurants ON user_ratings.res_id = restaurants.res_id