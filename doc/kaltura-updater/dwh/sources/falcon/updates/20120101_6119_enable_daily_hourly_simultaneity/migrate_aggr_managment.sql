ALTER TABLE kalturadw.aggr_managment
	ADD data_insert_time datetime,
	CHANGE aggr_day_int date_id int(11) unsigned NOT NULL,
	DROP COLUMN aggr_day;

DELETE FROM kalturadw.aggr_managment
	WHERE (is_calculated = 1 or date(date_id) + interval hour_id hour > now());

UPDATE kalturadw.aggr_managment
SET data_insert_time = now();

ALTER TABLE kalturadw.aggr_managment
	DROP COLUMN is_calculated;
