DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `calc_aggr_day`(p_date_val DATE,p_hour_id INT(11), p_aggr_name VARCHAR(100))
BEGIN
	DECLARE v_aggr_table VARCHAR(100);
	DECLARE v_aggr_id_field VARCHAR(100);
	DECLARE extra VARCHAR(100);
	DECLARE v_from_archive DATE;
	DECLARE v_ignore DATE;
	DECLARE v_table_name VARCHAR(100);
	DECLARE v_join_table VARCHAR(100);
	DECLARE v_join_condition VARCHAR(200);
    		
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
		ELSE
			SET v_table_name = 'dwh_fact_events_archive';
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
			FROM ',v_table_name,' as ev USE INDEX (event_hour_id_event_date_id_partner_id), dwh_dim_entries e',v_join_table,
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
				SUM(duration / 60 / 4 * (v_25+v_50+v_75+v_100)) sum_time_viewed,
				COUNT(DISTINCT s_play) count_time_viewed
				FROM(
				SELECT ev.partner_id, ev.event_date_id, ev.event_hour_id',v_aggr_id_field,', ev.session_id,
					MAX(duration) duration,
					COUNT(DISTINCT IF(ev.event_type_id IN (4),1,NULL)) v_25,
					COUNT(DISTINCT IF(ev.event_type_id IN (5),1,NULL)) v_50,
					COUNT(DISTINCT IF(ev.event_type_id IN (6),1,NULL)) v_75,
					COUNT(DISTINCT IF(ev.event_type_id IN (7),1,NULL)) v_100,
					MAX(IF(event_type_id IN (3),session_id,NULL)) s_play
				FROM ',v_table_name,' as ev USE INDEX (event_hour_id_event_date_id_partner_id), dwh_dim_entries e',v_join_table,
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
