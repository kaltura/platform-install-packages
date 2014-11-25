USE kalturadw;

DROP TABLE IF EXISTS dwh_entry_plays_views;

CREATE TABLE dwh_entry_plays_views
(entry_id VARCHAR(255), 
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
plays INT(11), 
views INT(11), 
PRIMARY KEY (entry_id),
KEY (updated_at));