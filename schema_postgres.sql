-- gcloud beta sql connect munchr-mysql --user=root


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


DROP TABLE IF EXISTS friends;
CREATE TABLE friends (
	user_id1    int NOT NULL,
	user_id2    int NOT NULL
);
-- CREATE INDEX ON friends (user_id1);
-- CREATE INDEX ON friends (user_id2);


-- DROP TABLE IF EXISTS restaurant;
-- CREATE TABLE restaurant (
-- 	restaurant_id   varchar(31) UNIQUE NOT NULL, -- sane as api id
-- 	cuisine         text NOT NULL,
-- 	vegitarian 		boolean NOT NULL,
-- 	PRIMARY KEY 	(restaurant_id)
-- );


-- DROP TABLE IF EXISTS swipe;
-- CREATE TABLE swipe (
-- 	user_id         int,
-- 	restaurant_id   int,
-- 	swipe           boolean
-- );


-- DROP TABLE IF EXISTS rating;
-- CREATE TABLE rating (
--   user_id           int NOT NULL,
--   restaurant_id     int NOT NULL,
--   overall_rating    int NOT NULL,
--   food_rating       int,
--   value_rating      int,
--   service_rating    int,
--   location_rating   int,
--   atmosphere_rating int
-- );


-- DROP TABLE IF EXISTS likes;
-- CREATE TABLE likes (
-- 	user_id     uuid,
-- 	place_id    uuid,
-- 	swipe       boolean,
-- 	liked       boolean,
-- 	rating      int,
-- 	times       int
-- )

INSERT INTO users (first_name, last_name, fb_id, email, password) VALUES ('Tyler', 'Camp', '123456', 'hugh@mungus.tr', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe');
INSERT INTO users (first_name, last_name, fb_id, email, password) VALUES ('Eddie', 'Tribaldos', '654321', 'fake@email.ha', '$2b$12$yIq.ZIHyM3eF031mvLW.YOvEXPChnrYv3RVRuCfMk3azLZ/vnPXum');
INSERT INTO users (first_name, last_name, fb_id, email, password) VALUES ('Nikita', 'Zamwar', '42069', 'princessnikita@chiquita.com', '$2b$12$4SsDXvYGvbwCbkxJP1bhIu9vW8V3LMB5/DJbX2DGSCn7X.X0SVeXe');

INSERT INTO friends (user_id1, user_id2) VALUES (1, 2);

INSERT INTO friends (user_id1, user_id2) VALUES (3, 2);
INSERT INTO friends (user_id1, user_id2) VALUES (3, 1);
INSERT INTO friends (user_id1, user_id2) VALUES (1, 3);
INSERT INTO friends (user_id1, user_id2) VALUES (2, 3);
