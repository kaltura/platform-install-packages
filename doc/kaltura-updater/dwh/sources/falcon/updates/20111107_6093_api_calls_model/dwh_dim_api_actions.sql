DROP TABLE IF EXISTS `kalturadw`.dwh_dim_api_actions;

CREATE TABLE `kalturadw`.`dwh_dim_api_actions` (
  `action_id` INT(11) NOT NULL AUTO_INCREMENT,
  `action_name` VARCHAR(166) NOT NULL DEFAULT '',
  `service_name` VARCHAR(166) NOT NULL DEFAULT '',
  `dwh_creation_date` TIMESTAMP  NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`action_id`),
   UNIQUE KEY (`action_name`, `service_name`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

CREATE TRIGGER `kalturadw`.`dwh_dim_api_actions_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_api_actions`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
