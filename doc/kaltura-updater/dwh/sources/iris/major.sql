/* 6154 - playManifest aggregation */
CREATE TABLE kalturadw_ds.aggr_type (
	`aggr_name` varchar(20) NOT NULL,
    `aggr_order` int(6) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

REPLACE INTO kalturadw_ds.aggr_type
	(aggr_name,
	aggr_order)
VALUES
	('events', 1),
	('bandwidth' , 2),
	('plays' , 3);
	
REPLACE INTO kalturadw_ds.fact_tables
                (fact_table_id,
                fact_table_name)
VALUES
        (7,'kalturadw.dwh_fact_plays');


REPLACE INTO kalturadw_ds.staging_areas
        (id,
        process_id,
        source_table,
        target_table_id,
        on_duplicate_clause,
        staging_partition_field,
        post_transfer_sp,
                post_transfer_aggregations,
                aggr_date_field,
                hour_id_field)
VALUES
        (13,1,
         'ds_plays',
         7,
         NULL,
         'cycle_id',
         NULL,
        '(\'plays_partner\',\'plays_entry\')',
        'play_date_id',
        'play_hour_id');

REPLACE INTO kalturadw_ds.retention_policy VALUES
('dwh_fact_plays', 30, 365, DATE('2014-06-01'));

REPLACE INTO kalturadw_ds.aggr_name_resolver
                (aggr_name,
                aggr_table,
                aggr_id_field,
                dim_id_field,
                aggr_type,
                join_table,
                join_id_field)
VALUES
        ('plays_partner','dwh_hourly_plays_partner','','','plays',NULL,NULL),
        ('plays_entry','dwh_hourly_plays_entry','entry_id','','plays',NULL,NULL);
		

USE `kalturadw_ds`;

CREATE TABLE `kalturadw_ds`.`ds_plays`(
  `line_number` INT(10),
  `cycle_id` INT(11) NOT NULL,
  `file_id` INT(11) NOT NULL,
  `partner_id` INT(11) NOT NULL,
  `entry_id` VARCHAR(20),
  `play_date_id` INT(11),
  `play_hour_id` INT(11),
  `client_tag_id` SMALLINT(6),
  `user_ip` VARCHAR(15),
  `user_ip_number` INT(10) UNSIGNED,
  `country_id` INT(11),
  `location_id` INT(11),
  `os_id` INT(11),
  `browser_id` INT(11)
) ENGINE=INNODB DEFAULT CHARSET=utf8
PARTITION BY LIST (cycle_id)
(PARTITION p_0 VALUES IN (0) ENGINE = INNODB);

USE `kalturadw`;

DROP TABLE IF EXISTS `dwh_fact_plays`;

CREATE TABLE `dwh_fact_plays` (
  `file_id` INT(11) NOT NULL,
  `line_number` INT (11),
  `partner_id` INT(11) NOT NULL DEFAULT '-1',
  `entry_id` varchar(20) DEFAULT NULL,
  `play_date_id` INT(11) DEFAULT '-1',
  `play_hour_id` TINYINT(4) DEFAULT '-1',
  `client_tag_id` SMALLINT(6),
  `user_ip` VARCHAR(15) DEFAULT NULL,
  `user_ip_number` INT(10) UNSIGNED DEFAULT NULL,
  `country_id` INT(11) DEFAULT NULL,
  `location_id` INT(11) DEFAULT NULL,
  `os_id` int(11),
  `browser_id` int(11),
  UNIQUE KEY (`file_id`,`line_number`,`play_date_id`),
  KEY Entry_id (entry_id),
  KEY `play_hour_id_play_date_id_partner_id` (play_hour_id, play_date_id, partner_id)
) ENGINE=INNODB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY RANGE (play_date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = INNODB) */;

CALL add_daily_partition_for_table('dwh_fact_plays');

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_play`$$

CREATE PROCEDURE `calc_aggr_day_play`(p_date_val DATE,p_hour_id INT(11), p_aggr_name VARCHAR(100))
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

END$$

DELIMITER ;

USE `kalturadw`;
 
CREATE TABLE kalturadw.`dwh_hourly_plays_partner` (
  `partner_id` INT DEFAULT NULL,
  `date_id` INT DEFAULT NULL,
  `hour_id` INT DEFAULT NULL,
  `client_tag_id` INT DEFAULT NULL,
  `count_plays` INT DEFAULT NULL,
   PRIMARY KEY (`partner_id`,`date_id`, `hour_id`, `client_tag_id`),
  KEY (`date_id`, `hour_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = INNODB);

CALL kalturadw.add_monthly_partition_for_table('dwh_hourly_plays_partner');

