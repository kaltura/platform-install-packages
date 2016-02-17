USE kalturadw_ds;

DROP TABLE IF EXISTS ds_errors;

CREATE TABLE ds_errors (
  	cycle_id INT(11) NOT NULL,
	file_id INT(11) NOT NULL,
	line_number INT(11) NOT NULL,
	partner_id INT(11) NOT NULL,
	error_time datetime NOT NULL,
	error_date_id int NOT NULL,
	error_hour_id int NOT NULL,
	error_object_id VARCHAR(50) NOT NULL,
	error_object_type_id INT(11) NOT NULL,
	error_code_id INT(11) NOT NULL,
	description mediumtext DEFAULT NULL
	) ENGINE=INNODB DEFAULT CHARSET=latin1
	PARTITION BY LIST(cycle_id)
	(PARTITION p_0 VALUES IN (0));
