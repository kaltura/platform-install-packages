/*
SQLyog Community v8.7 
MySQL - 5.1.37-log : Database - kaltura
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
USE `kalturadw`;

/*Table structure for table `batch_job_sep` */

DROP TABLE IF EXISTS `dwh_dim_batch_job_sep`;

CREATE TABLE `dwh_dim_batch_job_sep` (
  `dwh_id` INT(11) NOT NULL AUTO_INCREMENT,
  `id` INT(11) NOT NULL,
  `job_type_id` INT(6) DEFAULT NULL,
  `job_sub_type_id` INT(6) DEFAULT NULL,
  `object_id` VARCHAR(20) DEFAULT NULL,
  `object_type_id` INT(6) DEFAULT NULL,
  `data` VARCHAR(8192) DEFAULT NULL,
  `status_id` INT(11) DEFAULT NULL,
  `message` VARCHAR(1024) DEFAULT NULL,
  `description` VARCHAR(1024) DEFAULT NULL,
  `created_at` DATETIME DEFAULT NULL,
  `created_date_id` INT(11) DEFAULT '-1',
  `updated_at` DATETIME DEFAULT NULL,
  `updated_date_id` INT(11) DEFAULT '-1',
  `priority` TINYINT(4) NOT NULL,
  `queue_time` DATETIME DEFAULT NULL,
  `finish_time` DATETIME DEFAULT NULL,
  `entry_id` VARCHAR(20) DEFAULT NULL,
  `partner_id` INT(11) DEFAULT NULL,
  `last_scheduler_id` INT(11) DEFAULT NULL,
  `last_worker_id` INT(11) DEFAULT NULL,
  `parent_job_id` INT(11) DEFAULT NULL,
  `bulk_job_id` INT(11) DEFAULT NULL,
  `root_job_id` INT(11) DEFAULT NULL,
  `dc` VARCHAR(2) DEFAULT NULL,
  `error_type_id` INT(11) DEFAULT '0',
  `err_number` INT(11) DEFAULT '0',
  `execution_status_id` SMALLINT(6) DEFAULT NULL,
  `batch_job_lock_id` INT(20) DEFAULT NULL,
  `custom_data` TEXT,
  `lock_info` TEXT,
  `file_size` BIGINT(20) NOT NULL DEFAULT '-1',
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ri_ind` TINYINT(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`dwh_id`),
  UNIQUE KEY `id` (`id`),
  KEY `dwh_update_date` (`dwh_update_date`),
  KEY `updated_date_id` (`updated_date_id`,`job_type_id`)
) ENGINE=MYISAM AUTO_INCREMENT=51079 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
