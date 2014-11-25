USE `kalturadw_ds`;
-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: kalturadw_ds
-- ------------------------------------------------------
-- Server version	5.1.73
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'kalturadw_ds'
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `kalturadw_ds`.`get_error_code`(error_code_reason_param varchar(255)) RETURNS smallint(6)
    NO SQL
BEGIN
	DECLARE error_code smallint(6);
	INSERT IGNORE kalturadw_ds.invalid_ds_lines_error_codes (error_code_reason) VALUES(error_code_reason_param);
	SELECT error_code_id 
		INTO error_code
		FROM kalturadw_ds.invalid_ds_lines_error_codes
		WHERE error_code_reason = error_code_reason_param;
	return error_code;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 FUNCTION `kalturadw_ds`.`get_ip_country_location`(ip BIGINT) RETURNS varchar(30) CHARSET latin1
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE res VARCHAR(30);
	SELECT CONCAT(country_id,",",location_id)
	INTO res
	FROM kalturadw.dwh_dim_ip_ranges
	WHERE ip_from = (
	SELECT MAX(ip_from) 
	FROM kalturadw.dwh_dim_ip_ranges
	WHERE ip >= ip_from
	) ;
	RETURN res;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`add_cycle_partition`(p_cycle_id VARCHAR(10))
BEGIN
	DECLARE table_name VARCHAR(32);
	DECLARE done INT DEFAULT 0;
	DECLARE staging_areas_cursor CURSOR FOR SELECT source_table 
						FROM kalturadw_ds.staging_areas, kalturadw_ds.cycles 
						WHERE staging_areas.process_id = cycles.process_id AND cycles.cycle_id = p_cycle_id;
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN staging_areas_cursor;	
	read_loop: LOOP
		FETCH staging_areas_cursor INTO table_name;
		IF done THEN
			LEAVE read_loop;
		END IF;
		SET @s = CONCAT('alter table kalturadw_ds.',table_name,' ADD PARTITION (partition p_' ,	p_cycle_id ,' values in (', p_cycle_id ,'))');
		PREPARE stmt FROM  @s;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
	END LOOP;
	CLOSE staging_areas_cursor;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`drop_cycle_partition`(p_cycle_id VARCHAR(10))
BEGIN
	DECLARE table_name VARCHAR(32);
	DECLARE p_exists INT;
	DECLARE done INT DEFAULT 0;
	DECLARE staging_areas_cursor CURSOR FOR SELECT source_table 
						FROM kalturadw_ds.staging_areas, kalturadw_ds.cycles 
						WHERE staging_areas.process_id = cycles.process_id AND cycles.cycle_id = p_cycle_id;
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN staging_areas_cursor;	
	read_loop: LOOP
		FETCH staging_areas_cursor INTO table_name;
		IF done THEN
			LEAVE read_loop;
		END IF;
		
		SELECT COUNT(*) INTO p_exists
		FROM information_schema.PARTITIONS 
		WHERE partition_name = CONCAT('p_',p_cycle_id)
		AND table_name = table_name
		AND table_schema = 'kalturadw_ds';
		
		IF(p_exists>0) THEN
			SET @s = CONCAT('alter table kalturadw_ds.',table_name,' drop PARTITION  p_' ,p_cycle_id);
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		END IF;
	END LOOP;
	CLOSE staging_areas_cursor;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`empty_cycle_partition`(p_cycle_id VARCHAR(10))
BEGIN
	CALL drop_cycle_partition(p_cycle_id);
	CALL add_cycle_partition(p_cycle_id);
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`fms_sessionize`(
  partition_id INTEGER)
