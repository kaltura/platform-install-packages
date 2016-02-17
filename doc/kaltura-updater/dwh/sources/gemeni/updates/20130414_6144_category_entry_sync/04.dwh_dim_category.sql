/*
SQLyog Community v8.7 
MySQL - 5.1.37-log 
*********************************************************************
*/

use kalturadw;

drop table if exists `dwh_dim_category`;

CREATE TABLE `dwh_dim_category` (
	`category_id` INT(11) NOT NULL,
	`parent_id` INT(11) NOT NULL,
	`partner_id` INT(11) NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`full_name` TEXT,
	`created_at` DATETIME,
	`updated_at` DATETIME,
	`status_id` INT(11) NOT NULL,
	`kuser_id` INT(11),
	`dwh_creation_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
	`dwh_update_date` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
	PRIMARY KEY (`category_id`),
	KEY `category_name` (`name`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

CREATE TRIGGER `kalturadw`.`dwh_dim_category_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_category`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();

