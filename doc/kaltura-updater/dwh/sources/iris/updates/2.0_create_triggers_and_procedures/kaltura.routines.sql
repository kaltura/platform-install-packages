USE `kaltura`;
-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: kaltura
-- ------------------------------------------------------
-- Server version	5.1.73
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'kaltura'
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kaltura`.`update_entries`()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE entry_id CHAR(50);
    DECLARE new_views, new_plays INT;
    DECLARE updated_entries CURSOR FOR SELECT id, plays, views FROM temp_entry_update;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    OPEN updated_entries;
    
    SET SESSION sql_log_bin = 1;
    REPEAT
    FETCH updated_entries INTO entry_id, new_plays, new_views;
    UPDATE entry SET entry.plays = new_plays, entry.views = new_views WHERE entry.id = entry_id;
    UNTIL done END REPEAT;
    SET SESSION sql_log_bin = 0;
    CLOSE updated_entries;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kaltura`.`update_kusers`()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE new_kuser_id CHAR(50);
    DECLARE new_storage_size INT;
    DECLARE updated_kusers CURSOR FOR SELECT kuser_id, storage_kb FROM kaltura.temp_updated_kusers_storage_usage;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    OPEN updated_kusers;
    
    SET SESSION sql_log_bin = 1;
    REPEAT
    FETCH updated_kusers INTO new_kuser_id, new_storage_size;
    UPDATE kuser SET kuser.storage_size = new_storage_size WHERE kuser.id = new_kuser_id;
    UNTIL done END REPEAT;
    SET SESSION sql_log_bin = 0;
    CLOSE updated_kusers;
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

-- Dump completed on 2014-10-27  8:59:59
