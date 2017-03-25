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
-- CREATE INDEX ON users (user_id);

DROP TABLE IF EXISTS user_ratings;
CREATE TABLE user_ratings (
	user_id 	int NOT NULL,
	res_id 		text NOT NULL,
	liked		boolean NOT NULL,
	specific	text,
	review_date timestamp DEFAULT current_timestamp,
);


DROP TABLE IF EXISTS user_swipes;
CREATE TABLE user_swipes (
	user_id		int NOT NULL,
	res_id 		int NOT NULL,
	swipe_score number DEFAULT = 0
);


DROP TABLE IF EXISTS friends;
CREATE TABLE friends (
	user_id1    int NOT NULL,
	user_id2    int NOT NULL
);
-- CREATE INDEX ON friends (user_id1);
-- CREATE INDEX ON friends (user_id2);


DROP TABLE IF EXISTS restaurants;
CREATE TABLE restaurants (
	res_id   	text UNIQUE NOT NULL, -- same as api id
	cuisine     text,
	res_name 	text NOT NULL,
	PRIMARY KEY 	(res_id)
);

-- CREATE INDEX ON restaurants (restaurant_id);

INSERT INTO users (first_name, last_name, fb_id, email, password) VALUES ('Tyler', 'Camp', '123456', 'hugh@mungus.tr', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe');
INSERT INTO users (first_name, last_name, fb_id, email, password) VALUES ('Eddie', 'Tribaldos', '654321', 'fake@email.ha', '$2b$12$yIq.ZIHyM3eF031mvLW.YOvEXPChnrYv3RVRuCfMk3azLZ/vnPXum');
INSERT INTO users (first_name, last_name, fb_id, email, password) VALUES ('Nikita', 'Zamwar', '42069', 'princessnikita@chiquita.com', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe');

INSERT INTO friends (user_id1, user_id2) VALUES (1, 2);
INSERT INTO friends (user_id1, user_id2) VALUES (2, 1);

INSERT INTO friends (user_id1, user_id2) VALUES (3, 2);
INSERT INTO friends (user_id1, user_id2) VALUES (3, 1);
INSERT INTO friends (user_id1, user_id2) VALUES (1, 3);
INSERT INTO friends (user_id1, user_id2) VALUES (2, 3);

INSERT INTO restaurants (res_id, res_name) VALUES ('ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', 'The Hightower');

INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (3, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', true, 'food');
INSERT INTO user_ratings (user_id, res_id, liked, specific) VALUES (1, 'ChIJ9XmrDLC1RIYRKZ6iF4_DV7I', false, 'food');