BEGIN
  DECLARE FMS_STALE_SESSION_PURGE DATETIME;

  SELECT SUBDATE(NOW(),INTERVAL int_value DAY) INTO FMS_STALE_SESSION_PURGE FROM parameters WHERE id=3;

  DROP TABLE IF EXISTS ds_temp_fms_session_aggr;
  DROP TABLE IF EXISTS ds_temp_fms_sessions;

  CREATE TEMPORARY TABLE ds_temp_fms_session_aggr (
    agg_session_id              VARCHAR(20) NOT NULL,
    agg_session_time            DATETIME    NOT NULL,
    agg_client_ip               VARCHAR(15),
    agg_client_ip_number        INT(10),
    agg_client_country_id       INT(10),
    agg_client_location_id      INT(10),
    agg_session_date_id         INT(11),
    agg_con_cs_bytes            BIGINT,
    agg_con_sc_bytes            BIGINT,
    agg_dis_cs_bytes            BIGINT,
    agg_dis_sc_bytes            BIGINT,
    agg_partner_id              INT(10),
    agg_bandwidth_source_id     INT(11),
    agg_is_connected_ind        INT(11),
    agg_is_disconnected_ind     INT(11)
  ) ENGINE = MEMORY;

  CREATE TEMPORARY TABLE ds_temp_fms_sessions (
    session_id                  VARCHAR(20) NOT NULL,
    session_time                DATETIME    NOT NULL,
    session_date_id             INT(11),
    session_client_ip           VARCHAR(15),
    session_client_ip_number    INT(10),
    country_id                  INT(10),
    location_id                 INT(10),
    session_partner_id          INT(10),
    bandwidth_source_id         INT(11),
    total_bytes                 BIGINT
   ) ENGINE = MEMORY;

  INSERT INTO ds_temp_fms_session_aggr (agg_session_id,agg_session_time,agg_session_date_id, agg_client_ip, agg_client_ip_number, agg_client_country_id, agg_client_location_id,
              agg_con_cs_bytes,agg_con_sc_bytes,agg_dis_cs_bytes,agg_dis_sc_bytes,agg_partner_id, agg_bandwidth_source_id, agg_is_connected_ind, agg_is_disconnected_ind)
