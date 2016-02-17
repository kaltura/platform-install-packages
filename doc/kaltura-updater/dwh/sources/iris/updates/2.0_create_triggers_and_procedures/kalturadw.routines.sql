USE `kalturadw`;
-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: kalturadw
-- ------------------------------------------------------
-- Server version	5.1.73
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_api_actions_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_api_actions`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_applications_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_applications`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_categories_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_categories`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_category_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_category`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_category_entry_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_category_entry`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_category_entry_status_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_category_entry_status`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_category_status_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_category_status`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_client_tags_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_client_tags`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_control_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_control`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_domain_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_domain`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_editor_type_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_editor_type`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `dwh_dim_entries_setcreationtime_oninsert` BEFORE INSERT ON `dwh_dim_entries` 
    FOR EACH ROW SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_entry_media_source_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_entry_media_source`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_entry_media_type_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_entry_media_type`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_entry_status_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_entry_status`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_entry_type_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_entry_type`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_entry_type_display_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_entry_type_display`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_error_code_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_error_codes`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_event_type_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_event_type`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_gender_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_gender`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_hosts_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_hosts`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_kusers_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_kusers`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_locations_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_locations`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_moderation_status_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_moderation_status`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_partner_class_of_service_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_partner_class_of_service`
    FOR EACH ROW
        SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_partner_group_type_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_partner_group_type`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_partner_status_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_partner_status`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_partner_type_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_partner_type`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_partner_vertical_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_partner_vertical`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_partners_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_partners`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_partners_billing_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_partners_billing`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_permissions_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_permissions`
    FOR EACH ROW 
        SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_pusers_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_pusers`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_tags_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_tags`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_ui_conf_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_ui_conf`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_ui_conf_status_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_ui_conf_status`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_ui_conf_type_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_ui_conf_type`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_user_status_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_user_status`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_widget_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_widget`
    FOR EACH ROW 
	SET new.dwh_creation_date = NOW() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 trigger `kalturadw`.`dwh_dim_widget_security_policy_setcreationtime_oninsert` before insert
    on `kalturadw`.`dwh_dim_widget_security_policy`
    for each row 
	set new.dwh_creation_date = now() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `kalturadw`.`dwh_dim_widget_security_type_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_widget_security_type`
    FOR EACH ROW 
	set new.dwh_creation_date = now() */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping routines for database 'kalturadw'
