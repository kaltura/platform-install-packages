USE kalturadw;

DROP TABLE IF EXISTS dwh_fact_errors;

CREATE TABLE dwh_fact_errors (
	file_id INT(11) NOT NULL,
	line_number INT(11) NOT NULL,
	partner_id INT(11) NOT NULL,
	error_time datetime NOT NULL,
	error_date_id int NOT NULL,
	error_hour_id int NOT NULL,
	error_object_id VARCHAR(50) NOT NULL,
	error_object_type_id INT(11) NOT NULL,
	error_code_id INT(11) NOT NULL,
	description mediumtext DEFAULT NULL,
	PRIMARY KEY (`file_id`, `line_number`, `error_date_id`),
	UNIQUE KEY (`error_date_id`,`error_object_id`,`error_object_type_id`,`error_time`)
	) ENGINE=INNODB DEFAULT CHARSET=latin1
	/*!50100 PARTITION BY RANGE (error_date_id)
	(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = INNODB)*/;

CALL add_daily_partition_for_table('dwh_fact_errors');