SELECT session_id, MAX(event_time), MAX(event_date_id), MAX(client_ip), MAX(client_ip_number), MAX(client_country_id), MAX(client_location_id),
    SUM(IF(t.event_type='connect',client_to_server_bytes,0)) con_cs_bytes,
    SUM(IF(t.event_type='connect',server_to_client_bytes,0)) con_sc_bytes,
    SUM(IF(t.event_type='disconnect',client_to_server_bytes,0)) dis_cs_bytes,
    SUM(IF(t.event_type='disconnect',server_to_client_bytes,0)) dis_sc_bytes,
    MAX(partner_id) partner_id, MAX(bandwidth_source_id),
    MAX(IF(t.event_type='connect',1,0)) is_connected_ind,
    MAX(IF(t.event_type='disconnect',1,0)) is_disconnected_ind
  FROM ds_fms_session_events e
 INNER JOIN kalturadw.dwh_dim_fms_event_type t ON e.event_type_id = t.event_type_id
 INNER JOIN files f ON e.file_id = f.file_id
  LEFT OUTER JOIN kalturadw.dwh_dim_fms_bandwidth_source fbs ON (e.fms_app_id = fbs.fms_app_id AND f.process_id = fbs.process_id AND f.file_name REGEXP fbs.file_regex)
  WHERE e.cycle_id = partition_id
  GROUP BY session_id
  HAVING MAX(bandwidth_source_id) IS NOT NULL;

  INSERT INTO ds_temp_fms_sessions (session_id,session_time,session_date_id, session_client_ip, session_client_ip_number, country_id, location_id, session_partner_id, bandwidth_source_id, total_bytes)
  SELECT agg_session_id,agg_session_time,agg_session_date_id,agg_client_ip, agg_client_ip_number, agg_client_country_id, agg_client_location_id, agg_partner_id,agg_bandwidth_source_id,
  GREATEST(agg_dis_sc_bytes - agg_con_sc_bytes + agg_dis_cs_bytes - agg_con_cs_bytes, 0)
  FROM ds_temp_fms_session_aggr
  WHERE agg_partner_id IS NOT NULL AND agg_partner_id NOT IN (100  , -1  , -2  , 0 , 99 )  AND agg_is_connected_ind = 1 AND agg_is_disconnected_ind = 1;


  INSERT INTO fms_incomplete_sessions (session_id,session_time,updated_time,session_date_id, session_client_ip, session_client_ip_number, country_id, location_id, con_cs_bytes,con_sc_bytes,dis_cs_bytes,dis_sc_bytes,partner_id, is_connected_ind, is_disconnected_ind)
  SELECT agg_session_id,agg_session_time,NOW() AS agg_update_time,agg_session_date_id,agg_client_ip, agg_client_ip_number, agg_client_country_id, agg_client_location_id,
         agg_con_cs_bytes,agg_con_sc_bytes,agg_dis_cs_bytes,agg_dis_sc_bytes,agg_partner_id, agg_is_connected_ind, agg_is_disconnected_ind
  FROM ds_temp_fms_session_aggr
  WHERE agg_partner_id IS NULL OR agg_is_connected_ind = 0 AND agg_is_disconnected_ind = 0
  ON DUPLICATE KEY UPDATE
    session_time=GREATEST(session_time,VALUES(session_time)),
    session_date_id=GREATEST(session_date_id,VALUES(session_date_id)),
    session_client_ip=VALUES(session_client_ip),
    session_client_ip_number=VALUES(session_client_ip_number),
    location_id=VALUES(location_id),
    country_id=VALUES(country_id),
    con_cs_bytes=con_cs_bytes+VALUES(con_cs_bytes),
    con_sc_bytes=con_sc_bytes+VALUES(con_sc_bytes),
    dis_cs_bytes=dis_cs_bytes+VALUES(dis_cs_bytes),
    dis_sc_bytes=dis_sc_bytes+VALUES(dis_sc_bytes),
    partner_id=IF(partner_id IS NULL,VALUES(partner_id),partner_id),
    bandwidth_source_id=VALUES(bandwidth_source_id),
    updated_time=GREATEST(updated_time,VALUES(updated_time)),
    is_connected_ind = GREATEST(is_connected_ind, VALUES(is_connected_ind)),
    is_disconnected_ind = GREATEST(is_disconnected_ind, VALUES(is_disconnected_ind));

  INSERT INTO ds_temp_fms_sessions (session_id,session_time,session_date_id,session_client_ip, session_client_ip_number, country_id, location_id,session_partner_id,bandwidth_source_id,total_bytes)
  SELECT session_id,session_time,session_date_id,session_client_ip, session_client_ip_number, country_id, location_id,partner_id,bandwidth_source_id,
  GREATEST(dis_sc_bytes - con_sc_bytes + dis_cs_bytes -con_cs_bytes, 0)
  FROM fms_incomplete_sessions
  WHERE partner_id IS NOT NULL AND partner_id NOT IN (100  , -1  , -2  , 0 , 99 ) AND is_connected_ind = 1 AND is_disconnected_ind = 1;

  INSERT INTO fms_stale_sessions (partner_id, bandwidth_source_id, session_id, session_time,session_date_id,session_client_ip, session_client_ip_number, country_id, location_id,con_cs_bytes,con_sc_bytes,dis_cs_bytes,dis_sc_bytes,last_update_time,purge_time)
  SELECT partner_id,bandwidth_source_id, session_id,session_time,session_date_id,session_client_ip, session_client_ip_number, country_id, location_id,con_cs_bytes,con_sc_bytes,dis_cs_bytes,dis_sc_bytes,updated_time,NOW()
  FROM fms_incomplete_sessions
  WHERE GREATEST(session_time,updated_time) < FMS_STALE_SESSION_PURGE AND (partner_id IS NULL OR is_connected_ind = 0 AND is_disconnected_ind = 0);

  DELETE FROM fms_incomplete_sessions
  WHERE (partner_id IS NOT NULL AND is_connected_ind = 1 AND is_disconnected_ind = 1) OR
        GREATEST(session_time,updated_time) < FMS_STALE_SESSION_PURGE;

  INSERT INTO kalturadw.dwh_fact_fms_sessions (session_id,session_time,session_date_id,session_client_ip, session_client_ip_number, country_id, location_id,session_partner_id,bandwidth_source_id,total_bytes)
  SELECT session_id,session_time,session_date_id,session_client_ip, session_client_ip_number, country_id, location_id,session_partner_id,bandwidth_source_id,total_bytes
  FROM ds_temp_fms_sessions
  ON DUPLICATE KEY UPDATE
        total_bytes=VALUES(total_bytes),
        session_partner_id=VALUES(session_partner_id),
        session_time=VALUES(session_time),
        session_client_ip=VALUES(session_client_ip),
        session_client_ip_number=VALUES(session_client_ip_number),
        country_id=VALUES(country_id),
        location_id=VALUES(location_id),
        bandwidth_source_id=VALUES(bandwidth_source_id);
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`fms_sessionize_by_date_id`(p_event_date_id INT)
BEGIN
	DROP TABLE IF EXISTS ds_temp_fms_session_aggr;
	DROP TABLE IF EXISTS ds_temp_fms_sessions;
 
	CREATE TEMPORARY TABLE ds_temp_fms_session_aggr (
	    agg_session_id       	VARCHAR(20) NOT NULL,
	    agg_session_time     	DATETIME    NOT NULL,
	    agg_client_ip	 	VARCHAR(15),
	    agg_client_ip_number 	INT(10),
	    agg_client_country_id 	INT(10),
	    agg_client_location_id 	INT(10),
	    agg_session_date_id  	INT(11),
	    agg_con_cs_bytes     	BIGINT,
	    agg_con_sc_bytes     	BIGINT,
	    agg_dis_cs_bytes     	BIGINT,
	    agg_dis_sc_bytes     	BIGINT,
	    agg_partner_id       	INT(10),
	    agg_bandwidth_source_id     INT(11)
	  ) ENGINE = MEMORY;
	 
	  CREATE TABLE `kalturadw_ds`.ds_temp_fms_sessions (
	    session_id         		VARCHAR(20) NOT NULL,
	    session_time       		DATETIME    NOT NULL,
	    session_date_id    		INT(11),
	    session_client_ip	 	VARCHAR(15),
	    session_client_ip_number 	INT(10),
	    session_client_country_id 	INT(10),
	    session_client_location_id 	INT(10),
	    session_partner_id 		INT(10),
	    bandwidth_source_id		INT(11),
	    total_bytes        		BIGINT      
	   ) ENGINE = MEMORY;
	    
	
	INSERT INTO ds_temp_fms_session_aggr (agg_session_id,agg_session_time,agg_session_date_id, agg_client_ip, agg_client_ip_number, agg_client_country_id, agg_client_location_id,
		agg_con_cs_bytes,agg_con_sc_bytes,agg_dis_cs_bytes,agg_dis_sc_bytes,agg_partner_id, agg_bandwidth_source_id)
		SELECT session_id, MAX(event_time), MAX(event_date_id), MAX(client_ip), MAX(client_ip_number), MAX(client_country_id), MAX(client_location_id),  	
			SUM(IF(t.event_type='connect',client_to_server_bytes,0)) con_cs_bytes,
			SUM(IF(t.event_type='connect',server_to_client_bytes,0)) con_sc_bytes,
			SUM(IF(t.event_type='disconnect',client_to_server_bytes,0)) dis_cs_bytes,
			SUM(IF(t.event_type='disconnect',server_to_client_bytes,0)) dis_sc_bytes,
			MAX(partner_id) partner_id, MAX(bandwidth_source_id) bandwidth_source_id
		FROM kalturadw.dwh_fact_fms_session_events e 
		INNER JOIN kalturadw.dwh_dim_fms_event_type t ON e.event_type_id = t.event_type_id
		INNER JOIN files f ON e.file_id = f.file_id
		LEFT OUTER JOIN kalturadw.dwh_dim_fms_bandwidth_source fbs ON (e.fms_app_id = fbs.fms_app_id AND f.process_id = fbs.process_id)
		WHERE e.event_date_id = p_event_date_id 
		GROUP BY session_id
		HAVING MAX(bandwidth_source_id) IS NOT NULL;
	 
	INSERT INTO ds_temp_fms_sessions (session_id,session_time,session_date_id, session_client_ip, session_client_ip_number, session_client_country_id, session_client_location_id, session_partner_id, bandwidth_source_id, total_bytes)
		SELECT agg_session_id,agg_session_time,agg_session_date_id,agg_client_ip, agg_client_ip_number, agg_client_country_id, agg_client_location_id, agg_partner_id,agg_bandwidth_source_id,
		GREATEST(agg_dis_sc_bytes - agg_con_sc_bytes + agg_dis_cs_bytes -agg_con_cs_bytes, 0)
		FROM ds_temp_fms_session_aggr
		WHERE agg_partner_id IS NOT NULL AND agg_partner_id NOT IN (100  , -1  , -2  , 0 , 99 ) AND agg_dis_cs_bytes >0 AND agg_con_cs_bytes > 0;
	
	INSERT INTO kalturadw.dwh_fact_fms_sessions (session_id,session_time,session_date_id,session_client_ip, session_client_ip_number, session_client_country_id, session_client_location_id,session_partner_id,bandwidth_source_id,total_bytes)
	SELECT session_id,session_time,session_date_id,session_client_ip, session_client_ip_number, session_client_country_id, session_client_location_id,session_partner_id,bandwidth_source_id,total_bytes
	FROM ds_temp_fms_sessions
	ON DUPLICATE KEY UPDATE
		total_bytes=VALUES(total_bytes),
		session_partner_id=VALUES(session_partner_id),
		session_time=VALUES(session_time),
		session_client_ip=VALUES(session_client_ip),
		session_client_ip_number=VALUES(session_client_ip_number),
		session_client_country_id=VALUES(session_client_country_id),
		session_client_location_id=VALUES(session_client_location_id),
		bandwidth_source_id=VALUES(bandwidth_source_id);
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`insert_invalid_ds_line`(line_number_param INT(11), 
									file_id_param INT(11), 
									error_reason_param VARCHAR(255), 
									ds_line_param VARCHAR(4096), 
									date_id_param INT(11),
									partner_id_param INT(11), 
									cycle_id_param INT(11), 
									process_id_param INT(11))
