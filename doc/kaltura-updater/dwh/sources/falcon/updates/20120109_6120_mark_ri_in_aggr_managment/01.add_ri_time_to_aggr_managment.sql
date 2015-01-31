ALTER TABLE kalturadw.aggr_managment
	ADD COLUMN ri_time DATETIME,
	CHANGE hour_id hour_id INT(11) UNSIGNED NOT NULL AFTER date_id;
	
UPDATE kalturadw.aggr_managment
SET ri_time = end_time;
