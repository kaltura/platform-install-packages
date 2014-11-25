DROP TABLE IF EXISTS `kalturadw`.dwh_dim_hosts;

CREATE TABLE `kalturadw`.`dwh_dim_hosts` (
  `host_id` INT(11) NOT NULL AUTO_INCREMENT,
  `host_name` VARCHAR(333) NOT NULL DEFAULT '',
  `dwh_creation_date` TIMESTAMP  NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`host_id`),
   UNIQUE KEY (`host_name`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

CREATE TRIGGER `kalturadw`.`dwh_dim_hosts_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_hosts`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