BEGIN
	INSERT IGNORE INTO invalid_ds_lines (line_number, file_id, error_reason_code, ds_line, date_id, partner_id, cycle_id, process_id)
	VALUES (line_number_param, file_id_param, get_error_code(error_reason_param), ds_line_param, date_id_param, partner_id_param, cycle_id_param, process_id_param);
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`register_file`(p_file_name VARCHAR(750), p_process_id INT, p_file_size_kb INT(11), p_compression_suffix VARCHAR(10), p_subdir VARCHAR(1024))
BEGIN
	DECLARE v_assigned_server_id INT;
	DECLARE v_cycle_id INT;
	DECLARE v_file_id INT;
	
	SELECT file_id INTO v_file_id FROM kalturadw_ds.files WHERE file_name = p_file_name AND process_id = p_process_id AND compression_suffix = p_compression_suffix;
	
	IF (v_file_id IS NULL) THEN
		SELECT etl_server_id INTO v_assigned_server_id
			FROM kalturadw_ds.etl_servers s
				LEFT OUTER JOIN kalturadw_ds.cycles c 
					ON (s.etl_server_id = c.assigned_server_id AND c.STATUS = 'REGISTERED' AND c.process_id = p_process_id)
				LEFT OUTER JOIN kalturadw_ds.files f
					ON (c.cycle_id = f.cycle_id)		
			GROUP BY etl_server_id
			ORDER BY SUM(file_size_kb)/lb_constant, lb_constant desc LIMIT 1;
		
		IF (v_assigned_server_id IS NOT NULL) THEN
			SELECT c.cycle_id INTO v_cycle_id 
				FROM kalturadw_ds.processes p INNER JOIN kalturadw_ds.cycles c ON (c.process_id = p.id) LEFT OUTER JOIN kalturadw_ds.files f ON (c.cycle_id = f.cycle_id)
				WHERE 	p.id = p_process_id AND
					c.STATUS='REGISTERED' AND
					c.assigned_server_id = v_assigned_server_id
				GROUP BY c.cycle_id
				HAVING COUNT(file_id)<MAX(max_files_per_cycle) LIMIT 1;
			
			
			IF (v_cycle_id IS NOT NULL) THEN 
				INSERT INTO kalturadw_ds.files 	(file_name, file_status, insert_time, file_size_kb, process_id, cycle_id, compression_suffix, subdir)
							VALUES	(p_file_name, 'IN_CYCLE', NOW(), p_file_size_kb, p_process_id, v_cycle_id, p_compression_suffix, p_subdir);
			ELSE
				INSERT INTO kalturadw_ds.cycles (STATUS, insert_time, process_id, assigned_server_id)
							VALUES	('REGISTERED', NOW(), p_process_id, v_assigned_server_id);
				SET v_cycle_id = LAST_INSERT_ID();
				CALL add_cycle_partition(v_cycle_id);
				INSERT INTO kalturadw_ds.files 	(file_name, file_status, insert_time, file_size_kb, process_id, cycle_id, compression_suffix, subdir)
							VALUES	(p_file_name, 'IN_CYCLE', NOW(), p_file_size_kb, p_process_id, v_cycle_id, p_compression_suffix, p_subdir);
			END IF;
		END IF;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`restore_file_status`(
	pfile_id INT(20)
    )
