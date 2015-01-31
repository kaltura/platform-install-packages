/*
SQLyog Community v8.7 
MySQL - 5.1.47 : Database - kalturadw_bisources
*********************************************************************
*/

USE `kalturadw_bisources`;

DROP TABLE IF EXISTS `bisources_batch_job_exec_status`;

CREATE TABLE `bisources_batch_job_exec_status` (
  `batch_job_exec_status_id` INT(11) NOT NULL,
  `batch_job_exec_status_name` VARCHAR(100) DEFAULT 'missing value',
  PRIMARY KEY (`batch_job_exec_status_id`)
);

INSERT INTO `bisources_batch_job_exec_status`
VALUES 		(0,'NORMAL'),
			(1,'ABORTED');