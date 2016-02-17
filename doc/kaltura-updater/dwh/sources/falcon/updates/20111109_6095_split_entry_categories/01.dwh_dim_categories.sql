/*
SQLyog Community v8.7 
MySQL - 5.1.37-log 
*********************************************************************
*/

USE kalturadw;

DROP TABLE IF EXISTS `dwh_dim_categories`;

CREATE TABLE `dwh_dim_categories` (
	`category_id` INT(11) NOT NULL AUTO_INCREMENT,
    `category_name` VARCHAR(333) NOT NULL,
	`dwh_creation_date` TIMESTAMP  NOT NULL DEFAULT '0000-00-00 00:00:00',
	`dwh_update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`category_id`), UNIQUE KEY (category_name)
) ENGINE=MYISAM DEFAULT CHARSET=utf8; 

CREATE TRIGGER `kalturadw`.`dwh_dim_categories_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_categories`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW();
    
INSERT INTO dwh_dim_categories (category_id,category_name) VALUES (1,'-');