--
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`etl`@`localhost`*/ /*!50003 FUNCTION `kalturadw`.`calc_median_ff_convert_job_wait_time`(p_date_id INT(11)) RETURNS int(11)
    DETERMINISTIC
BEGIN
	DECLARE v_median INT(11);
	SET v_median = 0;
	SELECT t1.wait_time AS median_val INTO v_median FROM (
	SELECT @rownum:=@rownum+1 AS `row_number`, IF(d.wait_time>0, d.wait_time, 0) wait_time
	FROM kalturadw.dwh_fact_convert_job d,  (SELECT @rownum:=0) r
	WHERE created_date_id = p_date_id AND is_ff = 1 
	ORDER BY d.wait_time
	) AS t1, 
	(
	SELECT COUNT(*) AS total_rows
	FROM kalturadw.dwh_fact_convert_job d
	WHERE created_date_id = p_date_id AND is_ff = 1 
	) AS t2
	WHERE 1
	AND t1.row_number=FLOOR(total_rows/2)+1;
	
	RETURN v_median;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `kalturadw`.`calc_month_id`(date_id INT(11)) RETURNS int(11)
    DETERMINISTIC
BEGIN
	RETURN FLOOR(date_id/100);
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `kalturadw`.`calc_partner_monthly_storage`(p_month_id INT ,p_partner_id INT) RETURNS decimal(19,4)
    DETERMINISTIC
BEGIN
        DECLARE avg_cont_aggr_storage DECIMAL(19,4);

        SELECT  calc_partner_storage_data_time_range (DATE(p_month_id*100+1)*1,LAST_DAY(p_month_id*100+1)*1,p_partner_id)
        INTO avg_cont_aggr_storage;
        RETURN avg_cont_aggr_storage;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `kalturadw`.`calc_partner_storage_data_time_range`(p_start_date_id INT, p_end_date_id INT ,p_partner_id INT ) RETURNS decimal(19,4)
    DETERMINISTIC
BEGIN	
	DECLARE total_billable_storage_mb DECIMAL (19,4);
  	
    SELECT MAX(aggr_storage_mb)
    INTO total_billable_storage_mb
    FROM dwh_hourly_partner_usage aggr_p
    WHERE 
    IF (p_start_date_id = p_end_date_id, date_id = p_start_date_id,
	FLOOR(date_id/100) BETWEEN FLOOR(p_start_date_id/100) AND FLOOR(p_end_date_id/100))
    AND aggr_p.partner_id = p_partner_id
    AND aggr_p.hour_id = 0
    AND aggr_p.bandwidth_source_id = 1;
    
	RETURN total_billable_storage_mb;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `kalturadw`.`calc_time_shift`(date_id INT, hour_id INT, time_shift INT) RETURNS int(11)
    NO SQL
BEGIN
	RETURN DATE_FORMAT((date_id + INTERVAL hour_id HOUR + INTERVAL time_shift HOUR), '%Y%m%d')*1;
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `kalturadw`.`get_overage_charge`(max_amount DECIMAL(19,4), actual_amount DECIMAL(19,4), charge_units INT(11), charge_usd_per_unit DECIMAL(19,4)) RETURNS decimal(19,4)
    NO SQL
BEGIN
	RETURN GREATEST(0,IFNULL(CEILING((actual_amount - max_amount)/charge_units)*charge_usd_per_unit,0));
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `kalturadw`.`resolve_aggr_name`(p_aggr_name VARCHAR(100),p_field_name VARCHAR(100)) RETURNS varchar(100) CHARSET latin1
    DETERMINISTIC
BEGIN
	DECLARE v_aggr_table VARCHAR(100);
	DECLARE v_aggr_id_field VARCHAR(100);
	SELECT aggr_table, aggr_id_field
	INTO  v_aggr_table, v_aggr_id_field
	FROM kalturadw_ds.aggr_name_resolver
	WHERE aggr_name = p_aggr_name;
	
	IF p_field_name = 'aggr_table' THEN RETURN v_aggr_table;
	ELSEIF p_field_name = 'aggr_id_field' THEN RETURN v_aggr_id_field;
	END IF;
	RETURN '';
    END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`add_daily_partition_for_table`(table_name VARCHAR(40))
BEGIN
	DECLARE p_name,p_value VARCHAR(100);
	DECLARE p_date,_current_date DATETIME;
	DECLARE p_continue BOOL;
	
	SELECT NOW()
		INTO _current_date;
	SET p_continue = TRUE;
	WHILE (p_continue) DO
		SELECT MAX(partition_description) n,
			   (MAX(partition_description) + INTERVAL 1 DAY)*1  v,
			   STR_TO_DATE(MAX(partition_description),'%Y%m%d')
		INTO p_name,p_value, p_date
		FROM `information_schema`.`partitions` 
		WHERE `partitions`.`TABLE_NAME` = table_name;
		IF (_current_date > p_date - INTERVAL 7 DAY AND p_name IS NOT NULL) THEN
			SET @s = CONCAT('alter table kalturadw.' , table_name , ' ADD PARTITION (partition p_' ,p_name ,' values less than (', p_value ,'))');
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		ELSE
			SET p_continue = FALSE;
		END IF;
	END WHILE;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`add_live_plays_views`(p_date_id INT, p_hour_id INT)
BEGIN
    INSERT INTO dwh_entry_plays_views(entry_id, plays, views)
    SELECT aggr.entry_id, IFNULL(count_plays, 0) plays, IFNULL(count_loads, 0) views
    FROM kalturadw.dwh_hourly_events_live_entry aggr
    WHERE date_id = p_date_id AND hour_id = p_hour_id
    ON DUPLICATE KEY UPDATE
        plays = plays + VALUES(plays) ,
        views = views + VALUES(views);

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`add_monthly_partition_for_table`(table_name VARCHAR(40))
BEGIN
	DECLARE p_name,p_value VARCHAR(100);
	DECLARE p_date,_current_date DATETIME;
	DECLARE p_continue BOOL;
	
	SELECT NOW()
		INTO _current_date;
	SET p_continue = TRUE;
	WHILE (p_continue) DO
		SELECT EXTRACT( YEAR_MONTH FROM MAX(partition_description)) n,
			   (MAX(partition_description) + INTERVAL 1 MONTH)*1  v,
			   STR_TO_DATE(MAX(partition_description),'%Y%m%d')
		INTO p_name,p_value, p_date
		FROM `information_schema`.`partitions` 
		WHERE `partitions`.`TABLE_NAME` = table_name;
		IF (_current_date > p_date - INTERVAL 1 MONTH AND p_name IS NOT NULL) THEN
			SET @s = CONCAT('alter table kalturadw.' , table_name , ' ADD PARTITION (partition p_' ,p_name ,' values less than (', p_value ,'))');
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		ELSE
			SET p_continue = FALSE;
		END IF;
	END WHILE;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`add_partitions`()
BEGIN
	CALL add_daily_partition_for_table('dwh_fact_events');
        CALL add_daily_partition_for_table('dwh_fact_fms_session_events');
        CALL add_daily_partition_for_table('dwh_fact_fms_sessions');
        CALL add_daily_partition_for_table('dwh_fact_bandwidth_usage');
        CALL add_daily_partition_for_table('dwh_fact_api_calls');
        CALL add_daily_partition_for_table('dwh_fact_incomplete_api_calls');
        CALL add_daily_partition_for_table('dwh_fact_errors');
		CALL add_daily_partition_for_table('dwh_fact_plays');
        CALL add_monthly_partition_for_table('dwh_fact_entries_sizes');
        CALL add_monthly_partition_for_table('dwh_hourly_events_entry');
        CALL add_monthly_partition_for_table('dwh_hourly_events_domain');
        CALL add_monthly_partition_for_table('dwh_hourly_events_country');
        CALL add_monthly_partition_for_table('dwh_hourly_events_widget');
        CALL add_monthly_partition_for_table('dwh_hourly_events_uid');
        CALL add_monthly_partition_for_table('dwh_hourly_events_domain_referrer');
        CALL add_monthly_partition_for_table('dwh_hourly_partner');
        CALL add_monthly_partition_for_table('dwh_hourly_partner_usage');
		CALL add_monthly_partition_for_table('dwh_hourly_events_devices');
		CALL add_monthly_partition_for_table('dwh_hourly_api_calls');
    	CALL add_monthly_partition_for_table('dwh_hourly_errors');
		CALL add_monthly_partition_for_table('dwh_hourly_events_context_entry_user_app');
		CALL add_monthly_partition_for_table('dwh_hourly_events_context_app');
		CALL add_monthly_partition_for_table('dwh_hourly_user_usage');
		CALL add_monthly_partition_for_table('dwh_hourly_events_context_app_devices');
		CALL add_monthly_partition_for_table('dwh_daily_ingestion');
		CALL add_monthly_partition_for_table('dwh_daily_partner_ingestion');
		CALL kalturadw.add_monthly_partition_for_table('dwh_hourly_plays_partner');
		CALL kalturadw.add_monthly_partition_for_table('dwh_hourly_plays_entry');
		CALL kalturadw.add_monthly_partition_for_table('dwh_hourly_events_live_entry');
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`add_plays_views`(p_date_id INT, p_hour_id INT)
BEGIN
    INSERT INTO dwh_entry_plays_views(entry_id, plays, views)
    SELECT aggr.entry_id, IFNULL(count_plays, 0) plays, IFNULL(count_loads, 0) views
    FROM kalturadw.dwh_hourly_events_entry aggr
    WHERE date_id = p_date_id AND hour_id = p_hour_id 
    ON DUPLICATE KEY UPDATE 
        plays = plays + VALUES(plays) ,
        views = views + VALUES(views); 

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`all_tables_to_new`()
BEGIN
	DECLARE done INT DEFAULT 0;
	DECLARE v_greater_than_or_equal_date_id INT;
	DECLARE v_less_than_date_id INT;
	DECLARE v_table_name VARCHAR(256);
	DECLARE c_partitions 
	CURSOR FOR 
	SELECT greater_than_or_equal_date_id, less_than_date_id, table_name
	FROM kalturadw_ds.tables_to_new
	ORDER BY less_than_date_id;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	
	OPEN c_partitions;
	
	read_loop: LOOP
    FETCH c_partitions INTO v_greater_than_or_equal_date_id, v_less_than_date_id, v_table_name;
    IF done THEN
      LEAVE read_loop;
    END IF;
    
	CALL do_tables_to_new(v_greater_than_or_equal_date_id, v_less_than_date_id,v_table_name);
	
	
  END LOOP;

  CLOSE c_partitions;
	
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`apply_table_partitions_to_target_table`(p_table_name VARCHAR(255))
BEGIN
        DECLARE done INT DEFAULT 0;
        DECLARE v_partition_statement VARCHAR(255);
        DECLARE c_partitions
        CURSOR FOR
        SELECT CONCAT('ALTER TABLE kalturadw.',p_table_name,'_new ADD PARTITION (PARTITION ', partition_name,' VALUES LESS THAN(', partition_description, '));') cmd
        FROM information_schema.PARTITIONS existing, (SELECT MAX(partition_description) latest FROM information_schema.PARTITIONS WHERE table_name =CONCAT(p_table_name,'_new')) new_table
        WHERE existing.partition_description > new_table.latest AND table_name = p_table_name
        ORDER BY partition_description;

        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

        OPEN c_partitions;

        read_loop: LOOP
        FETCH c_partitions INTO v_partition_statement;
            IF done THEN
              LEAVE read_loop;
            END IF;
	SET @s = v_partition_statement;
        PREPARE stmt FROM @s;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        END LOOP;

        CLOSE c_partitions;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day`(p_date_val DATE,p_hour_id INT(11), p_aggr_name VARCHAR(100))
BEGIN
        DECLARE v_aggr_table VARCHAR(100);
        DECLARE v_aggr_id_field VARCHAR(100);
        DECLARE extra VARCHAR(100);
        DECLARE v_from_archive DATE;
        DECLARE v_ignore DATE;
        DECLARE v_table_name VARCHAR(100);
        DECLARE v_join_table VARCHAR(100);
        DECLARE v_join_condition VARCHAR(200);
        DECLARE v_use_index VARCHAR(100);

        SELECT DATE(NOW() - INTERVAL archive_delete_days_back DAY), DATE(archive_last_partition)
        INTO v_ignore, v_from_archive
        FROM kalturadw_ds.retention_policy
        WHERE table_name = 'dwh_fact_events';

        IF (p_date_val >= v_ignore) THEN

                        SELECT aggr_table, aggr_id_field
                        INTO  v_aggr_table, v_aggr_id_field
                        FROM kalturadw_ds.aggr_name_resolver
                        WHERE aggr_name = p_aggr_name;

                        SET extra = CONCAT('pre_aggregation_',p_aggr_name);
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME=extra) THEN
                            SET @ss = CONCAT('CALL ',extra,'(''', p_date_val,''',',p_hour_id,');');
                            PREPARE stmt1 FROM  @ss;
                            EXECUTE stmt1;
                            DEALLOCATE PREPARE stmt1;
                        END IF ;

                        IF (v_aggr_table <> '') THEN
                                SET @s = CONCAT('delete from ',v_aggr_table,' where date_id = DATE(''',p_date_val,''')*1 and hour_id = ',p_hour_id);
                                PREPARE stmt FROM  @s;
                                EXECUTE stmt;
                                DEALLOCATE PREPARE stmt;
                        END IF;

                        SET @s = CONCAT('INSERT INTO aggr_managment(aggr_name, date_id, hour_id, data_insert_time)
                                        VALUES(''',p_aggr_name,''',''',DATE(p_date_val)*1,''',',p_hour_id,',NOW())
                                        ON DUPLICATE KEY UPDATE data_insert_time = values(data_insert_time)');
                        PREPARE stmt FROM  @s;
                        EXECUTE stmt;
                        DEALLOCATE PREPARE stmt;

                        IF (p_date_val >= v_from_archive) THEN
                                SET v_table_name = 'dwh_fact_events';
                                SET v_use_index = 'USE INDEX (event_hour_id_event_date_id_partner_id)';
                        ELSE
                                SET v_table_name = 'dwh_fact_events_archive';
                                SET v_use_index = '';
                        END IF;

                        SELECT aggr_table, CONCAT(
                                                        IF(aggr_id_field <> '', CONCAT(',', aggr_id_field),'') ,
                                                        IF(dim_id_field <> '',  CONCAT(', e.', REPLACE(dim_id_field,',',', e.')), '')
                                                  )
                        INTO  v_aggr_table, v_aggr_id_field
                        FROM kalturadw_ds.aggr_name_resolver
                        WHERE aggr_name = p_aggr_name;

                        SELECT IF(join_table <> '' , CONCAT(',', join_table), ''), IF(join_table <> '', CONCAT(' AND ev.' ,join_id_field,'=',join_table,'.',join_id_field), '')
                        INTO v_join_table, v_join_condition
                        FROM kalturadw_ds.aggr_name_resolver
                        WHERE aggr_name = p_aggr_name;


                        SET @s = CONCAT('UPDATE aggr_managment SET start_time = NOW()
                                        WHERE aggr_name = ''',p_aggr_name,''' AND date_id = ''',DATE(p_date_val)*1,''' AND hour_id = ',p_hour_id);
                        PREPARE stmt FROM  @s;
                        EXECUTE stmt;
                        DEALLOCATE PREPARE stmt;

                        IF ( INSTR(v_aggr_table, 'live') = 0) THEN
                                SET @s = CONCAT('INSERT INTO ',v_aggr_table,'
                                        (partner_id
                                        ,date_id
                                        ,hour_id
                                        ',REPLACE(v_aggr_id_field,'e.',''),'
                                        ,count_loads
                                        ,count_plays
                                        ,count_plays_25
                                        ,count_plays_50
                                        ,count_plays_75
                                        ,count_plays_100
                                        ,count_edit
                                        ,count_viral
                                        ,count_download
                                        ,count_report
                                        ,count_buf_start
                                        ,count_buf_end
                                        ,count_open_full_screen
                                        ,count_close_full_screen
                                        ,count_replay
                                        ,count_seek
                                        ,count_open_upload
                                        ,count_save_publish
                                        ,count_close_editor
                                        ,count_pre_bumper_played
                                        ,count_post_bumper_played
                                        ,count_bumper_clicked
                                        ,count_preroll_started
                                        ,count_midroll_started
                                        ,count_postroll_started
                                        ,count_overlay_started
                                        ,count_preroll_clicked
                                        ,count_midroll_clicked
                                        ,count_postroll_clicked
                                        ,count_overlay_clicked
                                        ,count_preroll_25
                                        ,count_preroll_50
                                        ,count_preroll_75
                                        ,count_midroll_25
                                        ,count_midroll_50
                                        ,count_midroll_75
                                        ,count_postroll_25
                                        ,count_postroll_50
                                        ,count_postroll_75
                                        )
                                SELECT  ev.partner_id,ev.event_date_id, event_hour_id',v_aggr_id_field,',
                                SUM(IF(ev.event_type_id = 2, 1,NULL)) count_loads,
                                SUM(IF(ev.event_type_id = 3, 1,NULL)) count_plays,
                                SUM(IF(ev.event_type_id = 4, 1,NULL)) count_plays_25,
                                SUM(IF(ev.event_type_id = 5, 1,NULL)) count_plays_50,
                                SUM(IF(ev.event_type_id = 6, 1,NULL)) count_plays_75,
                                SUM(IF(ev.event_type_id = 7, 1,NULL)) count_plays_100,
                                SUM(IF(ev.event_type_id = 8, 1,NULL)) count_edit,
                                SUM(IF(ev.event_type_id = 9, 1,NULL)) count_viral,
                                SUM(IF(ev.event_type_id = 10, 1,NULL)) count_download,
                                SUM(IF(ev.event_type_id = 11, 1,NULL)) count_report,
                                SUM(IF(ev.event_type_id = 12, 1,NULL)) count_buf_start,
                                SUM(IF(ev.event_type_id = 13, 1,NULL)) count_buf_end,
                                SUM(IF(ev.event_type_id = 14, 1,NULL)) count_open_full_screen,
                                SUM(IF(ev.event_type_id = 15, 1,NULL)) count_close_full_screen,
                                SUM(IF(ev.event_type_id = 16, 1,NULL)) count_replay,
                                SUM(IF(ev.event_type_id = 17, 1,NULL)) count_seek,
                                SUM(IF(ev.event_type_id = 18, 1,NULL)) count_open_upload,
                                SUM(IF(ev.event_type_id = 19, 1,NULL)) count_save_publish,
                                SUM(IF(ev.event_type_id = 20, 1,NULL)) count_close_editor,
                                SUM(IF(ev.event_type_id = 21, 1,NULL)) count_pre_bumper_played,
                                SUM(IF(ev.event_type_id = 22, 1,NULL)) count_post_bumper_played,
                                SUM(IF(ev.event_type_id = 23, 1,NULL)) count_bumper_clicked,
                                SUM(IF(ev.event_type_id = 24, 1,NULL)) count_preroll_started,
                                SUM(IF(ev.event_type_id = 25, 1,NULL)) count_midroll_started,
                                SUM(IF(ev.event_type_id = 26, 1,NULL)) count_postroll_started,
                                SUM(IF(ev.event_type_id = 27, 1,NULL)) count_overlay_started,
                                SUM(IF(ev.event_type_id = 28, 1,NULL)) count_preroll_clicked,
                                SUM(IF(ev.event_type_id = 29, 1,NULL)) count_midroll_clicked,
                                SUM(IF(ev.event_type_id = 30, 1,NULL)) count_postroll_clicked,
                                SUM(IF(ev.event_type_id = 31, 1,NULL)) count_overlay_clicked,
                                SUM(IF(ev.event_type_id = 32, 1,NULL)) count_preroll_25,
                                SUM(IF(ev.event_type_id = 33, 1,NULL)) count_preroll_50,
                                SUM(IF(ev.event_type_id = 34, 1,NULL)) count_preroll_75,
                                SUM(IF(ev.event_type_id = 35, 1,NULL)) count_midroll_25,
                                SUM(IF(ev.event_type_id = 36, 1,NULL)) count_midroll_50,
                                SUM(IF(ev.event_type_id = 37, 1,NULL)) count_midroll_75,
                                SUM(IF(ev.event_type_id = 38, 1,NULL)) count_postroll_25,
                                SUM(IF(ev.event_type_id = 39, 1,NULL)) count_postroll_50,
                                SUM(IF(ev.event_type_id = 40, 1,NULL)) count_postroll_75
                                FROM ',v_table_name,' as ev ', v_use_index, ' , dwh_dim_entries e',v_join_table,
                                        ' WHERE ev.event_type_id BETWEEN 2 AND 40
                                        AND ev.event_date_id  = DATE(''',p_date_val,''')*1
                                        AND ev.event_hour_id = ',p_hour_id,'
                                        AND e.entry_media_type_id IN (1,2,5,6)  /* allow only video & audio & mix */
                                AND e.entry_id = ev.entry_id ' ,v_join_condition,
                                ' GROUP BY partner_id,event_date_id, event_hour_id',v_aggr_id_field,';');

                        PREPARE stmt FROM  @s;
                        EXECUTE stmt;
                        DEALLOCATE PREPARE stmt;

                        SET @s = CONCAT('INSERT INTO ',v_aggr_table,'
                                        (partner_id
                                        ,date_id
                                        ,hour_id
                                        ',REPLACE(v_aggr_id_field,'e.',''),'
                                        ,sum_time_viewed
                                        ,count_time_viewed)
                                        SELECT partner_id, event_date_id, event_hour_id',v_aggr_id_field,',
                                        SUM(duration / 60 / 4 * (if(v_25>v_play AND v_play <> 0,v_play,v_25)
                                                              +if(v_50>v_play AND v_play <> 0,v_play,v_50)
                                                              +if(v_75>v_play AND v_play <> 0,v_play,v_75)
                                                              +if(v_100>v_play AND v_play <> 0,v_play,v_100))) sum_time_viewed,
                                        COUNT(DISTINCT s_play) count_time_viewed
                                        FROM(
                                        SELECT ev.partner_id, ev.event_date_id, ev.event_hour_id',v_aggr_id_field,', ev.session_id,
                                                MAX(duration) duration,
                                                COUNT(IF(ev.event_type_id IN (4),1,NULL)) v_25,
                                                COUNT(IF(ev.event_type_id IN (5),1,NULL)) v_50,
                                                COUNT(IF(ev.event_type_id IN (6),1,NULL)) v_75,
                                                COUNT(IF(ev.event_type_id IN (7),1,NULL)) v_100,
                                                COUNT( IF(ev.event_type_id IN (3),1,NULL)) v_play,
                                                MAX(IF(event_type_id IN (3),session_id,NULL)) s_play
                                        FROM ',v_table_name,' as ev ', v_use_index, ' , dwh_dim_entries e',v_join_table,
                                        ' WHERE ev.event_date_id  = DATE(''',p_date_val,''')*1
                                                AND ev.event_hour_id = ',p_hour_id,'
                                                AND e.entry_media_type_id IN (1,2,5,6)  /* allow only video & audio & mix */
                                                AND e.entry_id = ev.entry_id
                                                AND ev.event_type_id IN(3,4,5,6,7) /* time viewed only when player reaches 25,50,75,100 */ ',v_join_condition,
                                        ' GROUP BY ev.partner_id, ev.event_date_id, ev.event_hour_id , ev.entry_id',v_aggr_id_field,',ev.session_id) e
                                        GROUP BY partner_id, event_date_id, event_hour_id',v_aggr_id_field,'
                                        ON DUPLICATE KEY UPDATE
                                        sum_time_viewed = values(sum_time_viewed), count_time_viewed=values(count_time_viewed);');

                                PREPARE stmt FROM  @s;
                                EXECUTE stmt;
                                DEALLOCATE PREPARE stmt;

                        ELSE
                                SET @s = CONCAT('INSERT INTO ',v_aggr_table,'
                                        (partner_id
                                        ,date_id
                                        ,hour_id
                                        ',REPLACE(v_aggr_id_field,'e.',''),'
                                        ,count_loads
                                        ,count_plays
                                        )
                                SELECT  ev.partner_id,ev.event_date_id, event_hour_id',v_aggr_id_field,',
                                SUM(IF(ev.event_type_id = 2, 1,NULL)) count_loads,
                                SUM(IF(ev.event_type_id = 3, 1,NULL)) count_plays
                                FROM ',v_table_name,' as ev ', v_use_index, ' , dwh_dim_entries e',v_join_table,
                                        ' WHERE ev.event_type_id IN (2,3)
                                        AND ev.event_date_id  = DATE(''',p_date_val,''')*1
                                        AND ev.event_hour_id = ',p_hour_id,'
                                        AND e.entry_type_id = 7  /* allow only live entries */
                                AND e.entry_id = ev.entry_id ' ,v_join_condition,
                                ' GROUP BY partner_id,event_date_id, event_hour_id',v_aggr_id_field,';');

                                PREPARE stmt FROM  @s;
                                EXECUTE stmt;
                                DEALLOCATE PREPARE stmt;
                        END IF;

                        SET extra = CONCAT('post_aggregation_',p_aggr_name);
                        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME=extra) THEN
                                SET @ss = CONCAT('CALL ',extra,'(''', p_date_val,''',',p_hour_id,');');
                                PREPARE stmt1 FROM  @ss;
                                EXECUTE stmt1;
                                DEALLOCATE PREPARE stmt1;
                        END IF ;

        END IF;

        SET @s = CONCAT('UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = ''',p_aggr_name,''' AND date_id = ''',DATE(p_date_val)*1,''' AND hour_id =',p_hour_id);
        PREPARE stmt FROM  @s;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day_api_calls`(p_date_val DATE, p_hour_id INT)
BEGIN
        DECLARE v_ignore DATE;
        DECLARE v_from_archive DATE;
        DECLARE v_table_name VARCHAR(100);
        DECLARE v_aggr_table VARCHAR(100);
        DECLARE v_aggr_id_field_str VARCHAR(100);
 
        SELECT aggr_table, IF(IFNULL(aggr_id_field,'')='','', CONCAT(', ', aggr_id_field)) aggr_id_field
        INTO  v_aggr_table, v_aggr_id_field_str
        FROM kalturadw_ds.aggr_name_resolver
        WHERE aggr_name = 'api_calls';
 
 
        UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'api_calls' AND date_id = DATE(p_date_val)*1 AND hour_id = p_hour_id;
 
        SELECT MAX(DATE(NOW() - INTERVAL archive_delete_days_back DAY))
        INTO v_ignore
        FROM kalturadw_ds.retention_policy
        WHERE table_name IN ('dwh_fact_api_calls');
 
        IF (p_date_val >= v_ignore) THEN
                SET @s = CONCAT('DELETE FROM kalturadw.',v_aggr_table, ' WHERE date_id = DATE(\'',p_date_val,'\')*1 and hour_id = ', p_hour_id);
		
                PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
                SELECT DATE(archive_last_partition)
                INTO v_from_archive
                FROM kalturadw_ds.retention_policy
                WHERE table_name = 'dwh_fact_api_calls';
                IF (p_date_val >= v_from_archive) THEN
                        SET v_table_name = 'dwh_fact_api_calls';
                ELSE
                        SET v_table_name = 'dwh_fact_api_calls_archive';
                END IF;
                SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id ', v_aggr_id_field_str,', count_calls,count_is_admin,count_is_in_multi_request,count_success,sum_duration_msecs)'
				'SELECT partner_id, api_call_date_id, api_call_hour_id hour_id', v_aggr_id_field_str,', count(*), sum(is_admin), sum(is_in_multi_request), sum(success), sum(duration_msecs)
				FROM ', v_table_name, '    WHERE api_call_date_id=date(\'',p_date_val,'\')*1 AND api_call_hour_id = ',p_hour_id,'
				GROUP BY partner_id', v_aggr_id_field_str);
		
                PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
        END IF;
        UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'api_calls' AND date_id = DATE(p_date_val)*1 AND hour_id = p_hour_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day_bandwidth`(p_date_val DATE, p_aggr_name VARCHAR(100))
BEGIN
	DECLARE v_ignore DATE;
	DECLARE v_from_archive DATE;
        DECLARE v_table_name VARCHAR(100);
	DECLARE v_aggr_table VARCHAR(100);
	DECLARE v_aggr_id_field_str VARCHAR(100);
	
	UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = p_aggr_name AND date_id = DATE(p_date_val)*1;
	SELECT MAX(DATE(NOW() - INTERVAL archive_delete_days_back DAY))
	INTO v_ignore
	FROM kalturadw_ds.retention_policy
	WHERE table_name IN('dwh_fact_bandwidth_usage', 'dwh_fact_fms_sessions');
	
	IF (p_date_val >= v_ignore) THEN 
		
		SELECT aggr_table, IF(IFNULL(aggr_id_field,'')='','', CONCAT(', ', aggr_id_field)) aggr_id_field
		INTO  v_aggr_table, v_aggr_id_field_str
		FROM kalturadw_ds.aggr_name_resolver
		WHERE aggr_name = p_aggr_name;
		
		SET @s = CONCAT('UPDATE kalturadw.',v_aggr_table, ' SET count_bandwidth_kb = NULL WHERE date_id = DATE(\'',p_date_val,'\')*1');
		PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
		
		
		SELECT DATE(archive_last_partition)
		INTO v_from_archive
		FROM kalturadw_ds.retention_policy
		WHERE table_name = 'dwh_fact_bandwidth_usage';
	
                IF (p_date_val >= v_from_archive) THEN 
                        SET v_table_name = 'dwh_fact_bandwidth_usage';
                ELSE
                        SET v_table_name = 'dwh_fact_bandwidth_usage_archive';
                END IF;
                
		SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id ', v_aggr_id_field_str,', count_bandwidth_kb)'
				'SELECT partner_id, MAX(activity_date_id), 0 hour_id', v_aggr_id_field_str,', SUM(bandwidth_bytes)/1024 count_bandwidth
				FROM ', v_table_name, '	WHERE activity_date_id=date(\'',p_date_val,'\')*1
				GROUP BY partner_id', v_aggr_id_field_str,'
				ON DUPLICATE KEY UPDATE	count_bandwidth_kb=IFNULL(count_bandwidth_kb,0) + VALUES(count_bandwidth_kb)');
	

		PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
			
		
		SELECT DATE(archive_last_partition)
		INTO v_from_archive
		FROM kalturadw_ds.retention_policy
		WHERE table_name = 'dwh_fact_fms_sessions';
		
		IF (p_date_val >= v_from_archive) THEN 
                        SET v_table_name = 'dwh_fact_fms_sessions';
                ELSE
                        SET v_table_name = 'dwh_fact_fms_sessions_archive';
                END IF;

		SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id', v_aggr_id_field_str,', count_bandwidth_kb)
				SELECT session_partner_id, MAX(session_date_id), 0 hour_id', v_aggr_id_field_str,', SUM(total_bytes)/1024 count_bandwidth 
				FROM ', v_table_name, ' WHERE session_date_id=date(\'',p_date_val,'\')*1
				GROUP BY session_partner_id', v_aggr_id_field_str,'
				ON DUPLICATE KEY UPDATE	count_bandwidth_kb=IFNULL(count_bandwidth_kb,0) + VALUES(count_bandwidth_kb)');
		PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
	
	END IF;
	
	UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = p_aggr_name AND date_id = DATE(p_date_val)*1;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day_errors`(p_date_val DATE, p_hour_id INT)
BEGIN
        DECLARE v_ignore DATE;
        DECLARE v_from_archive DATE;
        DECLARE v_table_name VARCHAR(100);
        DECLARE v_aggr_table VARCHAR(100);
        DECLARE v_aggr_id_field_str VARCHAR(100);
 
        SELECT aggr_table, IF(IFNULL(aggr_id_field,'')='','', CONCAT(', ', aggr_id_field)) aggr_id_field
        INTO  v_aggr_table, v_aggr_id_field_str
        FROM kalturadw_ds.aggr_name_resolver
        WHERE aggr_name = 'errors';
 
 
        UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'errors' AND date_id = DATE(p_date_val)*1 AND hour_id = p_hour_id;
 
        SELECT MAX(DATE(NOW() - INTERVAL archive_delete_days_back DAY))
        INTO v_ignore
        FROM kalturadw_ds.retention_policy
        WHERE table_name IN ('dwh_fact_errors');
 
        IF (p_date_val >= v_ignore) THEN
                SET @s = CONCAT('DELETE FROM kalturadw.',v_aggr_table, ' WHERE date_id = DATE(\'',p_date_val,'\')*1 and hour_id = ', p_hour_id);
		
                PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
                SELECT DATE(archive_last_partition)
                INTO v_from_archive
                FROM kalturadw_ds.retention_policy
                WHERE table_name = 'dwh_fact_errors';
 
                IF (p_date_val >= v_from_archive) THEN
                        SET v_table_name = 'dwh_fact_errors';
                ELSE
                        SET v_table_name = 'dwh_fact_errors_archive';
                END IF;
                SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id ', v_aggr_id_field_str,', count_errors)'
				'SELECT partner_id, error_date_id, error_hour_id hour_id', v_aggr_id_field_str,', count(*)
				FROM ', v_table_name, '    WHERE error_date_id=date(\'',p_date_val,'\')*1 AND error_hour_id = ',p_hour_id,'
				GROUP BY partner_id', v_aggr_id_field_str);
		
                PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
        END IF;
        UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'errors' AND date_id = DATE(p_date_val)*1 AND hour_id = p_hour_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`etl`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day_ingestion`(p_date_id INT(11))
BEGIN
	DECLARE v_entry_with_flavor_failed_count INT(11);
	DECLARE v_all_convert_entries_count INT(11);
	
	UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'ingestion' AND date_id = p_date_id;
		
	            
	SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, normal_wait_time_count, medium_wait_time_count, long_wait_time_count, extremely_long_wait_time_count, stuck_wait_time_count, total_ff_wait_time_sec, median_ff_wait_time_sec) '
					'SELECT created_date_id, COUNT(IF(wait_time< 5,1,null)) normal_wait_time, COUNT(IF(wait_time>=5 AND wait_time < 180,1,null)) medium_wait_time, COUNT(IF(wait_time>=180 AND wait_time<900,1,null)) long_wait_time,
					COUNT(IF(wait_time>=900 AND wait_time < 3600,1,null)) extremely_long_wait_time_count, COUNT(IF(wait_time>=3600,1,null)) stuck, SUM(IF(wait_time>0,wait_time, 0)), calc_median_ff_convert_job_wait_time(' , p_date_id ,')'
					' FROM kalturadw.dwh_fact_convert_job
					WHERE is_ff = 1 
					AND created_date_id = ' ,p_date_id , 
					' ON DUPLICATE KEY UPDATE	
						normal_wait_time_count=VALUES(normal_wait_time_count),
						medium_wait_time_count=VALUES(medium_wait_time_count),
						long_wait_time_count=VALUES(long_wait_time_count),
						extremely_long_wait_time_count=VALUES(extremely_long_wait_time_count),
						stuck_wait_time_count=VALUES(stuck_wait_time_count),
						total_ff_wait_time_sec=VALUES(total_ff_wait_time_sec),
						median_ff_wait_time_sec=VALUES(median_ff_wait_time_sec);');
	
		
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
	
	SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, success_entries_count, failed_entries_count)'
					'SELECT ' , p_date_id, ' ,COUNT(IF(entry_status_id=2, 1, NULL)) entries_success, COUNT(IF(entry_status_id=-1, 1, NULL)) entries_failure
					FROM 
					(SELECT distinct(entry.entry_id), entry_status_id
					FROM kalturadw.dwh_dim_entries entry, kalturadw.dwh_dim_batch_job_sep job
					WHERE entry.entry_id = job.entry_id
					AND entry.created_at BETWEEN DATE(' , p_date_id, ') AND DATE(', p_date_id, ') + INTERVAL 1 DAY',
					' AND entry.entry_media_type_id IN (1,5)
					AND job_type_id = 10) e
					ON DUPLICATE KEY UPDATE	
						success_entries_count=VALUES(success_entries_count),
						failed_entries_count=VALUES(failed_entries_count);');
	
		
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
	
	SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, success_convert_job_count, failed_convert_job_count)'
					'SELECT created_date_id, COUNT(IF(status_id=5,1,NULL)) convert_job_success, COUNT(IF(status_id=6 OR status_id = 10,1,NULL)) convert_job_failure 
					 FROM kalturadw.dwh_fact_convert_job
					 WHERE created_date_id = ', p_date_id,
					 ' ON DUPLICATE KEY UPDATE	
						success_convert_job_count=VALUES(success_convert_job_count),
						failed_convert_job_count=VALUES(failed_convert_job_count);');
						
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
	
	
    SELECT COUNT(DISTINCT(entry_id))
    INTO v_entry_with_flavor_failed_count
    FROM kalturadw.dwh_fact_convert_job
    WHERE created_date_id = p_date_id
    AND status_id IN (6,10);
    
    SELECT COUNT(DISTINCT(entry_id))
    INTO v_all_convert_entries_count
    FROM kalturadw.dwh_fact_convert_job
    WHERE created_date_id = p_date_id;
				
    
    SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, all_conversion_job_entries_count, failed_conversion_job_entries_count)'
			' VALUES (', p_date_id, ",", v_all_convert_entries_count, ",", v_entry_with_flavor_failed_count, ")"
			' ON DUPLICATE KEY UPDATE	
			all_conversion_job_entries_count=VALUES(all_conversion_job_entries_count),
			failed_conversion_job_entries_count=VALUES(failed_conversion_job_entries_count);');
	
		
    PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    
			
	SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, total_wait_time_sec, convert_jobs_count)'
					'SELECT created_date_id, SUM(IF(wait_time>0, wait_time, 0)), COUNT(id)
					 FROM kalturadw.dwh_fact_convert_job
					 WHERE created_date_id = ' ,p_date_id,
					 ' ON DUPLICATE KEY UPDATE	
						total_wait_time_sec=VALUES(total_wait_time_sec),
						convert_jobs_count=VALUES(convert_jobs_count);');
	
		
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_partner_ingestion (date_id, partner_id, total_conversion_sec)'
					'SELECT created_date_id, partner_id, SUM(conversion_time)
					 FROM kalturadw.dwh_fact_convert_job
					 WHERE created_date_id = ' ,p_date_id,
					 ' AND conversion_time > 0
					 GROUP BY partner_id' ,
					 ' ON DUPLICATE KEY UPDATE	
						total_conversion_sec=VALUES(total_conversion_sec);');
	
		
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    
		
	UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'ingestion' AND date_id = p_date_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day_partner_storage`(date_val DATE)
BEGIN
    DELETE FROM kalturadw.dwh_hourly_partner_usage WHERE date_id = DATE(date_val)*1 AND IFNULL(count_bandwidth_kb,0) = 0 AND IFNULL(count_transcoding_mb,0) = 0 AND bandwidth_source_id = 1;
    UPDATE kalturadw.dwh_hourly_partner_usage SET added_storage_mb = 0, deleted_storage_mb = 0, aggr_storage_mb=NULL WHERE date_id = DATE(date_val)*1 AND (IFNULL(count_bandwidth_kb,0) > 0 OR IFNULL(count_transcoding_mb,0) > 0);
	
	DROP TABLE IF EXISTS temp_aggr_storage;
	CREATE TEMPORARY TABLE temp_aggr_storage(
		partner_id      	INT(11) NOT NULL,
		date_id     		INT(11) NOT NULL,
		hour_id	 		TINYINT(4) NOT NULL,
		added_storage_mb	DECIMAL(19,4) NOT NULL,
		deleted_storage_mb      DECIMAL(19,4) NOT NULL
	) ENGINE = MEMORY;
      
	INSERT INTO 	temp_aggr_storage (partner_id, date_id, hour_id, added_storage_mb, deleted_storage_mb)
   	SELECT 		partner_id, MAX(entry_size_date_id), 0 hour_id, SUM(IF(entry_additional_size_kb>0,entry_additional_size_kb,0))/1024 added_storage_mb, SUM(IF(entry_additional_size_kb<0,entry_additional_size_kb*-1,0))/1024 deleted_storage_mb 
	FROM 		dwh_fact_entries_sizes
	WHERE		entry_size_date_id=DATE(date_val)*1
	GROUP BY 	partner_id;
	
	INSERT INTO 	kalturadw.dwh_hourly_partner_usage (partner_id, date_id, hour_id, bandwidth_source_id, added_storage_mb, deleted_storage_mb, aggr_storage_mb)
	SELECT		partner_id, DATE(date_val)*1, 0 hour_id, 1, 0, 0, aggr_storage_mb
	FROM        kalturadw.dwh_hourly_partner_usage
	WHERE       date_id = DATE(date_val - INTERVAL 1 DAY)*1
	AND         bandwidth_source_id = 1
	ON DUPLICATE KEY UPDATE added_storage_mb=VALUES(added_storage_mb), deleted_storage_mb=VALUES(deleted_storage_mb), aggr_storage_mb = VALUES(aggr_storage_mb);
	
	INSERT INTO 	kalturadw.dwh_hourly_partner_usage (partner_id, date_id, hour_id, bandwidth_source_id, added_storage_mb, deleted_storage_mb, aggr_storage_mb)
	SELECT		aggr.partner_id, aggr.date_id, aggr.hour_id, 1, aggr.added_storage_mb, aggr.deleted_storage_mb, aggr.added_storage_mb - aggr.deleted_storage_mb
	FROM		temp_aggr_storage aggr 
	ON DUPLICATE KEY UPDATE added_storage_mb=VALUES(added_storage_mb), deleted_storage_mb=VALUES(deleted_storage_mb), aggr_storage_mb=IFNULL(aggr_storage_mb,0) + VALUES(aggr_storage_mb) ;
	
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day_play`(p_date_val DATE,p_hour_id INT(11), p_aggr_name VARCHAR(100))
BEGIN
	DECLARE v_aggr_table VARCHAR(100);
	DECLARE v_aggr_id_field VARCHAR(100);
	DECLARE extra VARCHAR(100);
	DECLARE v_from_archive DATE;
	DECLARE v_ignore DATE;
	DECLARE v_table_name VARCHAR(100);
	DECLARE v_join_table VARCHAR(100);
	DECLARE v_join_condition VARCHAR(200);
	DECLARE v_use_index VARCHAR(100);
    		
	SELECT DATE(NOW() - INTERVAL archive_delete_days_back DAY), DATE(archive_last_partition)
	INTO v_ignore, v_from_archive
	FROM kalturadw_ds.retention_policy
	WHERE table_name = 'dwh_fact_plays';	
	
	IF (p_date_val >= v_ignore) THEN 
		
			SELECT aggr_table, aggr_id_field
			INTO  v_aggr_table, v_aggr_id_field
			FROM kalturadw_ds.aggr_name_resolver
			WHERE aggr_name = p_aggr_name;	
			
			SET extra = CONCAT('pre_aggregation_',p_aggr_name);
			IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME=extra) THEN
			    SET @ss = CONCAT('CALL ',extra,'(''', p_date_val,''',',p_hour_id,');'); 
			    PREPARE stmt1 FROM  @ss;
			    EXECUTE stmt1;
			    DEALLOCATE PREPARE stmt1;
			END IF ;
		
			IF (v_aggr_table <> '') THEN 
				SET @s = CONCAT('delete from ',v_aggr_table,' where date_id = DATE(''',p_date_val,''')*1 and hour_id = ',p_hour_id);
				PREPARE stmt FROM  @s;
				EXECUTE stmt;
				DEALLOCATE PREPARE stmt;	
			END IF;
			
			SET @s = CONCAT('INSERT INTO aggr_managment(aggr_name, date_id, hour_id, data_insert_time)
					VALUES(''',p_aggr_name,''',''',DATE(p_date_val)*1,''',',p_hour_id,',NOW())
					ON DUPLICATE KEY UPDATE data_insert_time = values(data_insert_time)');
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		
			IF (p_date_val >= v_from_archive) THEN 
				SET v_table_name = 'dwh_fact_plays';
				SET v_use_index = 'USE INDEX (play_hour_id_play_date_id_partner_id)';
			ELSE
				SET v_table_name = 'dwh_fact_plays_archive';
				SET v_use_index = '';
			END IF;
			
			SELECT aggr_table, CONCAT(
							IF(aggr_id_field <> '', CONCAT(',', aggr_id_field),'') ,
							IF(dim_id_field <> '', 	CONCAT(', e.', REPLACE(dim_id_field,',',', e.')), '')
						  )
			INTO  v_aggr_table, v_aggr_id_field
			FROM kalturadw_ds.aggr_name_resolver
			WHERE aggr_name = p_aggr_name;
			
			SELECT IF(join_table <> '' , CONCAT(',', join_table), ''), IF(join_table <> '', CONCAT(' AND ev.' ,join_id_field,'=',join_table,'.',join_id_field), '')
			INTO v_join_table, v_join_condition
			FROM kalturadw_ds.aggr_name_resolver
			WHERE aggr_name = p_aggr_name;
			
			
			SET @s = CONCAT('UPDATE aggr_managment SET start_time = NOW()
					WHERE aggr_name = ''',p_aggr_name,''' AND date_id = ''',DATE(p_date_val)*1,''' AND hour_id = ',p_hour_id);
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
			
			IF ( v_aggr_table <> '' ) THEN
				SET @s = CONCAT('INSERT INTO ',v_aggr_table,'
					(partner_id
					,date_id
					,hour_id
					',REPLACE(v_aggr_id_field,'e.',''),' 
					,client_tag_id
					,count_plays 
					) 
				SELECT  ev.partner_id,ev.play_date_id, play_hour_id',v_aggr_id_field,',
				client_tag_id,
				count(1) count_plays
				FROM ',v_table_name,' as ev ', v_use_index, v_join_table,
					' WHERE ev.play_date_id  = DATE(''',p_date_val,''')*1
					AND ev.play_hour_id = ',p_hour_id ,v_join_condition, 
				' GROUP BY partner_id,play_date_id, play_hour_id, client_tag_id',v_aggr_id_field,';');
			
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
						
				
				SET extra = CONCAT('post_aggregation_',p_aggr_name);
				IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME=extra) THEN
					SET @ss = CONCAT('CALL ',extra,'(''', p_date_val,''',',p_hour_id,');'); 
					PREPARE stmt1 FROM  @ss;
					EXECUTE stmt1;
					DEALLOCATE PREPARE stmt1;
				END IF ;
				
			END IF;	  
			
		
	END IF;
	
	SET @s = CONCAT('UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = ''',p_aggr_name,''' AND date_id = ''',DATE(p_date_val)*1,''' AND hour_id =',p_hour_id);
	PREPARE stmt FROM  @s;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
		
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day_transcoding_usage`(p_date_id INT(11))
BEGIN
	UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'transcoding_usage' AND date_id = p_date_id;
	
    UPDATE kalturadw.dwh_hourly_partner_usage SET count_transcoding_mb = 0 WHERE date_id = p_date_id AND bandwidth_source_id = 1;
	
	INSERT INTO kalturadw.dwh_hourly_partner_usage (partner_id, date_id, hour_id, bandwidth_source_id, count_transcoding_mb) 
	SELECT partner_id, p_date_id, 0 hour_id, 1, SUM(file_size)/1024/1024
	FROM kalturadw.dwh_dim_batch_job_sep
	WHERE created_date_id = p_date_id
	AND updated_date_id >= p_date_id
	AND job_type_id = 0
	AND status_id = 5
	AND file_size > 0
	GROUP BY partner_id
	ON DUPLICATE KEY UPDATE count_transcoding_mb=VALUES(count_transcoding_mb);
	
	UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'transcoding_usage' AND date_id = p_date_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_aggr_day_user_usage`(p_date_id INT(11))
BEGIN

    DECLARE v_date DATETIME;
    SET v_date = DATE(p_date_id);
	
    UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'user_storage_usage' AND date_id = p_date_id;
    
    DROP TABLE IF EXISTS temp_aggr_storage;
    CREATE TEMPORARY TABLE temp_aggr_storage(
        partner_id          INT(11) NOT NULL,
        kuser_id            INT(11) NOT NULL,
        added_storage_kb    DECIMAL(19,4) NOT NULL DEFAULT 0.0000,
        deleted_storage_kb  DECIMAL(19,4) NOT NULL DEFAULT 0.0000
    ) ENGINE = MEMORY;
    
    ALTER TABLE temp_aggr_storage ADD INDEX index_1 (kuser_id);  
    
    INSERT INTO     temp_aggr_storage (partner_id, kuser_id, added_storage_kb, deleted_storage_kb)
    SELECT         e.partner_id, e.kuser_id, SUM(IF(f.entry_additional_size_kb > 0,entry_additional_size_kb,0)),SUM(IF(f.entry_additional_size_kb < 0,entry_additional_size_kb*-1,0))
    FROM         dwh_fact_entries_sizes f, dwh_dim_entries e
    WHERE        entry_size_date_id=p_date_id
    AND          f.entry_id = e.entry_id
    AND          e.entry_type_id IN (1,2,7,10)
    GROUP BY     e.kuser_id, e.partner_id;
    
    DROP TABLE IF EXISTS entries_prev_owner;
    CREATE TEMPORARY TABLE entries_prev_owner AS
    SELECT partner_id, entry_id, prev_kuser_id, kuser_id 
    FROM dwh_dim_entries
    WHERE prev_kuser_id IS NOT NULL
	AND updated_at >= v_date
    AND IFNULL(kuser_updated_date_id,-1) = p_date_id
    AND IFNULL(created_date_id, -1) <> p_date_id
    AND entry_type_id IN (1,2,7,10);
 
    ALTER TABLE entries_prev_owner ADD INDEX index_1 (kuser_id);
    
    INSERT INTO  temp_aggr_storage (partner_id, kuser_id, added_storage_kb, deleted_storage_kb)
    SELECT       o.partner_id, o.prev_kuser_id, 0, SUM(f.entry_additional_size_kb)
    FROM         dwh_fact_entries_sizes f, entries_prev_owner o
    WHERE        f.entry_id = o.entry_id
    AND          f.entry_size_date_id < p_date_id
	AND          o.prev_kuser_id <> -1
    GROUP BY     o.prev_kuser_id, o.partner_id;
    
    
    INSERT INTO  temp_aggr_storage (partner_id, kuser_id, added_storage_kb, deleted_storage_kb)
    SELECT       o.partner_id, o.kuser_id, SUM(f.entry_additional_size_kb), 0
    FROM         dwh_fact_entries_sizes f, entries_prev_owner o
    WHERE        f.entry_id = o.entry_id
    AND          f.entry_size_date_id < p_date_id
	AND          o.kuser_id <> -1
    GROUP BY     o.kuser_id, o.partner_id;
    
    DROP TABLE IF EXISTS temp_aggr_entries;
    CREATE TEMPORARY TABLE temp_aggr_entries(
        partner_id          INT(11) NOT NULL,
        kuser_id             INT(11) NOT NULL,
        added_entries    INT(11) NOT NULL DEFAULT 0,
        deleted_entries  INT(11) NOT NULL DEFAULT 0,
        added_msecs INT(11) NOT NULL DEFAULT 0,
        deleted_msecs INT(11) NOT NULL DEFAULT 0
        
    ) ENGINE = MEMORY; 
    
    ALTER TABLE temp_aggr_entries ADD INDEX index_1 (`kuser_id`);
    
    INSERT INTO temp_aggr_entries(partner_id, kuser_id, added_entries, deleted_entries, added_msecs, deleted_msecs)
    SELECT partner_id, kuser_id,
    SUM(IF((entry_status_id <> 3 AND ((IFNULL(created_date_id,-1) = p_date_id AND IFNULL(created_date_id,-1) >= IFNULL(kuser_updated_date_id,-1)) OR IFNULL(kuser_updated_date_id,-1) = p_date_id))
		OR (entry_status_id = 3 AND IFNULL(updated_date_id,-1) <> p_date_id AND ((IFNULL(created_date_id,-1) = p_date_id AND IFNULL(created_date_id,-1) >= IFNULL(kuser_updated_date_id,-1)) OR IFNULL(kuser_updated_date_id,-1) = p_date_id)),1,0)),
    SUM(IF(entry_status_id = 3 AND (IFNULL(created_date_id,-1) <> p_date_id AND IFNULL(kuser_updated_date_id,-1) <> p_date_id),1,0)),
    SUM(IF((entry_status_id <> 3 AND ((IFNULL(created_date_id,-1) = p_date_id AND IFNULL(created_date_id,-1) >= IFNULL(kuser_updated_date_id,-1)) OR IFNULL(kuser_updated_date_id,-1) = p_date_id))
		OR (entry_status_id = 3 AND IFNULL(updated_date_id,-1) <> p_date_id AND ((IFNULL(created_date_id,-1) = p_date_id AND IFNULL(created_date_id,-1) >= IFNULL(kuser_updated_date_id,-1)) OR IFNULL(kuser_updated_date_id,-1) = p_date_id)),length_in_msecs,0)),
    SUM(IF(entry_status_id = 3 AND (IFNULL(created_date_id,-1) <> p_date_id AND IFNULL(kuser_updated_date_id,-1) <> p_date_id),length_in_msecs,0))
    FROM dwh_dim_entries e
    WHERE updated_at >= v_date AND (updated_at <= v_date + INTERVAL 1 DAY 
			OR IFNULL(created_date_id , -1) = p_date_id
			OR IFNULL(kuser_updated_date_id,-1) = p_date_id)
    AND e.entry_type_id IN (1,2,7,10)
    GROUP BY kuser_id, partner_id;
    
    INSERT INTO temp_aggr_entries(partner_id, kuser_id, added_entries, deleted_entries, added_msecs, deleted_msecs)
    SELECT o.partner_id, o.prev_kuser_id, 0, COUNT(*), 0, SUM(length_in_msecs)
    FROM entries_prev_owner o, dwh_dim_entries e
    WHERE o.entry_id = e.entry_id
    GROUP BY o.prev_kuser_id, o.partner_id;
   
    
    DELETE FROM dwh_hourly_user_usage USING temp_aggr_storage, dwh_hourly_user_usage
    WHERE dwh_hourly_user_usage.partner_id = temp_aggr_storage.partner_id 
    AND dwh_hourly_user_usage.kuser_id = temp_aggr_storage.kuser_id 
    AND dwh_hourly_user_usage.date_id = p_date_id;
    
    DROP TABLE IF EXISTS latest_total;
    CREATE TEMPORARY TABLE latest_total(
        partner_id          INT(11) NOT NULL,
        kuser_id             INT(11) NOT NULL,
        total_storage_kb    DECIMAL(19,4) NOT NULL DEFAULT 0,
        total_entries  INT(11) NOT NULL DEFAULT 0,
        total_msecs INT(11) NOT NULL DEFAULT 0
        
    ) ENGINE = MEMORY; 
    ALTER TABLE latest_total ADD INDEX index_1 (kuser_id);
        
    
    INSERT INTO latest_total (partner_id, kuser_id, total_storage_kb, total_entries, total_msecs)
    SELECT u.partner_id, u.kuser_id, IFNULL(u.total_storage_kb,0), IFNULL(u.total_entries,0), IFNULL(u.total_msecs,0)
    FROM dwh_hourly_user_usage u JOIN (SELECT kuser_id, partner_id, MAX(date_id) AS date_id FROM dwh_hourly_user_usage WHERE date_id < p_date_id GROUP BY kuser_id, partner_id) MAX
          ON u.kuser_id = max.kuser_id AND u.date_id = max.date_id AND u.partner_id = max.partner_id; 
          
    INSERT INTO dwh_hourly_user_usage (partner_id, kuser_id, date_id, hour_id, added_storage_kb, deleted_storage_kb, total_storage_kb, added_entries, deleted_entries, total_entries, added_msecs, deleted_msecs, total_msecs)
    SELECT      aggr.partner_id, aggr.kuser_id, p_date_id, 0, SUM(added_storage_kb), SUM(deleted_storage_kb), SUM(added_storage_kb) - SUM(deleted_storage_kb) + IFNULL(latest_total.total_storage_kb,0),
                0, 0, IFNULL(latest_total.total_entries,0), 0, 0,  IFNULL(latest_total.total_msecs,0)
    FROM        temp_aggr_storage aggr LEFT JOIN latest_total ON aggr.kuser_id = latest_total.kuser_id AND aggr.partner_id = latest_total.partner_id
    WHERE added_storage_kb <> 0 OR deleted_storage_kb <> 0
    GROUP BY    aggr.kuser_id, aggr.partner_id;
        
    INSERT INTO dwh_hourly_user_usage (partner_id, kuser_id, date_id, hour_id, added_storage_kb, deleted_storage_kb, total_storage_kb, added_entries, deleted_entries, total_entries, added_msecs, deleted_msecs, total_msecs)
    SELECT         aggr.partner_id, aggr.kuser_id, p_date_id, 0, 0, 0, IFNULL(latest_total.total_storage_kb,0), SUM(added_entries), SUM(deleted_entries), SUM(added_entries) - SUM(deleted_entries) + IFNULL(latest_total.total_entries,0),
            SUM(added_msecs), SUM(deleted_msecs), SUM(added_msecs) - SUM(deleted_msecs) + IFNULL(latest_total.total_msecs,0)
    FROM         temp_aggr_entries aggr LEFT JOIN latest_total ON aggr.kuser_id = latest_total.kuser_id AND aggr.partner_id = latest_total.partner_id
    WHERE added_entries <> 0 OR added_msecs <> 0 OR deleted_entries <> 0 OR deleted_msecs <> 0
    GROUP BY     aggr.kuser_id, aggr.partner_id
    ON DUPLICATE KEY UPDATE added_entries = VALUES(added_entries), deleted_entries = VALUES(deleted_entries), total_entries=VALUES(total_entries), 
                            added_msecs=VALUES(added_msecs), deleted_msecs=VALUES(deleted_msecs), total_msecs=VALUES(total_msecs);
    
    
    UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'user_storage_usage' AND date_id = p_date_id; 
 
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_entries_sizes`(p_date_id INT(11))
BEGIN
                DECLARE v_date DATETIME;
                SET v_date = DATE(p_date_id);
                UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'storage_usage' AND date_id = p_date_id;
                
                DELETE FROM kalturadw.dwh_fact_entries_sizes WHERE entry_size_date_id = p_date_id;
                
                DROP TABLE IF EXISTS today_file_sync_subset; 
                
                CREATE TEMPORARY TABLE today_file_sync_subset AS
                SELECT DISTINCT s.id, s.partner_id, IFNULL(a.entry_id, object_id) entry_id, object_id, object_type, object_sub_type, s.created_at, s.status, IFNULL(file_size, 0) file_size
                FROM kalturadw.dwh_dim_file_sync s LEFT OUTER JOIN kalturadw.dwh_dim_flavor_asset a
                ON (object_type = 4 AND s.object_id = a.id AND a.entry_id IS NOT NULL AND a.ri_ind =0 AND s.partner_id = a.partner_id)
                WHERE s.ready_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
                AND object_type IN (1,4)
                AND original = 1
                AND s.STATUS IN (2,3,4)
				AND s.dc IN (0,1)
                AND s.partner_id NOT IN ( -1  , -2  , 0 , 99 );
                
                ALTER TABLE today_file_sync_subset ADD INDEX id (`id`);            
                
                DROP TABLE IF EXISTS today_latest_file_sync;
                CREATE TEMPORARY TABLE today_latest_file_sync AS
                SELECT MAX(created_at) created_at, partner_id, entry_id, object_id, object_type, object_sub_type FROM today_file_sync_subset
                GROUP BY partner_id, entry_id, object_id, object_type, object_sub_type;
                
                DROP TABLE IF EXISTS today_file_sync_max_version_ids;
                
                CREATE TEMPORARY TABLE today_file_sync_max_version_ids AS
				SELECT today_file_sync_subset.id
				FROM today_file_sync_subset, today_latest_file_sync
				WHERE today_latest_file_sync.created_at = today_file_sync_subset.created_at
				AND today_latest_file_sync.partner_id = today_file_sync_subset.partner_id
				AND today_latest_file_sync.entry_id = today_file_sync_subset.entry_id
				AND today_latest_file_sync.object_id = today_file_sync_subset.object_id
				AND today_latest_file_sync.object_type = today_file_sync_subset.object_type
				AND today_latest_file_sync.object_sub_type = today_file_sync_subset.object_sub_type;
                
				
		DROP TABLE IF EXISTS today_sizes;
		CREATE TEMPORARY TABLE today_sizes(
			partner_id          INT(11) NOT NULL,
			entry_id 			VARCHAR(60) NOT NULL,
			object_id 			VARCHAR(60) NOT NULL,
			object_type         TINYINT(4) NOT NULL,
			object_sub_type     TINYINT(4) NOT NULL,
			created_at          DATETIME NOT NULL,        
			STATUS              TINYINT(4) NOT NULL,
			file_size           BIGINT (20),
			UNIQUE KEY `unique_key` (`partner_id`, `entry_id`, `object_id`, `object_type`, `object_sub_type`)
		) ENGINE = MEMORY; 

                
		INSERT INTO today_sizes(partner_id, entry_id, object_id, object_type, object_sub_type, created_at, STATUS, file_size)
                SELECT original.partner_id, original.entry_id, original.object_id, original.object_type, original.object_sub_type, original.created_at, original.status, original.file_size 
                FROM today_file_sync_max_version_ids max_id, today_file_sync_subset original
                WHERE max_id.id = original.id
				ORDER BY original.status DESC
				ON DUPLICATE KEY UPDATE 
					STATUS = VALUES(STATUS),
					file_size = VALUES(file_size);

                
           
                INSERT INTO today_sizes
                                SELECT s.partner_id, IFNULL(a.entry_id, object_id) entry_id, object_id, object_type, object_sub_type, s.created_at, s.status, 0 file_size
                                FROM kalturadw.dwh_dim_file_sync s LEFT OUTER JOIN kalturadw.dwh_dim_flavor_asset a
                                ON (object_type = 4 AND s.object_id = a.id AND a.entry_id IS NOT NULL AND a.ri_ind =0 AND s.partner_id = a.partner_id)
                                WHERE s.updated_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
                                AND object_type IN (1,4)
                                AND original = 1
                                AND s.STATUS IN (3,4)
                                AND s.partner_id NOT IN ( -1  , -2  , 0 , 99 )
                ON DUPLICATE KEY UPDATE
                                file_size = IF((VALUES(created_at) > today_sizes.created_at) OR (VALUES(created_at)=today_sizes.created_at AND today_sizes.STATUS IN (3,4)), 0, today_sizes.file_size);       			
                                
                DROP TABLE IF EXISTS deleted_flavors;
                
                CREATE TEMPORARY TABLE deleted_flavors AS 
                SELECT DISTINCT partner_id, entry_id, id
                FROM kalturadw.dwh_dim_flavor_asset FORCE INDEX (deleted_at)
                WHERE STATUS = 3 AND deleted_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
                AND partner_id NOT IN (100  , -1  , -2  , 0 , 99 );
                                
                BEGIN
                                DECLARE v_deleted_flavor_partner_id INT;
                                DECLARE v_deleted_flavor_entry_id VARCHAR(60);
                                DECLARE v_deleted_flavor_id VARCHAR(60);
                                DECLARE done INT DEFAULT 0;
				DECLARE v_status TINYINT(4);
                                DECLARE deleted_flavors_cursor CURSOR FOR 
                                SELECT partner_id, entry_id, id  FROM deleted_flavors;
                                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
                                
                                OPEN deleted_flavors_cursor;
								
                                read_loop: LOOP
                                                FETCH deleted_flavors_cursor INTO v_deleted_flavor_partner_id, v_deleted_flavor_entry_id, v_deleted_flavor_id;
                                                IF done THEN
                                                                LEAVE read_loop;
                                                END IF;
												
												SELECT entry_status_id
												INTO v_status
												FROM kalturadw.dwh_dim_entries
												WHERE entry_id = v_deleted_flavor_entry_id;
												
												IF v_STATUS <> 3 THEN
													INSERT INTO today_sizes
																	SELECT v_deleted_flavor_partner_id, v_deleted_flavor_entry_id, object_id, object_type, object_sub_type, MAX(created_at), 3 STATUS, 0 file_size
																	FROM kalturadw.dwh_dim_file_sync
																	WHERE object_id = v_deleted_flavor_id AND object_type = 4 AND ready_at < v_date AND file_size > 0
																	GROUP BY object_id, object_type, object_sub_type
													ON DUPLICATE KEY UPDATE
																	file_size = VALUES(file_size);
												END IF;
                                END LOOP;
                                CLOSE deleted_flavors_cursor;
                END;
                
                
                
                DROP TABLE IF EXISTS today_deleted_entries;
                CREATE TEMPORARY TABLE today_deleted_entries AS 
                SELECT entry_id, partner_id FROM kalturadw.dwh_dim_entries
                WHERE modified_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
                AND partner_id NOT IN (100  , -1  , -2  , 0 , 99 )
                AND entry_status_id = 3
                AND entry_type_id = 1;                
                
                DELETE today_sizes FROM today_sizes, today_deleted_entries e 
                                WHERE today_sizes.entry_id = e.entry_id;
                
                ALTER TABLE today_sizes DROP INDEX unique_key;
                
                DROP TABLE IF EXISTS yesterday_file_sync_subset; 
                CREATE TEMPORARY TABLE yesterday_file_sync_subset AS
                SELECT f.id, f.partner_id, f.object_id, f.object_type, f.object_sub_type, f.created_at, IFNULL(f.file_size, 0) file_size
                FROM today_sizes today, kalturadw.dwh_dim_file_sync f
                WHERE f.object_id = today.object_id
                AND f.partner_id = today.partner_id
                AND f.object_type = today.object_type
                AND f.object_sub_type = today.object_sub_type
                AND f.ready_at < v_date
                AND f.original = 1
				AND f.dc IN (0,1)
                AND f.STATUS IN (2,3,4);
                
                
                
		DROP TABLE IF EXISTS yesterday_latest_file_sync;
                CREATE TEMPORARY TABLE yesterday_latest_file_sync AS
                SELECT MAX(created_at) created_at, partner_id, object_id, object_type, object_sub_type FROM yesterday_file_sync_subset
                GROUP BY partner_id, object_id, object_type, object_sub_type;
                
                DROP TABLE IF EXISTS yesterday_file_sync_max_version_ids;
                
                CREATE TEMPORARY TABLE yesterday_file_sync_max_version_ids AS
				SELECT yesterday_file_sync_subset.id
				FROM yesterday_file_sync_subset, yesterday_latest_file_sync
				WHERE yesterday_latest_file_sync.created_at = yesterday_file_sync_subset.created_at
				AND yesterday_latest_file_sync.partner_id = yesterday_file_sync_subset.partner_id
				AND yesterday_latest_file_sync.object_id = yesterday_file_sync_subset.object_id
				AND yesterday_latest_file_sync.object_type = yesterday_file_sync_subset.object_type
				AND yesterday_latest_file_sync.object_sub_type = yesterday_file_sync_subset.object_sub_type;
                
		
                DROP TABLE IF EXISTS yesterday_sizes;
                CREATE TEMPORARY TABLE yesterday_sizes AS
                SELECT original.partner_id, original.object_id, original.object_type, original.object_sub_type, original.file_size 
                FROM yesterday_file_sync_max_version_ids max_id, yesterday_file_sync_subset original
                WHERE max_id.id = original.id;
                
                
                INSERT INTO kalturadw.dwh_fact_entries_sizes (partner_id, entry_id, entry_additional_size_kb, entry_size_date, entry_size_date_id)
                SELECT t.partner_id, t.entry_id, ROUND(SUM(t.file_size - IFNULL(Y.file_size, 0))/1024, 3) entry_additional_size_kb, v_date, p_date_id 
                FROM today_sizes t LEFT OUTER JOIN yesterday_sizes Y 
                ON t.object_id = Y.object_id
                AND t.partner_id = Y.partner_id
                AND t.object_type = Y.object_type
                AND t.object_sub_type = Y.object_sub_type
                AND t.file_size <> Y.file_size
                GROUP BY t.partner_id, t.entry_id
                HAVING entry_additional_size_kb <> 0
                ON DUPLICATE KEY UPDATE 
                                entry_additional_size_kb = VALUES(entry_additional_size_kb);
                
                
                DROP TABLE IF EXISTS deleted_entries;
                CREATE TEMPORARY TABLE deleted_entries AS
                                SELECT es.partner_id partner_id, es.entry_id entry_id, v_date entry_size_date, p_date_id entry_size_date_id, -SUM(entry_additional_size_kb) entry_additional_size_kb
                                FROM today_deleted_entries e, kalturadw.dwh_fact_entries_sizes es
                                WHERE e.entry_id = es.entry_id 
                                                AND e.partner_id = es.partner_id 
                                                AND es.entry_size_date_id < p_date_id
                                GROUP BY es.partner_id, es.entry_id
                                HAVING SUM(entry_additional_size_kb) > 0;
                
                INSERT INTO kalturadw.dwh_fact_entries_sizes (partner_id, entry_id, entry_size_date, entry_size_date_id, entry_additional_size_kb)
                                SELECT partner_id, entry_id, entry_size_date, entry_size_date_id, entry_additional_size_kb FROM deleted_entries
                ON DUPLICATE KEY UPDATE 
                                entry_additional_size_kb = VALUES(entry_additional_size_kb);
                
                CALL kalturadw.calc_aggr_day_partner_storage(v_date);
                UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'storage_usage' AND date_id = p_date_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_partner_billing_data`(p_date_id INT(11),p_partner_id INT)
BEGIN
	SELECT
        FLOOR(date_id/100) month_id,
        SUM(aggr_storage_mb)/(IF(FLOOR(date_id/100)=FLOOR(LEAST(p_date_id,DATE(NOW())*1)/100),DAY(LEAST(p_date_id,DATE(NOW())*1)),DAY(LAST_DAY(date_id)))) avg_continuous_aggr_storage_mb,
        SUM(count_bandwidth_kb) sum_partner_bandwidth_kb
    FROM dwh_hourly_partner_usage 
    WHERE partner_id=p_partner_id AND hour_id = 0
    AND date_id <= LEAST(p_date_id,DATE(NOW())*1)
    GROUP BY month_id
	WITH ROLLUP;	
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_partner_overage`(p_month_id INTEGER)
BEGIN
		DROP TABLE IF EXISTS partner_quotas;
		CREATE TEMPORARY TABLE partner_quotas AS
		SELECT 	q.partner_id partner_id,
			IFNULL(p.partner_id,q.partner_id) usage_partner_id,
			q.max_monthly_bandwidth_kb,
			q.charge_monthly_bandwidth_kb_usd,
			q.charge_monthly_bandwidth_kb_unit,
			q.max_monthly_storage_mb,
			q.charge_monthly_storage_mb_usd,
			q.charge_monthly_storage_mb_unit,
			q.max_monthly_total_usage_mb,
			q.charge_monthly_total_usage_mb_usd,
			q.charge_monthly_total_usage_mb_unit,
			q.max_monthly_plays,
			q.charge_monthly_plays_usd,
			q.charge_monthly_plays_unit,
			q.max_monthly_entries,
			q.charge_monthly_entries_usd,
			q.charge_monthly_entries_unit
		FROM dwh_view_partners_monthly_billing q 
			LEFT OUTER JOIN kalturadw.dwh_dim_partners p ON (q.partner_id = p.partner_parent_id AND q.partner_group_type_id = 3)
		WHERE is_active = 1 AND q.month_id = p_month_id
        GROUP BY partner_id, usage_partner_id;
        

		DROP TABLE IF EXISTS partner_overages;
		CREATE TEMPORARY TABLE partner_overages (
				    partner_id       			INT(11),
				    included_bandwidth_kb    		BIGINT(20),
				    actual_bandwidth_kb	 		BIGINT(20),
				    charge_overage_bandwidth_kb		DECIMAL(15,3),
				    included_storage_mb    		BIGINT(20),
				    actual_storage_mb	 		BIGINT(20),
				    charge_overage_storage_mb 		DECIMAL(15,3),
				    included_total_usage_mb    		BIGINT(20),
				    actual_total_usage_mb		BIGINT(20),
				    charge_overage_total_usage_mb 	DECIMAL(15,3),
				    included_entries			BIGINT(20),
				    actual_entries			BIGINT(20),
				    charge_overage_entries		DECIMAL(15,3),
				    included_plays			BIGINT(20),
				    actual_plays			BIGINT(20),
				    charge_overage_plays		DECIMAL(15,3),
				    PRIMARY KEY (partner_id)
				  ) ENGINE = MEMORY;
	
		INSERT INTO partner_overages (partner_id, included_bandwidth_kb, actual_bandwidth_kb, charge_overage_bandwidth_kb, included_storage_mb, actual_storage_mb, charge_overage_storage_mb, included_total_usage_mb, actual_total_usage_mb, charge_overage_total_usage_mb)
			SELECT partner_id,
				included_bandwidth_kb,actual_bandwidth_kb,
				get_overage_charge(included_bandwidth_kb, actual_bandwidth_kb, charge_monthly_bandwidth_kb_unit, charge_monthly_bandwidth_kb_usd) charge_overage_bandwidth_kb,
				included_storage_mb, actual_storage_mb,
				get_overage_charge(included_storage_mb, actual_storage_mb, charge_monthly_storage_mb_unit, charge_monthly_storage_mb_usd) charge_overage_storage_mb, 
				included_total_usage_mb, actual_bandwidth_kb/1024+actual_storage_mb actual_total_usage_mb,
				get_overage_charge(included_total_usage_mb, actual_bandwidth_kb/1024+actual_storage_mb , charge_monthly_total_usage_mb_unit, charge_monthly_total_usage_mb_usd) charge_overage_total_usage_mb
			FROM
			(SELECT pq.partner_id, 
				MAX(max_monthly_bandwidth_kb) included_bandwidth_kb,
				IFNULL(SUM(count_bandwidth_kb),0) actual_bandwidth_kb,
				MAX(charge_monthly_bandwidth_kb_unit) charge_monthly_bandwidth_kb_unit,
				MAX(charge_monthly_bandwidth_kb_usd) charge_monthly_bandwidth_kb_usd,	
				MAX(max_monthly_storage_mb) included_storage_mb,
				IFNULL(SUM(aggr_storage_mb),0)/DAY(LAST_DAY(p_month_id*100+1)) actual_storage_mb,
				MAX(charge_monthly_storage_mb_unit) charge_monthly_storage_mb_unit,
				MAX(charge_monthly_storage_mb_usd) charge_monthly_storage_mb_usd,
				MAX(max_monthly_total_usage_mb) included_total_usage_mb,
				MAX(charge_monthly_total_usage_mb_unit) charge_monthly_total_usage_mb_unit,
				MAX(charge_monthly_total_usage_mb_usd) charge_monthly_total_usage_mb_usd
			FROM partner_quotas pq LEFT OUTER JOIN kalturadw.dwh_hourly_partner_usage partner_usage 
					ON (pq.usage_partner_id = partner_usage.partner_id AND partner_usage.date_id BETWEEN p_month_id*100 AND p_month_id*100+31)
			GROUP BY pq.partner_id) inner_q
			WHERE actual_bandwidth_kb > included_bandwidth_kb OR 
				actual_storage_mb > included_storage_mb OR 
				actual_bandwidth_kb/1024+actual_storage_mb > included_total_usage_mb
		ON DUPLICATE KEY UPDATE 
			included_bandwidth_kb=VALUES(included_bandwidth_kb),
			actual_bandwidth_kb=VALUES(actual_bandwidth_kb),
			charge_overage_bandwidth_kb=VALUES(charge_overage_bandwidth_kb),
			included_storage_mb=VALUES(included_storage_mb),
			actual_storage_mb=VALUES(actual_storage_mb),
			charge_overage_storage_mb=VALUES(charge_overage_storage_mb),
			included_total_usage_mb=VALUES(included_total_usage_mb),
			actual_total_usage_mb=VALUES(actual_total_usage_mb),
			charge_overage_total_usage_mb=VALUES(charge_overage_total_usage_mb);
			
		INSERT INTO partner_overages (partner_id, included_entries, actual_entries, charge_overage_entries)
			SELECT 	pq.partner_id, 
				MAX(max_monthly_entries) included_entries,
				COUNT(entries.entry_id) actual_entries,
				get_overage_charge(MAX(max_monthly_entries), COUNT(entries.entry_id), MAX(charge_monthly_entries_unit), MAX(charge_monthly_entries_usd)) charge_overage_entries
			FROM partner_quotas pq, kalturadw.dwh_dim_entries entries
			WHERE 	pq.usage_partner_id = entries.partner_id AND 
				entries.created_at < LAST_DAY(DATE(p_month_id*100+1)) + INTERVAL 1 DAY AND
				entries.entry_type_id IN (1,7) 
				AND entry_status_id NOT IN (-2,-1,3) 
			GROUP BY pq.partner_id
			HAVING actual_entries > included_entries
		ON DUPLICATE KEY UPDATE 
			included_entries=VALUES(included_entries),
			actual_entries=VALUES(actual_entries),
			charge_overage_entries=VALUES(charge_overage_entries);
	
		INSERT INTO partner_overages (partner_id, included_plays, actual_plays, charge_overage_plays)
			SELECT 	pq.partner_id, 
				MAX(max_monthly_plays) included_plays,
				SUM(count_plays) actual_plays,
				get_overage_charge(MAX(max_monthly_plays), SUM(count_plays), MAX(charge_monthly_plays_unit), MAX(charge_monthly_plays_usd)) charge_overage_plays
			FROM partner_quotas pq, kalturadw.dwh_hourly_partner plays
			WHERE 	pq.usage_partner_id = plays.partner_id AND
				date_id BETWEEN p_month_id*100 AND p_month_id*100+31
			GROUP BY pq.partner_id
			HAVING 	SUM(count_plays) > MAX(max_monthly_plays)
		ON DUPLICATE KEY UPDATE 
			included_plays=VALUES(included_plays),
			actual_plays=VALUES(actual_plays),
			charge_overage_plays=VALUES(charge_overage_plays);
	
		SELECT 	IF(children.partner_group_type_id=3,children.partner_id,parents.partner_id) parent_partner_id,
			IF(children.partner_group_type_id=3,children.partner_name,parents.partner_name) parent_partner_name,
			group_types.partner_group_type_name,
			IF(children.partner_group_type_id=3,NULL,children.partner_id) publisher_id,
			IF(children.partner_group_type_id=3,NULL,children.partner_name) publisher_name,
			d_cos.partner_class_of_service_name,
			d_vertical.partner_vertical_name,
			included_bandwidth_kb,
			actual_bandwidth_kb,
			charge_overage_bandwidth_kb,
			included_storage_mb, 
			actual_storage_mb, 
			charge_overage_storage_mb, 
			included_total_usage_mb, 
			actual_total_usage_mb, 
			charge_overage_total_usage_mb,
			included_entries, 
			actual_entries, 
			charge_overage_entries,
			included_plays, 
			actual_plays, 
			charge_overage_plays			
		FROM partner_overages po 
		INNER JOIN kalturadw.dwh_dim_partners children ON (po.partner_id = children.partner_id)
		LEFT OUTER JOIN kalturadw.dwh_dim_partners parents ON (children.partner_parent_id = parents.partner_id)
		INNER JOIN kalturadw.dwh_dim_partner_group_type group_types ON (IF(parents.partner_id IS NOT NULL, parents.partner_group_type_id,children.partner_group_type_id) = group_types.partner_group_type_id)
		LEFT OUTER JOIN kalturadw.dwh_dim_partner_class_of_service d_cos ON (children.class_of_service_id = d_cos.partner_class_of_service_id)
		LEFT OUTER JOIN kalturadw.dwh_dim_partner_vertical d_vertical ON (children.vertical_id = d_vertical.partner_vertical_id)
		WHERE parents.partner_group_type_id <> 3 OR parents.partner_group_type_id IS NULL;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_partner_usage_data`(p_date_id INT(11),p_partner_id INT,p_total BOOL)
BEGIN
    IF(p_total) THEN
    
	    SELECT 
		month_id,
	    SUM(free.avg_continuous_aggr_storage_mb) avg_continuous_aggr_storage_mb,
	    SUM(free.sum_partner_bandwidth_kb) sum_partner_bandwidth_kb
	    FROM 
	    (SELECT
		FLOOR(date_id/100) month_id,
		SUM(aggr_storage_mb/IF(FLOOR(date_id/100)=FLOOR(LEAST(p_date_id,DATE(NOW())*1)),DAY(LEAST(p_date_id,DATE(NOW())*1)),DAY(LAST_DAY(date_id)))) avg_continuous_aggr_storage_mb,
		SUM(count_bandwidth_kb) sum_partner_bandwidth_kb
	    FROM dwh_hourly_partner_usage 
	    WHERE partner_id=p_partner_id AND hour_id = 0
	    AND date_id <= LEAST(p_date_id,DATE(NOW())*1)
	    GROUP BY month_id) AS free;
     ELSE
	
	SELECT
		FLOOR(date_id/100) month_id,
		SUM(aggr_storage_mb)/DAY(LEAST(p_date_id,DATE(NOW())*1)) avg_continuous_aggr_storage_mb,
		SUM(count_bandwidth_kb) sum_partner_bandwidth_kb
	    FROM dwh_hourly_partner_usage 
	    WHERE partner_id=p_partner_id AND hour_id = 0
	    AND FLOOR(date_id/100) = FLOOR(LEAST(p_date_id,DATE(NOW())*1)/100);
     END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`etl`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_updated_batch_job`(p_start_date INT(11), p_end_date INT(11))
BEGIN
                                
                BEGIN
				
                                DECLARE v_date_id INT(11);
                                DECLARE done INT DEFAULT 0;
                                DECLARE days_to_update CURSOR FOR 
                                SELECT day_id FROM kalturadw.dwh_dim_time WHERE day_id BETWEEN p_start_date AND p_end_date;
                                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
                                
                                OPEN days_to_update;
								
                                read_loop: LOOP
                                                FETCH days_to_update INTO v_date_id;
                                                IF done THEN
                                                                LEAVE read_loop;
                                                END IF;
                                                CALL kalturadw.calc_updated_batch_job_day(v_date_id);
                                END LOOP;
                                CLOSE days_to_update;
                END;
				
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`etl`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`calc_updated_batch_job_day`(p_date_id INT(11))
BEGIN
                DECLARE v_date DATETIME;
                DECLARE v_ignore_partner_ids TEXT;
                SET v_ignore_partner_ids = '';
				
                
                SELECT IFNULL(GROUP_CONCAT(ignore_partner.partner_id),'')
				INTO v_ignore_partner_ids
				FROM 
				(SELECT partner_id FROM kalturadw.dwh_dim_batch_job_sep WHERE job_type_id = 0 AND job_sub_type_id IN (1,2,3,99) AND updated_date_id = p_date_id
				GROUP BY partner_id
				HAVING COUNT(*) > 1000) ignore_partner;
                                
                
                SET @s = CONCAT("INSERT INTO kalturadw.dwh_fact_convert_job(id, job_type_id, status_id, created_date_id, updated_date_id, finish_date_id, partner_id, entry_id, dc, wait_time, conversion_time, is_ff)
				SELECT id, job_type_id, status_id, created_date_id, updated_date_id, DATE(finish_time)*1, partner_id, entry_id, dc, time_to_sec(timediff(queue_time, created_at)) wait_time, IF(finish_time IS NULL, -1, time_to_sec(timediff(finish_time, queue_time))) conversion_time, 0
				FROM kalturadw.dwh_dim_batch_job_sep WHERE job_type_id = 0 AND job_sub_type_id IN (1,2,3,99) AND priority <> 10 AND queue_time IS NOT NULL AND updated_date_id = ", p_date_id, IF(LENGTH(v_ignore_partner_ids)=0,"",CONCAT(" AND partner_id NOT IN (" , v_ignore_partner_ids, ")")),
				" ON DUPLICATE KEY UPDATE 
					status_id = VALUES(status_id),
					updated_date_id = VALUES(updated_date_id),
					finish_date_id = VALUES(finish_date_id),
					wait_time = VALUES(wait_time),
					conversion_time = VALUES(conversion_time);");
					
				PREPARE stmt FROM  @s;
				EXECUTE stmt;
				DEALLOCATE PREPARE stmt;	
					
				SELECT IFNULL(GROUP_CONCAT(ignore_partner.partner_id),'')
				INTO v_ignore_partner_ids
				FROM 
				(SELECT partner_id FROM kalturadw.dwh_dim_batch_job_sep WHERE job_type_id = 10 AND updated_date_id = p_date_id
				GROUP BY partner_id
				HAVING COUNT(*) > 1000) ignore_partner;
			
		DROP TABLE IF EXISTS kalturadw.tmp_convert_job_ids;
			
		SET @s = CONCAT("CREATE TEMPORARY TABLE kalturadw.tmp_convert_job_ids AS SELECT id FROM kalturadw.dwh_dim_batch_job_sep WHERE job_type_id = 10 AND priority <> 10 AND updated_date_id = ", p_date_id,
		IF(LENGTH(v_ignore_partner_ids)=0,"",CONCAT(" AND partner_id NOT IN (" , v_ignore_partner_ids, ")")), ";");
		
		PREPARE stmt FROM  @s;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;	
				
                INSERT INTO kalturadw.dwh_fact_convert_job(id, job_type_id, status_id, created_date_id, updated_date_id, finish_date_id, partner_id, entry_id, dc, wait_time, conversion_time, is_ff)
                                SELECT id, job_type_id, status_id, created_date_id, updated_date_id, DATE(finish)*1, partner_id, c.entry_id, dc, TIME_TO_SEC(TIMEDIFF(queue_time, created_at)) wait_time, IF(finish IS NULL, -1, TIME_TO_SEC(TIMEDIFF(finish, queue_time))) conversion_time, 1 
				FROM (SELECT entry_id, root_job_id, MIN(finish_time) AS finish 
                FROM kalturadw.dwh_dim_batch_job_sep, tmp_convert_job_ids t WHERE root_job_id = t.id AND job_type_id = 0 AND job_sub_type_id IN (1,2,3,99) GROUP BY entry_id)
                AS c INNER JOIN kalturadw.dwh_dim_batch_job_sep batch_job ON c.root_job_id = batch_job.root_job_id AND c.finish =  batch_job.finish_time
                GROUP BY c.entry_id
				ON DUPLICATE KEY UPDATE 
					status_id = VALUES(status_id),
					updated_date_id = VALUES(updated_date_id),
					finish_date_id = VALUES(finish_date_id),
					wait_time = VALUES(wait_time),
					conversion_time = VALUES(conversion_time),
					is_ff = VALUES(is_ff);
                		
                                
                BEGIN
                                DECLARE v_created_date_id INT(11);
                                DECLARE done INT DEFAULT 0;
                                DECLARE days_to_aggregate CURSOR FOR 
                                SELECT DISTINCT(created_date_id) FROM kalturadw.dwh_fact_convert_job WHERE updated_date_id = p_date_id
                                AND MONTH(DATE(created_date_id) + INTERVAL 1 MONTH) >=  MONTH(DATE(p_date_id));
                                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
                                
                                OPEN days_to_aggregate;
								
                                read_loop: LOOP
                                                FETCH days_to_aggregate INTO v_created_date_id;
                                                IF done THEN
                                                                LEAVE read_loop;
                                                END IF;
                                                INSERT INTO kalturadw.aggr_managment(aggr_name,date_id,hour_id,data_insert_time) 
												VALUES ("ingestion", v_created_date_id, 0 ,NOW())
                                                ON DUPLICATE KEY UPDATE
                                                                data_insert_time = VALUES(data_insert_time);
                                END LOOP;
                                CLOSE days_to_aggregate;
                END;
				
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`do_tables_to_new`(p_greater_than_or_equal_date_id int, p_less_than_date_id int, p_table_name varchar(256))
BEGIN
	DECLARE v_copied int;
	declare v_column varchar(256);
	DECLARE select_fields VARCHAR(4000);


	SELECT is_copied, column_name
	INTO v_copied, v_column
	FROM kalturadw_ds.tables_to_new
	WHERE greater_than_or_equal_date_id = p_greater_than_or_equal_date_id AND 
	      	less_than_date_id = p_less_than_date_id AND 
		table_name = p_table_name;
	
	IF (v_copied=0) THEN
		
		SELECT GROUP_CONCAT(column_name) 
		INTO 	select_fields
		FROM (
			SELECT  column_name
	                FROM information_schema.COLUMNS
        	        WHERE CONCAT(table_schema,'.',table_name) IN (CONCAT('kalturadw.',p_table_name),CONCAT('kalturadw.',p_table_name,'_new'))
			 GROUP BY column_name
			 HAVING COUNT(*) > 1
			 ORDER BY MIN(ordinal_position)
		) COLUMNS;
		
		SET @s = CONCAT('insert into ',p_table_name,'_new (',select_fields,') ',
						' select ',select_fields,
						' from ',p_table_name,
						' where ',v_column,'  >= ',p_greater_than_or_equal_date_id, ' AND ', v_column, ' < ', p_less_than_date_id);
		PREPARE stmt FROM @s;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;

		UPDATE tables_to_new SET is_copied = 1 
		WHERE greater_than_or_equal_date_id = p_greater_than_or_equal_date_id AND
                less_than_date_id = p_less_than_date_id AND
                table_name = p_table_name;
	END IF;
	
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`generate_daily_usage_report`(p_date_val DATE)
BEGIN
	DECLARE yesterday_date_id INT(11);
	
	DECLARE the_day_before_yesteray_date_id INT(11);
	
	DECLARE 5_days_ago_date_id DATE;
	DECLARE 30_days_ago_date_id DATE;
	
	SET yesterday_date_id = (DATE(p_date_val) - INTERVAL 1 DAY)*1;
	
	SET the_day_before_yesteray_date_id = (DATE(p_date_val) - INTERVAL 2 DAY)*1;
	
	SET 5_days_ago_date_id = (DATE(p_date_val) - INTERVAL 5 DAY)*1;
	SET 30_days_ago_date_id = (DATE(p_date_val) - INTERVAL 30 DAY)*1;
	
	INSERT INTO kalturadw.dwh_daily_usage_reports (measure, classification, DATE, yesterday, the_day_before, diff, last_5_days_avg, last_30_days_avg, outer_order, inner_order)
	
	SELECT 	measure AS Measure, 
		classification AS Classification, 
		IF (measure = 'Bandwidth (MB)',DATE(p_date_val) - INTERVAL 3 DAY, DATE(p_date_val))  AS 'Report Date', 
		IFNULL(yesterday, 0) yesterday, 
		IFNULL(the_day_before, 0) the_day_before, 
		IF(IFNULL(the_day_before, 0) = 0, 0, IFNULL(yesterday, 2)/the_day_before*100 - 100) diff,
		IFNULL(last_5_days, 0) AS last_5_days_avg, 
		IFNULL(last_30_days, 0) AS last_30_days_avg,
		outer_order, inner_order FROM (
	
	SELECT * FROM(
	
	SELECT 'Content' measure, 
		t.caption classification, 
		yesterday, 
		the_day_before, 
		last_5_days, 
		last_30_days,
		1 outer_order,
		sort_order inner_order
	FROM
	(
		SELECT 	IF(entry_media_type_id NOT IN (1, 5, 2, 6), IF (entry_media_type_id IN (11,12,13), -99999, -1), entry_media_type_id) entry_media_type_id,
			SUM(IF (created_at BETWEEN DATE(yesterday_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0)) yesterday,
			SUM(IF (created_at BETWEEN DATE(the_day_before_yesteray_date_id) AND DATE(the_day_before_yesteray_date_id) + INTERVAL 1 DAY, 1, 0)) the_day_before,
			SUM(IF (created_at BETWEEN DATE(5_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0))/5 last_5_days,
			COUNT(*)/30 last_30_days			
			FROM kalturadw.dwh_dim_entries 
			WHERE created_at BETWEEN DATE(30_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY
			GROUP BY IF(entry_media_type_id NOT IN (1, 5, 2, 6), IF (entry_media_type_id IN (11,12,13), -99999, -1), entry_media_type_id)
	) e RIGHT OUTER JOIN 
	(
		SELECT 	entry_media_type_id, 
			CASE entry_media_type_name
				WHEN 'VIDEO' THEN 'Videos'
				WHEN 'AUDIO' THEN 'Audios'
				WHEN 'IMAGE' THEN 'Images'
				WHEN 'SHOW' THEN 'Mixs'
				WHEN 'PDF' THEN 'PDF'
				ELSE 'Other' END caption,
			CASE entry_media_type_name
				WHEN 'VIDEO' THEN 1
				WHEN 'AUDIO' THEN 2
				WHEN 'IMAGE' THEN 3
				WHEN 'SHOW' THEN 4
				WHEN 'PDF' THEN 5
				ELSE 6 END sort_order
		FROM (SELECT entry_media_type_id, entry_media_type_name FROM kalturadw.dwh_dim_entry_media_type UNION SELECT -99999, 'PDF') entry_media_type
		WHERE entry_media_type_id IN (1, 5, 2, 6, -99999, -1)
	) t
	ON e.entry_media_type_id = t.entry_media_type_id
	) Content	
	UNION
	
	SELECT * FROM ( 
	SELECT 	'Deleted' measure, 
		'Entries' Classification, 
		SUM(IF (modified_at BETWEEN DATE(yesterday_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0)) yesterday,
		SUM(IF (modified_at BETWEEN DATE(the_day_before_yesteray_date_id) AND DATE(the_day_before_yesteray_date_id) + INTERVAL 1 DAY, 1, 0)) the_day_before,
		SUM(IF (modified_at BETWEEN DATE(5_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0))/5 last_5_days,
		COUNT(*)/30 last_30_days, 2 outer_order, 1 inner_order
		FROM kalturadw.dwh_dim_entries 
		WHERE modified_at BETWEEN DATE(30_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY
		AND entry_status_id = 3) deleted_entries
	UNION
	
	SELECT * FROM (
	SELECT 'Upload' measure, 
		caption classification, 
		yesterday, 
		the_day_before, 
		last_5_days, 
		last_30_days, 3 outer_order, sort_order inner_order 
		FROM 
		(
			SELECT IF (entry_status_id = 2, 0, IF (entry_status_id IN (-2, -1, 0, 1, 4), 1, NULL)) entry_status_id,
			SUM(IF (created_at BETWEEN DATE(yesterday_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0)) yesterday,
			SUM(IF (created_at BETWEEN DATE(the_day_before_yesteray_date_id) AND DATE(the_day_before_yesteray_date_id) + INTERVAL 1 DAY, 1, 0)) the_day_before,
			SUM(IF (created_at BETWEEN DATE(5_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0))/5 last_5_days,
			COUNT(*)/30 last_30_days
			FROM kalturadw.dwh_dim_entries
			WHERE created_at BETWEEN DATE(30_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY
			AND entry_media_source_id = 1
			GROUP BY IF (entry_status_id = 2, 0, IF (entry_status_id IN (-2, -1, 0, 1, 4), 1, NULL))
		) e
		RIGHT OUTER JOIN 
		(
			SELECT 0 id, 'Ready' caption, 1 sort_order
			UNION 
			SELECT 1 id, 'Failed' caption, 2 sort_order
		) s
		ON e.entry_status_id = s.id) uploaded_entries
	
	UNION
	
	SELECT * FROM (SELECT 'Web Cam' measure, 
		caption classification, 
		yesterday, 
		the_day_before, 
		last_5_days, 
		last_30_days, 4 outer_order, sort_order inner_order FROM 
		(
			SELECT IF (entry_status_id = 2, 0, IF (entry_status_id IN (-2, -1, 0, 1, 4), 1, NULL)) entry_status_id,
			SUM(IF (created_at BETWEEN DATE(yesterday_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0)) yesterday,
			SUM(IF (created_at BETWEEN DATE(the_day_before_yesteray_date_id) AND DATE(the_day_before_yesteray_date_id) + INTERVAL 1 DAY, 1, 0)) the_day_before,
			SUM(IF (created_at BETWEEN DATE(5_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0))/5 last_5_days,
			COUNT(*)/30 last_30_days
			FROM kalturadw.dwh_dim_entries
			WHERE created_at BETWEEN DATE(30_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY
			AND entry_media_source_id = 2
			GROUP BY IF (entry_status_id = 2, 0, IF (entry_status_id IN (-2, -1, 0, 1, 4), 1, NULL))
		) e
		RIGHT OUTER JOIN 
		(
			SELECT 0 id, 'Ready' caption, 1 sort_order
			UNION 
			SELECT 1 id, 'Failed' caption, 2 sort_order
		) s
		ON e.entry_status_id = s.id) web_cam
	
	UNION
	
	SELECT * FROM (SELECT 'Import' measure, 
		caption classification, 
		yesterday, 
		the_day_before, 
		last_5_days, 
		last_30_days, 5 outer_order, sort_order inner_order FROM 
		(
			SELECT IF (entry_status_id = 2, 0, IF (entry_status_id IN (-2, -1, 0, 1, 4), 1, NULL)) entry_status_id,
			SUM(IF (created_at BETWEEN DATE(yesterday_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0)) yesterday,
			SUM(IF (created_at BETWEEN DATE(the_day_before_yesteray_date_id) AND DATE(the_day_before_yesteray_date_id) + INTERVAL 1 DAY, 1, 0)) the_day_before,
			SUM(IF (created_at BETWEEN DATE(5_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0))/5 last_5_days,
			COUNT(*)/30 last_30_days
			FROM kalturadw.dwh_dim_entries
			WHERE created_at BETWEEN DATE(30_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY
			AND entry_media_source_id NOT IN (1, 2)
			GROUP BY IF (entry_status_id = 2, 0, IF (entry_status_id IN (-2, -1, 0, 1, 4), 1, NULL))
		) e
		RIGHT OUTER JOIN 
		(
			SELECT 0 id, 'Ready' caption, 1 sort_order
			UNION 
			SELECT 1 id, 'Failed' caption, 2 sort_order
		) s
		ON e.entry_status_id = s.id) imported_entries
	
	UNION
	
	SELECT * FROM (SELECT 'Conversion' measure, 
		caption classification, 
		yesterday, 
		the_day_before, 
		last_5_days, 
		last_30_days, 6 outer_order, sort_order inner_order  FROM 
		(
			SELECT IF (entry_status_id = 2, 0, IF (entry_status_id IN (-2, -1, 0, 1, 4), 1, NULL)) entry_status_id,
			SUM(IF (created_at BETWEEN DATE(yesterday_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0)) yesterday,
			SUM(IF (created_at BETWEEN DATE(the_day_before_yesteray_date_id) AND DATE(the_day_before_yesteray_date_id) + INTERVAL 1 DAY, 1, 0)) the_day_before,
			SUM(IF (created_at BETWEEN DATE(5_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0))/5 last_5_days,
			COUNT(*)/30 last_30_days
			FROM kalturadw.dwh_dim_entries
			WHERE created_at BETWEEN DATE(30_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY
			GROUP BY IF (entry_status_id = 2, 0, IF (entry_status_id IN (-2, -1, 0, 1, 4), 1, NULL))
		) e
		RIGHT OUTER JOIN 
		(
			SELECT 0 id, 'Ready' caption, 1 sort_order
			UNION 
			SELECT 1 id, 'Failed' caption, 2 sort_order
		) s
		ON e.entry_status_id = s.id) conversions
	UNION
	
	SELECT * FROM ( 
	SELECT 	'Storage MB' measure, 
		'Additional daily' Classification, 
		SUM(IF (date_id BETWEEN yesterday_date_id AND yesterday_date_id, count_storage, 0)) yesterday,
		SUM(IF (date_id BETWEEN the_day_before_yesteray_date_id AND the_day_before_yesteray_date_id, count_storage, 0)) the_day_before,
		SUM(IF (date_id BETWEEN 5_days_ago_date_id AND yesterday_date_id, count_storage, 0))/5 last_5_days,
		SUM(count_storage)/30 last_30_days,
		7 outer_order, 1 inner_order
		FROM kalturadw.dwh_aggr_partner 
		WHERE date_id BETWEEN 30_days_ago_date_id AND yesterday_date_id) STORAGE
	
	UNION 
	
	SELECT * FROM ( 
	SELECT 'Playback' Measure, 
		classification, 
		yesterday, the_day_before, last_5_days, last_30_days,
		8 outer_order, sort_order inner_order
	FROM (
		SELECT 'Playback' classification, 
		SUM(IF (date_id BETWEEN yesterday_date_id AND yesterday_date_id, count_plays, 0)) yesterday,
		SUM(IF (date_id BETWEEN the_day_before_yesteray_date_id AND the_day_before_yesteray_date_id, count_plays, 0)) the_day_before,
		SUM(IF (date_id BETWEEN 5_days_ago_date_id AND yesterday_date_id, count_plays, 0))/5 last_5_days,
		SUM(count_plays)/30 last_30_days, 1 sort_order
		FROM kalturadw.dwh_aggr_events_entry
		WHERE date_id BETWEEN 30_days_ago_date_id AND yesterday_date_id
		
		UNION
		SELECT '25%' classification,
		SUM(IF (date_id BETWEEN yesterday_date_id AND yesterday_date_id, count_plays_25, 0)) yesterday,
		SUM(IF (date_id BETWEEN the_day_before_yesteray_date_id AND the_day_before_yesteray_date_id, count_plays_25, 0)) the_day_before,
		SUM(IF (date_id BETWEEN 5_days_ago_date_id AND yesterday_date_id, count_plays_25, 0))/5 last_5_days,
		SUM(count_plays_25)/30 last_30_days, 2 sort_order
		FROM kalturadw.dwh_aggr_events_entry
		WHERE date_id BETWEEN 30_days_ago_date_id AND yesterday_date_id
		UNION 
		SELECT '50%' classification,
		SUM(IF (date_id BETWEEN yesterday_date_id AND yesterday_date_id, count_plays_50, 0)) yesterday,
		SUM(IF (date_id BETWEEN the_day_before_yesteray_date_id AND the_day_before_yesteray_date_id, count_plays_50, 0)) the_day_before,
		SUM(IF (date_id BETWEEN 5_days_ago_date_id AND yesterday_date_id, count_plays_50, 0))/5 last_5_days,
		SUM(count_plays_50)/30 last_30_days, 3 sort_order
		FROM kalturadw.dwh_aggr_events_entry
		WHERE date_id BETWEEN 30_days_ago_date_id AND yesterday_date_id
	
		UNION 
	
		SELECT '75%' classification,
		SUM(IF (date_id BETWEEN yesterday_date_id AND yesterday_date_id, count_plays_75, 0)) yesterday,
		SUM(IF (date_id BETWEEN the_day_before_yesteray_date_id AND the_day_before_yesteray_date_id, count_plays_75, 0)) the_day_before,
		SUM(IF (date_id BETWEEN 5_days_ago_date_id AND yesterday_date_id, count_plays_75, 0))/5 last_5_days,
		SUM(count_plays_75)/30 last_30_days, 4 sort_order
		FROM kalturadw.dwh_aggr_events_entry
		WHERE date_id BETWEEN 30_days_ago_date_id AND yesterday_date_id
		UNION 
		SELECT '100%' classification,
		SUM(IF (date_id BETWEEN yesterday_date_id AND yesterday_date_id, count_plays_100, 0)) yesterday,
		SUM(IF (date_id BETWEEN the_day_before_yesteray_date_id AND the_day_before_yesteray_date_id, count_plays_100, 0)) the_day_before,
		SUM(IF (date_id BETWEEN 5_days_ago_date_id AND yesterday_date_id, count_plays_100, 0))/5 last_5_days,
		SUM(count_plays_100)/30 last_30_days, 5 sort_order
		FROM kalturadw.dwh_aggr_events_entry
		WHERE date_id BETWEEN 30_days_ago_date_id AND yesterday_date_id
	) playback ) playback
	
	UNION
	SELECT * FROM ( 
	SELECT 'Registrations' measure, t.caption classification, 
		yesterday, 
		the_day_before, 
		last_5_days, 
		last_30_days, 9 outer_order, sort_order inner_order 
	FROM
	(
		SELECT 	IF(partner_type_id NOT IN (1, 102, 101, 104, 106, 103), 2, partner_type_id) partner_type_id,
			SUM(IF (created_at BETWEEN DATE(yesterday_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0)) yesterday,
			SUM(IF (created_at BETWEEN DATE(the_day_before_yesteray_date_id) AND DATE(the_day_before_yesteray_date_id) + INTERVAL 1 DAY, 1, 0)) the_day_before,
			SUM(IF (created_at BETWEEN DATE(5_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY, 1, 0))/5 last_5_days,
			COUNT(*)/30 last_30_days
		FROM kalturadw.dwh_dim_partners
		WHERE created_at BETWEEN DATE(30_days_ago_date_id) AND DATE(yesterday_date_id) + INTERVAL 1 DAY
		GROUP BY IF(partner_type_id NOT IN (1, 102, 101, 104, 106, 103), 2, partner_type_id)
	) p
	RIGHT OUTER JOIN 
	(
		SELECT partner_type_id, 
		CASE partner_type_name
			WHEN 'KMC_SIGNUP' THEN 'Kaltura'
			WHEN 'DRUPAL' THEN 'Drupal'
			WHEN 'WORDPRESS' THEN 'WordPress'
			WHEN 'MODDLE' THEN 'Moodle'
			WHEN 'JOOMLA ' THEN 'Joomla'
			WHEN 'MIND_TOUCH' THEN 'MindTouch'
			ELSE 'Other' 
		END caption,
		CASE partner_type_name
			WHEN 'KMC_SIGNUP' THEN 1
			WHEN 'DRUPAL' THEN 2
			WHEN 'WORDPRESS' THEN 3
			WHEN 'MOODLE' THEN 4
			WHEN 'JOOMLA ' THEN 5
			WHEN 'MIND_TOUCH' THEN 6
			ELSE 7 
		END sort_order, 
		partner_type_name
		FROM kalturadw.dwh_dim_partner_type WHERE partner_type_id NOT IN (0,-1, 105, 100)
	) t
	ON (p.partner_type_id = t.partner_type_id)) Registrations
	
	
	UNION
	SELECT * FROM ( 
	SELECT 	'Bandwidth (MB)' measure, 
		caption classification, 
		yesterday,
		the_day_before,
		last_5_days,
		last_30_days, 10 outer_order, sort_order inner_order 
		FROM 
		(
			SELECT partner_sub_activity_id,
			SUM(IF (activity_date_id BETWEEN (DATE(yesterday_date_id) - INTERVAL 3 DAY)*1 AND (DATE(yesterday_date_id) - INTERVAL 3 DAY)*1 , amount, 0))/1024 yesterday,
			SUM(IF (activity_date_id BETWEEN (DATE(the_day_before_yesteray_date_id) - INTERVAL 3 DAY)*1 AND (DATE(the_day_before_yesteray_date_id) - INTERVAL 3 DAY)*1 , amount, 0))/1024 the_day_before,
			SUM(IF (activity_date_id BETWEEN (DATE(5_days_ago_date_id) - INTERVAL 3 DAY)*1 AND (DATE(yesterday_date_id) - INTERVAL 3 DAY)*1 , amount, 0))/5/1024 last_5_days,
			SUM(amount)/30/1024 last_30_days
			FROM kalturadw.dwh_fact_partner_activities 
			WHERE partner_activity_id = 1 AND activity_date_id BETWEEN (DATE(30_days_ago_date_id) - INTERVAL 3 DAY)*1 AND (DATE(yesterday_date_id) - INTERVAL 3 DAY)*1 
			GROUP BY partner_sub_activity_id
		) bandwidth 
		RIGHT OUTER JOIN
		(
			SELECT 1 id, 'www.kaltura.com' caption, 4 sort_order
			UNION 
			SELECT 2 id, 'Limelight' caption, 2 sort_order
			UNION 
			SELECT 3 id, 'Level3' caption, 3 sort_order
			UNION 
			SELECT 4 id, 'Akamai' caption, 1 sort_order
		) filler
		ON (bandwidth.partner_sub_activity_id = filler.id)) Bandwidth) all_tables
		ON DUPLICATE KEY UPDATE 
			yesterday = VALUES(yesterday), 
			the_day_before = VALUES(the_day_before), 
			diff = VALUES(diff), 
			last_5_days_avg = VALUES(last_5_days_avg), 
			last_30_days_avg = VALUES(last_30_days_avg),
			outer_order = VALUES(outer_order),
			inner_order = VALUES(inner_order);
		
		SELECT 	measure AS Measure, 
		classification AS Classification, 
		DATE AS 'Report Date', 
		FORMAT(yesterday, 2) AS 'Yesterday', 
		FORMAT(the_day_before, 2) AS 'Day Before Yesterday', 
		CONCAT(diff, '%') AS 'Diff',
		FORMAT(last_5_days_avg, 2) AS 'Last 5 Days (AVG)', 
		FORMAT(last_30_days_avg, 2) AS 'Last 30 Days (AVG)'
		FROM kalturadw.dwh_daily_usage_reports
		WHERE DATE = IF (measure = 'Bandwidth (MB)',DATE(p_date_val) - INTERVAL 3 DAY, DATE(p_date_val))
		ORDER BY outer_order, inner_order;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`get_data_for_operational`(p_sync_type VARCHAR(55))
BEGIN
	DECLARE v_execution_start_time DATETIME;
	
	DECLARE v_group_column VARCHAR(1024);
	DECLARE v_entity_table VARCHAR(1024);
	DECLARE v_aggregation_phrase VARCHAR(1024);
	DECLARE v_aggregation_table VARCHAR(1024);
	DECLARE v_bridge_entity VARCHAR(1024);
	DECLARE v_bridge_table VARCHAR(1024);
	DECLARE v_last_execution_parameter_id INT;
	DECLARE v_execution_start_time_parameter_id INT;
	
	SET v_execution_start_time = NOW();
   
    UPDATE kalturadw_ds.parameters	
    SET date_value = v_execution_start_time 
    WHERE id = v_execution_start_time_parameter_id;

    IF p_sync_type='entry' THEN 
    
        SELECT e.entry_id, e.plays, e.views
        FROM dwh_entry_plays_views e, kalturadw_ds.parameters p
        WHERE e.updated_at > p.date_value AND p.id = 4;
    
    ELSE
    
        SELECT group_column, entity_table, aggregation_phrase, aggregation_table, 
            bridge_entity, bridge_table, last_execution_parameter_id, execution_start_time_parameter_id
        INTO	v_group_column, v_entity_table, v_aggregation_phrase, v_aggregation_table, 
            v_bridge_entity, v_bridge_table, v_last_execution_parameter_id, v_execution_start_time_parameter_id
        FROM kalturadw_ds.operational_syncs WHERE operational_sync_name = p_sync_type;

        UPDATE kalturadw_ds.parameters	SET date_value = v_execution_start_time WHERE id = v_execution_start_time_parameter_id;

        SET @s = CONCAT('SELECT dim.', v_group_column,', ', v_aggregation_phrase, 
                ' FROM ', v_aggregation_table ,' aggr, ', IF (v_bridge_table IS NULL, '', CONCAT(v_bridge_table, ' bridge, ')), v_entity_table, ' dim, kalturadw_ds.parameters p',
                ' WHERE aggr.', IF(v_bridge_entity IS NULL, v_group_column, 
                            CONCAT(v_bridge_entity, ' = bridge.',v_bridge_entity, ' AND bridge.', v_group_column)), 
                ' = dim.', v_group_column, ' AND dim.operational_measures_updated_at > p.date_value AND p.id = ', v_last_execution_parameter_id,
                ' GROUP BY dim.',v_group_column);
        
        PREPARE stmt FROM  @s;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`mark_operational_sync_as_done`(p_sync_type VARCHAR(55))
BEGIN
	DECLARE v_last_execution_parameter_id INT;
	DECLARE v_execution_start_time_parameter_id INT;
	
	SELECT last_execution_parameter_id, execution_start_time_parameter_id
	INTO	v_last_execution_parameter_id, v_execution_start_time_parameter_id
	FROM kalturadw_ds.operational_syncs WHERE operational_sync_name = p_sync_type;

	UPDATE kalturadw_ds.parameters main, kalturadw_ds.parameters start_time	
	SET main.date_value = start_time.date_value
	WHERE main.id = v_last_execution_parameter_id AND start_time.id = v_execution_start_time_parameter_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`move_innodb_to_archive`()
BEGIN
	DECLARE v_table_name VARCHAR(256);
	DECLARE v_archive_name VARCHAR(256);	
	DECLARE v_partition_name VARCHAR(256);
	DECLARE v_partition_date_id INT;
	DECLARE v_column VARCHAR(256);
	DECLARE v_is_archived INT;
	DECLARE v_is_in_fact INT;
	
	DECLARE v_drop_from_archive INT DEFAULT 0;
	DECLARE v_drop_from_fact INT DEFAULT 0;
	DECLARE v_migrate_from_fact INT DEFAULT 0;
		
	DECLARE v_done INT DEFAULT 0;
	
	DECLARE c_partitions 
	CURSOR FOR 	
	SELECT 	r.table_name, 
		CONCAT(r.table_name, '_archive') archive_name,
		partition_name, 
		DATE(partition_description)*1 partition_date_id, 
		partition_expression column_name,
		MAX(IF(CONCAT(r.table_name, '_archive') = p.table_name,1,0)) is_archived, 
		MAX(IF(r.table_name=p.table_name,1,0)) is_in_fact
	FROM information_schema.PARTITIONS p, kalturadw_ds.retention_policy r
	WHERE LENGTH(partition_description) = 8 
	AND DATE(partition_description)*1 IS NOT NULL
	AND (p.table_name = r.table_name OR CONCAT(r.table_name, '_archive') = p.table_name)
	GROUP BY r.table_name, partition_name, partition_date_id, column_name
	ORDER BY partition_date_id;
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;
	
	OPEN c_partitions;
	
	read_loop: LOOP
		FETCH c_partitions INTO v_table_name, v_archive_name, v_partition_name, v_partition_date_id, v_column, v_is_archived, v_is_in_fact;

		IF v_done = 1 THEN
		  LEAVE read_loop;
		END IF;

		SET v_drop_from_archive = 0;
		SET v_drop_from_fact = 0;
		SET v_migrate_from_fact = 0;

		
		SELECT if(count(*)=0,0,v_is_archived), if(count(*)=0, 0,v_is_in_fact)
		INTO v_drop_from_archive, v_drop_from_fact
		FROM kalturadw_ds.retention_policy
		WHERE DATE(NOW() - INTERVAL archive_delete_days_back DAY)*1 >= v_partition_date_id
		AND table_name = v_table_name;

		IF (v_drop_from_archive > 0) THEN 
			SET @s = CONCAT('ALTER TABLE ',v_archive_name,' DROP PARTITION ', v_partition_name);
			
			PREPARE stmt FROM @s;
                        EXECUTE stmt;
                        DEALLOCATE PREPARE stmt;
		END IF;

		
		SELECT if(count(*)=0,0, v_is_in_fact)
		INTO v_migrate_from_fact
		FROM kalturadw_ds.retention_policy
		WHERE DATE(NOW() - INTERVAL archive_start_days_back DAY)*1 >= v_partition_date_id
		AND table_name = v_table_name
		AND v_is_in_fact > 0;
		
		
		IF (v_migrate_from_fact > 0 AND v_drop_from_fact = 0) THEN
			
			IF (v_is_archived > 0) THEN
				SET @s = CONCAT('ALTER TABLE ',v_archive_name,' DROP PARTITION ', v_partition_name);
		
				PREPARE stmt FROM @s;
				EXECUTE stmt;
				DEALLOCATE PREPARE stmt;
			END IF;
			
			
			SET @s = CONCAT('ALTER TABLE ',v_archive_name,' ADD PARTITION (PARTITION ',v_partition_name,' VALUES LESS THAN (',v_partition_date_id,'))');
			
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
			
			SET @s = CONCAT('INSERT INTO ',v_archive_name,' SELECT * FROM ',v_table_name,' WHERE ', v_column ,' < ',v_partition_date_id);
			
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
			
			UPDATE kalturadw_ds.retention_policy
			SET archive_last_partition = DATE(v_partition_date_id)
			WHERE table_name = v_table_name;

			SET v_drop_from_fact = 1;
		END IF;

		
		IF (v_drop_from_fact > 0) THEN
			SET @s = CONCAT('ALTER TABLE ',v_table_name,' DROP PARTITION ',v_partition_name);
			
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		END IF;
	END LOOP read_loop;

	CLOSE c_partitions;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`populate_time_dim`(start_date datetime, end_date datetime)
    DETERMINISTIC
BEGIN    

    WHILE start_date <= end_date DO
	INSERT INTO kalturadw.dwh_dim_time 
	(day_id, date_field, datetime_field, day_eng_name, YEAR, month_str, month_id, month_eng_name, MONTH, day_of_year, day_of_month, 
	day_of_week, week_id, week_of_year, week_eng_name, day_of_week_desc, day_of_week_short_desc, month_desc, month_short_desc, 
	QUARTER, quarter_id, quarter_eng_name)
	SELECT 1*DATE(d), d, d, DATE_FORMAT(d, '%b %e, %Y'), YEAR(d), DATE_FORMAT(d, '%Y-%m'), DATE_FORMAT(d, '%Y%m')*1, DATE_FORMAT(d, '%b-%y'), MONTH(d), DAYOFYEAR(d),DAYOFMONTH(d),
	DAYOFWEEK(d), DATE_FORMAT(d, '%Y%U')*1, WEEK(d), DATE_FORMAT(d, 'Week %U, %Y'), DAYNAME(d),DATE_FORMAT(d,'%a'),MONTHNAME(d), DATE_FORMAT(d, '%b'), 
	QUARTER(d), YEAR(d)*10+QUARTER(d), CONCAT('Quarter ', QUARTER(d), ',', YEAR(d))
        FROM(SELECT start_date d) a;
        
        SET start_date = DATE_ADD(start_date, INTERVAL 1 DAY);
    END WHILE;
    
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`post_aggregation_entry`(date_val DATE, p_hour_id INT(11))
BEGIN
	CALL add_plays_views(date_val*1, p_hour_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`post_aggregation_live_entry`(date_val DATE, p_hour_id INT(11))
BEGIN
        CALL add_live_plays_views(date_val*1, p_hour_id);

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`post_aggregation_partner`(date_val DATE, p_hour_id INT(11))
BEGIN
	DECLARE v_aggr_table VARCHAR(100);
	
	SELECT aggr_table INTO v_aggr_table
	FROM kalturadw_ds.aggr_name_resolver
	WHERE aggr_name = 'partner';
	
	SET @s = CONCAT('INSERT INTO ',v_aggr_table,'
    		(partner_id, 
    		date_id, 
		hour_id,
		new_videos,
		new_images,
		new_audios,
		new_livestreams,
		new_playlists,
		new_documents,
		new_other_entries)
    		SELECT partner_id,DATE(''',date_val,''')*1 date_id, ', p_hour_id, ' hour_id,
    			SUM(IF(entry_type_id = 1 AND entry_media_type_id = 1, 1,0)) new_videos,
    			SUM(IF(entry_type_id = 1 AND entry_media_type_id = 2, 1,0)) new_images,
    			SUM(IF(entry_type_id = 1 AND entry_media_type_id = 5, 1,0)) new_audios,
			SUM(IF(entry_type_id = 7, 1,0)) new_livestreams,
			SUM(IF(entry_type_id = 5, 1,0)) new_playlists,
			SUM(IF(entry_type_id = 10, 1,0)) new_documents,
			SUM(IF(entry_type_id NOT IN (1,5,7,10) or (entry_type_id = 1 and entry_media_type_id NOT IN (1,2,5)), 1, 0)) new_other_entries
    		FROM dwh_dim_entries  en 
    		WHERE en.created_at between DATE(''',date_val,''') + INTERVAL ', p_hour_id, ' HOUR ',' 
					   AND DATE(''',date_val,''') + INTERVAL ', p_hour_id, ' + 1 HOUR - INTERVAL 1 SECOND ','
    	
		GROUP BY partner_id
    	ON DUPLICATE KEY UPDATE
    		new_videos=VALUES(new_videos),
		new_images=VALUES(new_images),
		new_audios=VALUES(new_audios),
		new_livestreams=VALUES(new_livestreams),
		new_playlists=VALUES(new_playlists),
		new_documents=VALUES(new_documents),
		new_other_entries=VALUES(new_other_entries);
    	');
	
 
	PREPARE stmt FROM  @s;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	
	SET @s = CONCAT('INSERT INTO ',v_aggr_table,'
    		(partner_id, 
    		 date_id, 
		 hour_id,
		 deleted_audios,
		 deleted_images,
		 deleted_videos,
		 deleted_documents,
		 deleted_livestreams,
		 deleted_playlists,
		 deleted_other_entries)
		SELECT  partner_id,DATE(''',date_val,''')*1 date_id, ', p_hour_id, ' hour_id,
			SUM(IF(entry_type_id = 1 AND entry_media_type_id = 1, 1,0)) deleted_videos,
			SUM(IF(entry_type_id = 1 AND entry_media_type_id = 2, 1,0)) deleted_images,
			SUM(IF(entry_type_id = 1 AND entry_media_type_id = 5, 1,0)) deleted_audios,
			SUM(IF(entry_type_id = 7, 1,0)) deleted_livestreams,
			SUM(IF(entry_type_id = 5, 1,0)) deleted_playlists,
			SUM(IF(entry_type_id = 10, 1,0)) deleted_documents,
			SUM(IF(entry_type_id NOT IN (1,5,7,10) or (entry_type_id = 1 and entry_media_type_id NOT IN (1,2,5)), 1, 0)) deleted_other_entries
		FROM 	dwh_dim_entries  en 
    		WHERE 	entry_status_id = 3
    			AND en.modified_at between DATE(''',date_val,''') + INTERVAL ', p_hour_id, ' HOUR ',' 
					   AND DATE(''',date_val,''') + INTERVAL ', p_hour_id, ' + 1 HOUR - INTERVAL 1 SECOND ','
    		GROUP BY partner_id
		ON DUPLICATE KEY UPDATE
			deleted_videos=VALUES(deleted_videos),
			deleted_images=VALUES(deleted_images),
			deleted_audios=VALUES(deleted_audios),
			deleted_livestreams=VALUES(deleted_livestreams),
			deleted_playlists=VALUES(deleted_playlists),
			deleted_documents=VALUES(deleted_documents),
			deleted_other_entries=VALUES(deleted_other_entries);
    	');

	PREPARE stmt FROM  @s;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
	
	SET @s = CONCAT('
    	INSERT INTO ',v_aggr_table,'
    		(partner_id, 
    		 date_id, 
		 hour_id,
    		 new_admins)
    	SELECT  partner_id, DATE(''',date_val,''')*1 date_id, ', p_hour_id, ' hour_id, count(*) new_admins
    	FROM dwh_dim_kusers  ku
    	WHERE ku.created_at between DATE(''',date_val,''') + INTERVAL ', p_hour_id, ' HOUR ',' 
					   AND DATE(''',date_val,''') + INTERVAL ', p_hour_id, ' + 1 HOUR - INTERVAL 1 SECOND ','
		and is_admin = 1
   		GROUP BY partner_id
    	ON DUPLICATE KEY UPDATE
		new_admins=VALUES(new_admins) ;
        ');
	
	PREPARE stmt FROM  @s;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`post_aggregation_widget`(date_val DATE, p_hour_id INT(11))
BEGIN
	DECLARE v_aggr_table VARCHAR(100);
    SELECT aggr_table INTO  v_aggr_table
	FROM kalturadw_ds.aggr_name_resolver
	WHERE aggr_name = 'widget';
	
	SET @s = CONCAT('
    	INSERT INTO ',v_aggr_table,'
    		(partner_id, 
    		date_id, 
		hour_id,
		widget_id,
     		count_widget_loads)
    	SELECT  partner_id,event_date_id,HOUR(event_time),widget_id,
    		SUM(IF(event_type_id=1,1,NULL)) count_widget_loads
		FROM dwh_fact_events  ev
		WHERE event_type_id = 1 AND event_date_id = DATE(''',date_val,''')*1 and event_hour_id = ', p_hour_id, '
		GROUP BY partner_id, event_date_id, event_hour_id, widget_id
		ON DUPLICATE KEY UPDATE
    		count_widget_loads=VALUES(count_widget_loads);
    	');
	PREPARE stmt FROM  @s;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`pre_aggregation_entry`(date_val DATE, p_hour_id INT(11))
BEGIN
	CALL remove_plays_views(date_val*1, p_hour_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`pre_aggregation_live_entry`(date_val DATE, p_hour_id INT(11))
BEGIN
        CALL remove_live_plays_views(date_val*1, p_hour_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`remove_live_plays_views`(p_date_id INT, p_hour_id INT)
BEGIN
  DECLARE v_done INT DEFAULT FALSE;
  DECLARE v_entry_id VARCHAR(20);
  DECLARE v_plays INT;
  DECLARE v_views INT;

  DECLARE entries CURSOR FOR SELECT entry_id, count_plays, count_loads FROM kalturadw.dwh_hourly_events_live_entry WHERE date_id = p_date_id AND hour_id = p_hour_id;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

  OPEN entries;

  read_loop: LOOP
    FETCH entries INTO v_entry_id, v_plays, v_views;

    IF v_done THEN
      LEAVE read_loop;
    END IF;

    UPDATE dwh_entry_plays_views
        SET plays =
                IF((IFNULL(plays, 0) - IFNULL(v_plays, 0))<0,
                        0,
                        IFNULL(plays, 0) - IFNULL(v_plays, 0)),
            views =
                IF((IFNULL(views, 0) - IFNULL(v_views, 0))<0,
                        0,
                        IFNULL(views, 0) - IFNULL(v_views, 0))
        WHERE v_entry_id = entry_id;

  END LOOP;

  CLOSE entries;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw`.`remove_plays_views`(p_date_id INT, p_hour_id INT)
BEGIN
  DECLARE v_done INT DEFAULT FALSE;
  DECLARE v_entry_id VARCHAR(20);
  DECLARE v_plays INT;
  DECLARE v_views INT;
  
  DECLARE entries CURSOR FOR SELECT entry_id, count_plays, count_loads FROM dwh_hourly_events_entry WHERE date_id = p_date_id AND hour_id = p_hour_id;
  
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

  OPEN entries;
  
  read_loop: LOOP
    FETCH entries INTO v_entry_id, v_plays, v_views;
     
    IF v_done THEN
      LEAVE read_loop;
    END IF;
    
    UPDATE dwh_entry_plays_views
	SET plays = 
		IF((IFNULL(plays, 0) - IFNULL(v_plays, 0))<0, 
			0, 
			IFNULL(plays, 0) - IFNULL(v_plays, 0)),
	    views = 
		IF((IFNULL(views, 0) - IFNULL(v_views, 0))<0, 
			0, 
			IFNULL(views, 0) - IFNULL(v_views, 0))
	WHERE v_entry_id = entry_id;	

  END LOOP;

  CLOSE entries;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-10-27  9:00:10