CREATE TABLE kalturadw.`dwh_hourly_plays_entry` (
  `partner_id` INT DEFAULT NULL,
  `date_id` INT DEFAULT NULL,
  `hour_id` INT DEFAULT NULL,
  `client_tag_id` INT DEFAULT NULL,
  `entry_id` VARCHAR(20) DEFAULT NULL,
  `count_plays` INT DEFAULT NULL,
   PRIMARY KEY (`partner_id`,`date_id`, `hour_id`, `client_tag_id`,`entry_id`),
   KEY (`date_id`, `hour_id`),
   KEY `entry_id` (`entry_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = INNODB);

CALL kalturadw.add_monthly_partition_for_table('dwh_hourly_plays_entry');

DROP TABLE IF EXISTS `dwh_fact_plays_archive`;

CREATE TABLE `dwh_fact_plays_archive` (
  `file_id` INT(11) NOT NULL,
  `line_number` INT (11),
  `partner_id` INT(11) NOT NULL DEFAULT '-1',
  `entry_id` varchar(20) DEFAULT NULL,
  `play_date_id` INT(11) DEFAULT '-1',
  `play_hour_id` TINYINT(4) DEFAULT '-1',
  `client_tag_id` SMALLINT(6),
  `user_ip` VARCHAR(15) DEFAULT NULL,
  `user_ip_number` INT(10) UNSIGNED DEFAULT NULL,
  `country_id` INT(11) DEFAULT NULL,
  `location_id` INT(11) DEFAULT NULL,
  `os_id` int(11),
  `browser_id` int(11)
) ENGINE=ARCHIVE DEFAULT CHARSET=utf8
PARTITION BY RANGE (play_date_id)
(PARTITION p_0 VALUES LESS THAN (1) ENGINE = ARCHIVE);


DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `add_partitions`$$

CREATE PROCEDURE `add_partitions`()
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
                
END$$

DELIMITER ;

DROP TABLE IF EXISTS kalturadw.dwh_dim_client_tag;

CREATE TABLE kalturadw.dwh_dim_client_tag (
  client_tag_id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  KEY client_tag_id (client_tag_id),
  KEY name (name)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/* 6155 - live entry aggregation   */

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day`$$

CREATE PROCEDURE `calc_aggr_day`(p_date_val DATE,p_hour_id INT(11), p_aggr_name VARCHAR(100))
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

END$$

DELIMITER ;


CREATE TABLE kalturadw.`dwh_hourly_events_live_entry` (
  `partner_id` INT DEFAULT NULL,
  `date_id` INT DEFAULT NULL,
  `hour_id` INT DEFAULT NULL,
  `entry_id` VARCHAR(20) DEFAULT NULL,
  `count_plays` INT DEFAULT NULL,
  `count_loads` INT DEFAULT NULL,
  PRIMARY KEY `partner_id` (`partner_id`,`date_id`,`hour_id`,`entry_id`),
  KEY (`date_id`,`hour_id`),
  KEY `entry_id` (`entry_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = INNODB);

USE kalturadw;

DELIMITER &&

DROP PROCEDURE IF EXISTS `add_live_plays_views`&&

CREATE PROCEDURE add_live_plays_views(p_date_id INT, p_hour_id INT)
BEGIN
    INSERT INTO dwh_entry_plays_views(entry_id, plays, views)
    SELECT aggr.entry_id, IFNULL(count_plays, 0) plays, IFNULL(count_loads, 0) views
    FROM kalturadw.dwh_hourly_events_live_entry aggr
    WHERE date_id = p_date_id AND hour_id = p_hour_id
    ON DUPLICATE KEY UPDATE
        plays = plays + VALUES(plays) ,
        views = views + VALUES(views);

END&&

DELIMITER ;

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `remove_live_plays_views`$$

CREATE PROCEDURE `remove_live_plays_views`(p_date_id INT, p_hour_id INT)
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

END$$

DELIMITER ;

update kalturadw_ds.staging_areas set post_transfer_aggregations = '(\'country\',\'domain\',\'entry\',\'partner\',\'uid\',\'widget\',\'domain_referrer\',\'devices\',\'users\',\'context\',\'app_devices\',\'live_entry\')' where id = 1;

INSERT  INTO kalturadw_ds.aggr_name_resolver(aggr_name,aggr_table,aggr_id_field,dim_id_field,aggr_type,join_table,join_id_field)
VALUES ('live_entry','dwh_hourly_events_live_entry','','entry_id','events','','');

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `add_partitions`$$

CREATE PROCEDURE `add_partitions`()
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

END$$

DELIMITER ;

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `pre_aggregation_live_entry`$$

CREATE PROCEDURE `pre_aggregation_live_entry`(date_val DATE, p_hour_id INT(11))
BEGIN
        CALL remove_live_plays_views(date_val*1, p_hour_id);
END$$

DELIMITER ;

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `post_aggregation_live_entry`$$

CREATE PROCEDURE `post_aggregation_live_entry`(date_val DATE, p_hour_id INT(11))
BEGIN
        CALL add_live_plays_views(date_val*1, p_hour_id);

END$$

DELIMITER ;

/* live bandwidth */

REPLACE INTO kalturadw_ds.processes (id, process_name, max_files_per_cycle) VALUES (12, 'kaltura_live_bandwidth', 20);

REPLACE INTO kalturadw.dwh_dim_bandwidth_source (bandwidth_source_id,bandwidth_source_name, is_live) VALUES (10, 'kaltura_live',1);

REPLACE INTO kalturadw_ds.staging_areas
        (id,
        process_id,
        source_table,
        target_table_id,
        on_duplicate_clause,
        staging_partition_field,
        post_transfer_sp,
                post_transfer_aggregations,
                aggr_date_field,
                hour_id_field)
VALUES
        (14,      12,
         'ds_bandwidth_usage',
         2,
         NULL,
         'cycle_id',
         NULL,
        '(\'bandwidth_usage\')',
        'activity_date_id',
        'activity_hour_id');

UPDATE kalturadw_ds.retention_policy SET archive_delete_days_back = 365 WHERE archive_delete_days_back > 365;


