/*
SQLyog Community v8.7 
MySQL - 5.1.37-log 
*********************************************************************
*/

use kalturadw;

drop table if exists `dwh_dim_entry_categories`;

create table `dwh_dim_entry_categories` (
	`partner_id` int(11) NOT NULL,
    	`entry_id` varchar(60) NOT NULL,
        `category_id` int(11) NOT NULL,
	`updated_at` DATETIME,
	`ri_ind` TINYINT(4)  NOT NULL DEFAULT 0 ,
	UNIQUE (entry_id, partner_id, `category_id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8; 
