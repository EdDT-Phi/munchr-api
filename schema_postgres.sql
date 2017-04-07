-- DROP TABLE IF EXISTS users;
-- CREATE TABLE users (
-- 	user_id     serial UNIQUE NOT NULL,
-- 	fb_id       text,
-- 	first_name  text NOT NULL,
-- 	last_name   text NOT NULL,
-- 	email       text UNIQUE NOT NULL,
-- 	password    text,
-- 	photo_url   text,
-- 	PRIMARY KEY (user_id)
-- );


-- DROP TABLE IF EXISTS user_ratings;
-- CREATE TABLE user_ratings (
-- 	user_id 	int NOT NULL,
-- 	res_id 		text NOT NULL,
-- 	liked		boolean NOT NULL,
-- 	specific	text,
-- 	review_date timestamp DEFAULT current_timestamp
-- );


-- DROP TABLE IF EXISTS friends;
-- CREATE TABLE friends (
-- 	user_id1    int NOT NULL,
-- 	user_id2    int NOT NULL
-- );


-- DROP TABLE IF EXISTS friend_requests;
-- CREATE TABLE friend_requests (
-- 	user_from_id	int NOT NULL,
-- 	user_to_id		int NOT NULL
-- );


-- DROP TABLE IF EXISTS restaurants;
-- CREATE TABLE restaurants (
-- 	res_id   	text UNIQUE NOT NULL, -- same as api id
-- 	cuisine     text,
-- 	res_name 	text NOT NULL,
-- 	PRIMARY KEY 	(res_id),
-- );

DROP TABLE IF EXISTS recommendations;
CREATE TABLE recommendations (
	user_from_id	int,
	user_to_id		int,
	res_id			text
);


-- INSERT INTO users (first_name, last_name, fb_id, email, photo_url) VALUES ('Eddie', 'Tribaldos', '1473474075997450', 'et_2012@live.com', 'https://graph.facebook.com/1473474075997450/picture?type=large');
-- INSERT INTO users (first_name, last_name, fb_id, email, photo_url) VALUES ('Nikita', 'Zamwar', '1504576432888498', 'nikitazamwar@gmail.com', 'https://graph.facebook.com/1504576432888498/picture?type=large');
-- INSERT INTO users (first_name, last_name, email, password, photo_url) VALUES ('Tyler', 'Camp', 'hugh@mungus.tr', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe', 'https://scontent-dft4-2.xx.fbcdn.net/v/t1.0-1/p160x160/16425895_10206154964472732_3240717448970717075_n.jpg?oh=1bba1b9e59f8d9c3775b83ad6da4f306&oe=5951F321');

-- INSERT INTO users (first_name, last_name, email, password, photo_url) VALUES ('Rick', 'Sanchez', 'fake1@email.ok', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe', 'http://img04.deviantart.net/1de9/i/2015/270/8/d/rick_sanchez_from_rick_and_morty_by_ravage657-d9b4oui.png');
-- INSERT INTO users (first_name, last_name, email, password, photo_url) VALUES ('Morty', 'Sanchez', 'fake2@email.ok', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe', 'https://static.giantbomb.com/uploads/scale_small/0/9517/2816097-tumblr_n45cr8dmj61ty0km0o7_1280.png');
-- INSERT INTO users (first_name, last_name, email, password, photo_url) VALUES ('Summer', 'Sanchez', 'fake3@email.ok', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe', 'http://vignette1.wikia.nocookie.net/rickandmorty/images/0/07/SummerComics.jpeg/revision/latest?cb=20161223004721');
-- INSERT INTO users (first_name, last_name, email, password, photo_url) VALUES ('Bird', 'Person', 'fake4@email.ok', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe', 'https://pbs.twimg.com/profile_images/651231825763790848/GxBvDrgO_400x400.jpg');
-- INSERT INTO users (first_name, last_name, email, password, photo_url) VALUES ('Squanchy', '', 'fake5@email.ok', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe', 'https://i.ytimg.com/vi/WEsqSJLeeDc/hqdefault.jpg');

-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (1, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', true, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (2, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (3, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', true, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (3, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (4, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (5, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (1, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (5, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (6, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (7, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (8, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
-- INSERT INTO friend_requests (user_from_id, user_to_id) VALUES (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3);

