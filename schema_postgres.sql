DROP TABLE IF EXISTS users;
CREATE TABLE users (
	user_id     serial UNIQUE NOT NULL,
	fb_id       text,
	first_name  text NOT NULL,
	last_name   text NOT NULL,
	email       text UNIQUE NOT NULL,
	password    text,
	photo_url   text,
	PRIMARY KEY (user_id)
);


-- DROP TABLE IF EXISTS user_ratings;
-- CREATE TABLE user_ratings (
-- 	user_id 	int NOT NULL,
-- 	res_id 		text NOT NULL,
-- 	liked		boolean NOT NULL,
-- 	specific	text,
-- 	review_date timestamp DEFAULT current_timestamp
-- );


-- DROP TABLE IF EXISTS user_swipes;
-- CREATE TABLE user_swipes (
-- 	user_id		int NOT NULL,
-- 	res_id 		int NOT NULL,
-- 	swipe_score float DEFAULT 0
-- );


DROP TABLE IF EXISTS friends;
CREATE TABLE friends (
	user_id1    int NOT NULL,
	user_id2    int NOT NULL
);


DROP TABLE IF EXISTS friend_requests;
CREATE TABLE friend_requests (
	user_from_id	int NOT NULL,
	user_to_id		int NOT NULL
);


-- DROP TABLE IF EXISTS restaurants;
-- CREATE TABLE restaurants (
-- 	res_id   	text UNIQUE NOT NULL, -- same as api id
-- 	cuisine     text,
-- 	res_name 	text NOT NULL,
-- 	PRIMARY KEY 	(res_id),
-- );


-- INSERT INTO users (first_name, last_name, fb_id, email, photo_url) VALUES ('Nikita', 'Zamwar', '1504576432888498', 'nikitazamwar@gmail.com', 'https://graph.facebook.com/1504576432888498/picture?type=large');
-- INSERT INTO users (first_name, last_name, fb_id, email, photo_url) VALUES ('Eddie', 'Tribaldos', '1473474075997450', 'et_2012@live.com', 'https://graph.facebook.com/1473474075997450/picture?type=large');
-- INSERT INTO users (first_name, last_name, email, password, photo_url) VALUES ('Tyler', 'Camp', 'hugh@mungus.tr', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe', 'https://scontent-dft4-2.xx.fbcdn.net/v/t1.0-1/p160x160/16425895_10206154964472732_3240717448970717075_n.jpg?oh=1bba1b9e59f8d9c3775b83ad6da4f306&oe=5951F321');
INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (1, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (2, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', true, 'food');
INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (3, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', true, 'food');
INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (3, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO friends (user_id1, user_id2) VALUES (1, 3), (2, 3), (3, 1), (3, 2);
INSERT INTO friend_requests (user_from_id, user_to_id) VALUES (1, 3), (3, 2)
