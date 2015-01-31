DROP TABLE IF EXISTS `kalturadw`.dwh_dim_api_error_codes;

CREATE TABLE `kalturadw`.`dwh_dim_api_error_codes` (
  `api_error_code_id` INT(11) NOT NULL AUTO_INCREMENT,
  `api_error_code_name` VARCHAR(333) NOT NULL DEFAULT '',
  `dwh_creation_date` TIMESTAMP  NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`api_error_code_id`),
   UNIQUE KEY (`api_error_code_name`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

CREATE TRIGGER `kalturadw`.`dwh_dim_api_error_code_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_api_error_codes`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