BEGIN
	UPDATE kalturadw_ds.files f
	SET f.file_status = f.prev_status,
	    f.prev_status = f.file_status
	WHERE f.file_id = pfile_id;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`set_cycle_status`(
	p_cycle_id INT(20),
	new_cycle_status VARCHAR(20)
    )
BEGIN
	UPDATE kalturadw_ds.cycles c
	SET c.prev_status = c.status
	    ,c.status = new_cycle_status
	WHERE c.cycle_id = p_cycle_id;
	
	IF new_cycle_status = 'RUNNING'
	THEN 
		UPDATE kalturadw_ds.cycles c
		SET c.run_time = NOW()
		WHERE c.cycle_id = p_cycle_id;
	ELSEIF new_cycle_status = 'TRANSFERING'
	THEN 
		UPDATE kalturadw_ds.cycles c
		SET c.transfer_time = NOW()
		WHERE c.cycle_id = p_cycle_id;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`set_file_status`(
	pfile_id INT(20),
	new_file_status VARCHAR(20)
    )
BEGIN
	CALL set_file_status_full(pfile_id,new_file_status,1);
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`set_file_status_full`(
	pfile_id INT(20),
	new_file_status VARCHAR(20),
	override_safety_check INT
    )
BEGIN
	DECLARE cur_status VARCHAR(20);
	IF override_safety_check = 1 THEN
		SELECT f.file_status
		INTO cur_status
		FROM kalturadw_ds.files f
		WHERE f.file_id = pfile_id;
		IF  new_file_status NOT IN ('WAITING','RUNNING','PROCESSED','TRANSFERING','DONE','FAILED')
		 OR new_file_status = 'RUNNING' AND cur_status <> 'WAITING'
		 OR new_file_status = 'PROCESSED' AND cur_status <> 'RUNNING'
		 OR new_file_status = 'TRANSFERING' AND cur_status <> 'PROCESSED'
		 OR new_file_status = 'DONE' AND cur_status <> 'TRANSFERING'
		THEN
			SET @s = CONCAT('call Illegal_state_trying_to_set_',
					new_file_status,'_to_', cur_status,'_file_',pfile_id);
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;		
		END IF;
	END IF;
	
	UPDATE kalturadw_ds.files f
	SET f.prev_status = f.file_status
	    ,f.file_status = new_file_status
	WHERE f.file_id = pfile_id;
	IF new_file_status = 'RUNNING'
	THEN 
		UPDATE kalturadw_ds.files f
		SET f.run_time = NOW()
		WHERE f.file_id = pfile_id;
	ELSEIF new_file_status = 'TRANSFERING'
	THEN 
		UPDATE kalturadw_ds.files f
		SET f.transfer_time = NOW()
		WHERE f.file_id = pfile_id;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`transfer_cycle_partition`(p_cycle_id VARCHAR(10))
