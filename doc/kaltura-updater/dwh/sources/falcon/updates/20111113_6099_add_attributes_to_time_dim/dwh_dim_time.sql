ALTER TABLE kalturadw.dwh_dim_time
	CHANGE date_field date_field DATE NOT NULL,
	ADD day_eng_name VARCHAR(50) AFTER date_field,	
	ADD datetime_field DATETIME NOT NULL AFTER date_field,
	ADD week_id INT(11) AFTER day_of_week,
	ADD week_eng_name VARCHAR(50) AFTER week_of_year,
	ADD month_eng_name VARCHAR(50) AFTER YEAR,	
	ADD month_id INT(11) AFTER YEAR, 
	ADD month_str VARCHAR(50) AFTER YEAR,
	ADD quarter_eng_name  VARCHAR(50) AFTER QUARTER,
	ADD quarter_id INT(11) AFTER QUARTER;

UPDATE kalturadw.dwh_dim_time
SET 	datetime_field = date_field,
	day_eng_name = DATE_FORMAT(date_field, '%b %e, %Y'),
	week_id = DATE_FORMAT(date_field, '%Y%U')*1,
	week_eng_name = DATE_FORMAT(date_field, 'Week %U, %Y'),
	month_id = DATE_FORMAT(date_field, '%Y%m')*1,
	month_str = DATE_FORMAT(date_Field, '%Y-%m'),
	month_eng_name = DATE_FORMAT(date_Field, '%b-%y'),
	quarter_id = YEAR(date_Field)*10+QUARTER(date_field),
	quarter_eng_name = CONCAT('Quarter ', QUARTER(date_field), ',', YEAR(date_Field));
