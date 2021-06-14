CREATE TABLE IF NOT EXISTS UserContact (	
	email VARCHAR(50),
	phone CHAR(20),
	PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS UserInfo (
	id INTEGER PRIMARY KEY,
	email VARCHAR(50) NOT NULL UNIQUE,
	name VARCHAR(50),
	FOREIGN KEY(email)
		REFERENCES UserContact (email)
		ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Follows (
	uid INTEGER,
	followed_id INTEGER,
	follower_id INTEGER,
	PRIMARY KEY(uid, followed_id, follower_id),
	FOREIGN KEY(uid)
		REFERENCES UserInfo (id)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS VideoMedia (
	name VARCHAR(50),
	PRIMARY KEY(name)
);

CREATE TABLE IF NOT EXISTS Series (
	name VARCHAR(50),
	seasons INTEGER,
	episodes INTEGER,
	PRIMARY KEY(name),
	FOREIGN KEY(name)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Movies (
	name VARCHAR(50),
	length INTEGER,
	PRIMARY KEY(name),
	FOREIGN KEY(name)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS MoviePeople (
	name VARCHAR(50),
	id INTEGER,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Country (
	name VARCHAR(50),
	id INTEGER UNIQUE,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Lists (
	id INTEGER,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS CuratedList (
	id INTEGER UNIQUE NOT NULL,
	curator VARCHAR(50),
	name VARCHAR(50),
	PRIMARY KEY(id,curator)
);

CREATE TABLE IF NOT EXISTS UserWatchList (
    id INTEGER,
    name VARCHAR(50),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Ratings (
	id INTEGER UNIQUE NOT NULL,
	author VARCHAR(50),
	comment VARCHAR(50),
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS StreamingServices (
	name VARCHAR(50),
	id INTEGER UNIQUE NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Languages (
	id INTEGER UNIQUE NOT NULL,
	name VARCHAR(50),
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS SubscribesTo (
	streaming_id INTEGER,
	streaming_name VARCHAR(50),
	user_id INTEGER,
	tier_name VARCHAR(50),
	PRIMARY KEY(streaming_id, streaming_name,user_id),
	FOREIGN KEY(streaming_id)
		REFERENCES StreamingServices (id)
		ON DELETE SET NULL,
	FOREIGN KEY(user_id)
		REFERENCES UserInfo (id)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS AccessibleIn (
	streamingService_id INTEGER,
	streamingService_name VARCHAR(50),
	country_id INTEGER,
	PRIMARY KEY(streamingService_id, streamingService_name,country_id),
	FOREIGN KEY(streamingService_id)
		REFERENCES StreamingServices (id)
		ON DELETE SET NULL,
	FOREIGN KEY(country_id)
		REFERENCES Country (id)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Certifications (
	name VARCHAR(50),
	PRIMARY KEY(name)
);

CREATE TABLE IF NOT EXISTS Receives (
	videomedia_name VARCHAR(50),
	certifications_name VARCHAR(50),
	PRIMARY KEY(videoMedia_name, certifications_name),
	FOREIGN KEY(videoMedia_name)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL,
	FOREIGN KEY(certifications_name)
		REFERENCES Certifications (name)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ViewableIn (
	country_id INTEGER,
	videomedia_name VARCHAR(50),
	PRIMARY KEY(country_id, videomedia_name),
	FOREIGN KEY(country_id)
		REFERENCES Country (id)
		ON DELETE SET NULL,
	FOREIGN KEY(videomedia_name)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Contains (
	user_watchlist_id INTEGER,
	videomedia_name VARCHAR(50),
	streamingService_id INTEGER,
	PRIMARY KEY(user_watchlist_id, videomedia_name, streamingService_id),
	FOREIGN KEY(user_watchlist_id)
		REFERENCES UserWatchList (id)
		ON DELETE SET NULL,
	FOREIGN KEY(videomedia_name)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL,
	FOREIGN KEY(streamingService_id)
		REFERENCES StreamingServices (id)
		ON DELETE SET NULL 
);

CREATE TABLE IF NOT EXISTS Genre (
	name VARCHAR(50),
	PRIMARY KEY(name)
);

CREATE TABLE IF NOT EXISTS BelongsTo (
	genre_name VARCHAR(50),
	videomedia_name VARCHAR(50),
	PRIMARY KEY(genre_name),
	FOREIGN KEY(genre_Name)
		REFERENCES Genre (name)
		ON DELETE SET NULL,
	FOREIGN KEY(videomedia_name)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Has (
	ratings_id INTEGER,
	videomedia_name VARCHAR(50),
	PRIMARY KEY(ratings_id, videomedia_name),
	FOREIGN KEY(ratings_id)
		REFERENCES Ratings (id)
		ON DELETE SET NULL,
	FOREIGN KEY(videomedia_name)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ParticipatedInType (
	MoviePeopleId INTEGER,
	VideoMediaName VARCHAR(50),
	Type VARCHAR(50),
	PRIMARY KEY(MoviePeopleId, VideoMediaName),
	FOREIGN KEY(MoviePeopleId)
		REFERENCES MoviePeople (id)
		ON DELETE SET NULL,
	FOREIGN KEY(VideoMediaName)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ParticipatedInRole (
	MoviePeopleId INTEGER,
	VideoMediaName VARCHAR(50),
	Role VARCHAR(50),
	PRIMARY KEY(MoviePeopleId, VideoMediaName),
	FOREIGN KEY(MoviePeopleId)
		REFERENCES MoviePeople (id)
		ON DELETE SET NULL,
	FOREIGN KEY(VideoMediaName)
		REFERENCES VideoMedia (name)
		ON DELETE SET NULL
);
