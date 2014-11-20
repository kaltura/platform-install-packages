/*
SQLyog Community v8.7 
MySQL - 5.1.47 : Database - kalturadw_bisources
*********************************************************************
*/

USE `kalturadw_bisources`;

DROP TABLE IF EXISTS `bisources_batch_job_object_type`;

CREATE TABLE `bisources_batch_job_object_type` (
  `batch_job_object_type_id` INT(11) NOT NULL,
  `batch_job_object_type_name` VARCHAR(100) DEFAULT 'missing value',
  PRIMARY KEY (`batch_job_object_type_id`)
);

INSERT INTO `bisources_batch_job_object_type` (`batch_job_object_type_id`,`batch_job_object_type_name`) 
VALUES 		(1,'ENTRY'),
			(2,'CATEGORY'),
			(3,'FILE_SYNC'),
			(4,'ASSET');