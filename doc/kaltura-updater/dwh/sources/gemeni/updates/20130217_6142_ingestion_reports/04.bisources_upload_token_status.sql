/*
SQLyog Community v8.7 
MySQL - 5.1.47 : Database - kalturadw_bisources
*********************************************************************
*/

USE `kalturadw_bisources`;

DROP TABLE IF EXISTS `bisources_upload_token_status`;

CREATE TABLE `bisources_upload_token_status` (
  `upload_token_status_id` INT(11) NOT NULL,
  `upload_token_status_name` VARCHAR(100) DEFAULT 'missing value',
  PRIMARY KEY (`upload_token_status_id`)
);

INSERT INTO `bisources_upload_token_status`
			(`upload_token_status_id`,`upload_token_status_name`) 
		
VALUES 	
			(0,'PENDING'),
			(1,'PARTIAL_UPLOAD'),
			(2,'FULL_UPLOAD'),
			(3,'CLOSED'),
			(4,'TIMED_OUT'),
			(5,'DELETED');