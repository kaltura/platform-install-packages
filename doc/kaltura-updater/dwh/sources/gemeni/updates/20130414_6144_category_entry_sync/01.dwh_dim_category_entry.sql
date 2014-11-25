/*
SQLyog Community v8.7 
MySQL - 5.1.37-log 
*********************************************************************
*/

use kalturadw;

drop table if exists `dwh_dim_category_entry`;

create table `dwh_dim_category_entry` (
	`id` int(11) NOT NULL,
	`partner_id` int(11) NOT NULL,
    `entry_id` varchar(20) NOT NULL,
    `category_id` int(11) NOT NULL,
	`created_at` DATETIME,
	`updated_at` DATETIME,
	`status_id` int(11) NOT NULL,
	`dwh_creation_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
	`dwh_update_date` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
	PRIMARY KEY (`id`),
	KEY `category_id` (`category_id`),
	KEY `entry_id` (`entry_id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8; 

CREATE TRIGGER `kalturadw`.`dwh_dim_category_entry_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_category_entry`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();

