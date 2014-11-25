DROP TABLE IF EXISTS `kalturadw`.dwh_dim_client_tags;

CREATE TABLE `kalturadw`.`dwh_dim_client_tags` (
  `client_tag_id` INT(11) NOT NULL AUTO_INCREMENT,
  `client_tag_name` VARCHAR(333) NOT NULL DEFAULT '',
  `dwh_creation_date` TIMESTAMP  NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`client_tag_id`),
   UNIQUE KEY (`client_tag_name`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

CREATE TRIGGER `kalturadw`.`dwh_dim_client_tags_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_client_tags`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
