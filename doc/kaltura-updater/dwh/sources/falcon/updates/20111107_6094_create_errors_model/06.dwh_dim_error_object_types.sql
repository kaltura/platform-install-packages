USE kalturadw;

DROP TABLE IF EXISTS dwh_dim_error_object_types;

CREATE TABLE dwh_dim_error_object_types (
	error_object_type_id INT(11) NOT NULL AUTO_INCREMENT,
	error_object_type_name VARCHAR(255) NOT NULL,
	PRIMARY KEY (`error_object_type_id`),
	UNIQUE KEY (`error_object_type_name`)
	) ENGINE=INNODB DEFAULT CHARSET=latin1;
