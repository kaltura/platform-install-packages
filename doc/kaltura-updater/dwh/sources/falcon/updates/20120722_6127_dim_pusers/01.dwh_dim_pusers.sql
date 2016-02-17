DROP TABLE IF EXISTS `kalturadw`.`dwh_dim_pusers`;

CREATE TABLE `kalturadw`.`dwh_dim_pusers` (
  `puser_id` INT AUTO_INCREMENT NOT NULL ,
  `name` VARCHAR(100) DEFAULT 'missing value',
  `partner_id` INT NOT NULL,
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT 0,
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `ri_ind` TINYINT NOT NULL DEFAULT '0',
  PRIMARY KEY (`puser_id`),
  KEY `partner_name_index` (`partner_id`,`name`)
) ENGINE=MYISAM  DEFAULT CHARSET=utf8;

CREATE TRIGGER `kalturadw`.`dwh_dim_pusers_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_pusers`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
