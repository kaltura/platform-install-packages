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

/*Table structure for table `upload_token` */

DROP TABLE IF EXISTS `dwh_dim_upload_token`;

CREATE TABLE `dwh_dim_upload_token` (
  `dwh_id` int(11) NOT NULL AUTO_INCREMENT,
  `id` varchar(35) NOT NULL,
  `int_id` varchar(11) NOT NULL,
  `partner_id` int(11) DEFAULT NULL,
  `kuser_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `file_name` varchar(256) DEFAULT NULL,
  `file_size` bigint(20) DEFAULT NULL,
  `uploaded_file_size` bigint(20) DEFAULT NULL,
  `uploaded_temp_path` varchar(256) DEFAULT NULL,
  `user_ip` varchar(39) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_date_id` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_date_id` int(11) DEFAULT NULL,
  `dc` varchar(2) DEFAULT NULL,
  `object_id` varchar(31) DEFAULT NULL,
  `object_type_id` varchar(127) DEFAULT NULL,
  `dwh_creation_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ri_ind` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`dwh_id`),
  UNIQUE KEY `id` (`id`),
  KEY `dwh_update_date` (`dwh_update_date`),
  KEY `updated_date_id` (`updated_date_id`)
) ENGINE=MyISAM AUTO_INCREMENT=660 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
