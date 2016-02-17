/*
SQLyog Community v8.7 
MySQL - 5.1.47 : Database - kalturadw
*********************************************************************
*/

use `kalturadw`;

DROP TABLE IF EXISTS `dwh_dim_batch_job_object_type`;

CREATE TABLE `dwh_dim_batch_job_object_type` (
  `batch_job_object_type_id` int(11) NOT NULL,
  `batch_job_object_type_name` VARCHAR(100) DEFAULT 'missing value',
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ri_ind` TINYINT(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`batch_job_object_type_id`)
) ENGINE=MYISAM;
