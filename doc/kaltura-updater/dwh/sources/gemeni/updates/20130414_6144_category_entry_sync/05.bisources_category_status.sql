/*
SQLyog Community v8.7 
MySQL - 5.1.47 : Database - kalturadw_bisources
*********************************************************************
*/

USE `kalturadw_bisources`;

DROP TABLE IF EXISTS `bisources_category_status`;

CREATE TABLE `bisources_category_status` (
  `category_status_id` INT(11) NOT NULL,
  `category_status_name` VARCHAR(100) DEFAULT 'missing value',
  PRIMARY KEY (`category_status_id`)
);

INSERT INTO `bisources_category_status`
			(`category_status_id`,`category_status_name`) 
		
VALUES 	
			(1,'UPDATING'),
			(2,'ACTIVE'),
			(3,'DELETED'),
			(4,'PURGED');
			
			
			