BEGIN
	DECLARE src_table VARCHAR(45);
	DECLARE tgt_table VARCHAR(45);
	DECLARE tgt_table_id INT;
	DECLARE dup_clause VARCHAR(4000);
	DECLARE partition_field VARCHAR(45);
	DECLARE select_fields VARCHAR(4000);
	DECLARE post_transfer_sp_val VARCHAR(4000);
	DECLARE v_ignore_duplicates_on_transfer BOOLEAN;	
	DECLARE aggr_date VARCHAR(400);
	DECLARE aggr_hour VARCHAR(400);
	DECLARE aggr_names VARCHAR(4000);
	DECLARE reset_aggr_min_date DATETIME;
	DECLARE v_reaggr_percent_trigger INT;
	
	
	DECLARE done INT DEFAULT 0;
	DECLARE staging_areas_cursor CURSOR FOR SELECT 	source_table, target_table_id, fact_table_name, IFNULL(on_duplicate_clause,''),	staging_partition_field, post_transfer_sp, aggr_date_field, hour_id_field, post_transfer_aggregations, reset_aggregations_min_date, ignore_duplicates_on_transfer, reaggr_percent_trigger
											FROM staging_areas s, cycles c, fact_tables f
											WHERE s.process_id=c.process_id AND c.cycle_id = p_cycle_id AND f.fact_table_id = s.target_table_id;
											
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN staging_areas_cursor;
	
	read_loop: LOOP
		FETCH staging_areas_cursor INTO src_table, tgt_table_id, tgt_table, dup_clause, partition_field, post_transfer_sp_val, aggr_date, aggr_hour, aggr_names, reset_aggr_min_date, v_ignore_duplicates_on_transfer, v_reaggr_percent_trigger;
		IF done THEN
			LEAVE read_loop;
		END IF;
	
		DROP TABLE IF EXISTS tmp_stats;
	
		SET @s = CONCAT('CREATE TEMPORARY TABLE tmp_stats '
				'SELECT ds.date_id, ds.hour_id, new_rows+IFNULL(uncalculated_records,0) as uncalculated_records, ',
				'IFNULL(total_records, 0) calculated_records from ',
				'(SELECT ', aggr_date, ' date_id, ', aggr_hour, ' hour_id, count(*) new_rows FROM ',src_table,
				' WHERE ', partition_field,'  = ',p_cycle_id, ' group by date_id, hour_id) ds ',
				'LEFT OUTER JOIN kalturadw_ds.fact_stats fs on ds.date_id = fs.date_id AND ds.hour_id = fs.hour_id
				AND fs.fact_table_id = ', tgt_table_id);
		PREPARE stmt FROM @s;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
		
		
		IF ((LENGTH(AGGR_DATE) > 0) && (LENGTH(aggr_names) > 0)) THEN
			SET @s = CONCAT('INSERT INTO kalturadw.aggr_managment(aggr_name, date_id, hour_id, data_insert_time)
					SELECT aggr_name, date_id, hour_id, now() 
					FROM kalturadw_ds.aggr_name_resolver a, tmp_stats ts
					WHERE 	aggr_name in ', aggr_names, '
					AND date_id >= date(\'',reset_aggr_min_date,'\')
					AND if(calculated_records=0,100, uncalculated_records*100/(calculated_records+uncalculated_records)) > ', v_reaggr_percent_trigger, '
					ON DUPLICATE KEY UPDATE data_insert_time = now()');
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		END IF;
		
		SELECT 	GROUP_CONCAT(column_name ORDER BY ordinal_position)
		INTO 	select_fields
		FROM information_schema.COLUMNS
		WHERE CONCAT(table_schema,'.',table_name) = tgt_table;
			
		SET @s = CONCAT('INSERT ', IF(v_ignore_duplicates_on_transfer=1, 'IGNORE', '') ,' INTO ',tgt_table, ' (',select_fields,') ',
						' SELECT ',select_fields,
						' FROM ',src_table,
						' WHERE ',partition_field,'  = ',p_cycle_id,
						' ',dup_clause );
		PREPARE stmt FROM @s;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
			
		INSERT INTO kalturadw_ds.fact_stats (fact_table_id, date_id, hour_id, total_records, uncalculated_records)
			SELECT tgt_table_id, date_id, hour_id,
				IF(calculated_records=0 OR uncalculated_records*100/(calculated_records+uncalculated_records) > v_reaggr_percent_trigger,
					calculated_records + uncalculated_records, calculated_records),
				IF(calculated_records=0 OR uncalculated_records*100/(calculated_records+uncalculated_records) > v_reaggr_percent_trigger,
					0, uncalculated_records)
			FROM tmp_stats t
		ON DUPLICATE KEY UPDATE 
			total_records = IF(t.calculated_records=0 OR t.uncalculated_records*100/(t.calculated_records+t.uncalculated_records) > v_reaggr_percent_trigger,
					t.calculated_records + t.uncalculated_records, t.calculated_records),
			uncalculated_records = IF(t.calculated_records=0 OR t.uncalculated_records*100/(t.calculated_records+t.uncalculated_records) > v_reaggr_percent_trigger,
					0, t.uncalculated_records);
	
		
		IF LENGTH(POST_TRANSFER_SP_VAL)>0 THEN
			SET @s = CONCAT('CALL ',post_transfer_sp_val,'(',p_cycle_id,')');
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		END IF;
	END LOOP;
	CLOSE staging_areas_cursor;
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
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `kalturadw_ds`.`unify_incomplete_api_calls`(p_cycle_id INTEGER)
BEGIN
    DROP TABLE IF EXISTS unified_api_calls;
    CREATE TEMPORARY TABLE unified_api_calls
    SELECT     cycle_calls.file_id,
        cycle_calls.line_number,
        cycle_calls.session_id,
        cycle_calls.request_index,
        IFNULL(cycle_calls.api_call_time, old_calls.api_call_time) api_call_time,
        IFNULL(cycle_calls.api_call_date_id, old_calls.api_call_date_id) api_call_date_id,
        IFNULL(cycle_calls.api_call_hour_id, old_calls.api_call_hour_id) api_call_hour_id,
        IFNULL(cycle_calls.partner_id, old_calls.partner_id) partner_id,
        IFNULL(cycle_calls.action_id, old_calls.action_id) action_id,
        IFNULL(cycle_calls.os_id, old_calls.os_id) os_id,
        IFNULL(cycle_calls.browser_id, old_calls.browser_id) browser_id,
        IFNULL(cycle_calls.client_tag_id, old_calls.client_tag_id) client_tag_id ,
        IFNULL(cycle_calls.is_admin, old_calls.is_admin) is_admin,
        IFNULL(cycle_calls.pid, old_calls.pid) pid,
        IFNULL(cycle_calls.host_id, old_calls.host_id) host_id,
        IFNULL(cycle_calls.user_ip, old_calls.user_ip) user_ip,
        IFNULL(cycle_calls.user_ip_number, old_calls.user_ip_number) user_ip_number,
        IFNULL(cycle_calls.country_id, old_calls.country_id) country_id,
        IFNULL(cycle_calls.location_id, old_calls.location_id) location_id,
        IFNULL(cycle_calls.master_partner_id, old_calls.master_partner_id) master_partner_id,
        IFNULL(cycle_calls.ks, old_calls.ks) ks,
        IFNULL(cycle_calls.kuser_id, old_calls.kuser_id) kuser_id,
        IFNULL(cycle_calls.is_in_multi_request, old_calls.is_in_multi_request) is_in_multi_request,
        IFNULL(cycle_calls.success, old_calls.success) success,
        IFNULL(cycle_calls.error_code_id, old_calls.error_code_id) error_code_id,
        IFNULL(cycle_calls.duration_msecs, old_calls.duration_msecs) duration_msecs
    FROM 
        kalturadw.dwh_fact_incomplete_api_calls cycle_calls, 
        kalturadw.dwh_fact_incomplete_api_calls old_calls
    WHERE 
        cycle_calls.session_id = old_calls.session_id
        AND cycle_calls.request_index = old_calls.request_index
        AND cycle_calls.cycle_id = p_cycle_id
        AND old_calls.cycle_id <> p_cycle_id
        AND IFNULL(cycle_calls.api_call_date_id, old_calls.api_call_date_id) IS NOT NULL
                AND IFNULL(cycle_calls.duration_msecs, old_calls.duration_msecs) IS NOT NULL;
 
        
    INSERT INTO kalturadw.dwh_fact_api_calls (file_id, line_number, session_id, request_index, api_call_time, api_call_date_id, 
                        api_call_hour_id, partner_id, action_id, os_id, browser_id, client_tag_id, is_admin,
                        pid, host_id, user_ip, user_ip_number, country_id, location_id, master_partner_id, 
                        ks, kuser_id, is_in_multi_request, success, error_code_id, duration_msecs)
    SELECT file_id, line_number, session_id, request_index, api_call_time, api_call_date_id, 
                        api_call_hour_id, partner_id, action_id, os_id, browser_id, client_tag_id, is_admin,
                        pid, host_id, user_ip, user_ip_number, country_id, location_id, master_partner_id, 
                        ks, kuser_id, is_in_multi_request, success, error_code_id, duration_msecs
    FROM unified_api_calls;
     
        
    INSERT INTO kalturadw.dwh_fact_errors
        (file_id, line_number, partner_id, 
        error_time, error_date_id, error_hour_id, 
        error_object_id, error_object_type_id, error_code_id)
    SELECT     file_id, line_number, partner_id, 
        api_call_time, api_call_date_id, api_call_hour_id,
        CONCAT(session_id, '_', request_index), error_object_type_id, error_code_id
    FROM unified_api_calls u, kalturadw.dwh_dim_error_object_types eot
    WHERE eot.error_object_type_name = 'API Call'
    AND error_code_id IS NOT NULL;
    
    DELETE kalturadw.dwh_fact_incomplete_api_calls
    FROM     kalturadw.dwh_fact_incomplete_api_calls, 
        unified_api_calls unified_calls
    WHERE 
        kalturadw.dwh_fact_incomplete_api_calls.session_id = unified_calls.session_id
        AND kalturadw.dwh_fact_incomplete_api_calls.request_index = unified_calls.request_index;
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

-- Dump completed on 2014-10-27  9:00:11
