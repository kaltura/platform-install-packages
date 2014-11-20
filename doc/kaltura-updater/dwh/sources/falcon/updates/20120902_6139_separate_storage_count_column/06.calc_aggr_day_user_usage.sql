DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_user_usage`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `calc_aggr_day_user_usage`(p_date_id INT(11))
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
    SELECT         e.partner_id, e.kuser_id, SUM(if(f.entry_additional_size_kb > 0,entry_additional_size_kb,0)),SUM(IF(f.entry_additional_size_kb < 0,entry_additional_size_kb*-1,0))
    FROM         dwh_fact_entries_sizes f, dwh_dim_entries e
    WHERE        entry_size_date_id=p_date_id
    AND          f.entry_id = e.entry_id
    AND          e.entry_type_id IN (1,2,7,10)
    GROUP BY     e.kuser_id;
    
    DROP TABLE IF EXISTS entries_prev_owner;
    CREATE TEMPORARY TABLE entries_prev_owner AS
    SELECT partner_id, entry_id, prev_kuser_id, kuser_id 
    FROM dwh_dim_entries
    WHERE prev_kuser_id IS NOT NULL
	AND updated_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
    AND kuser_updated_date_id = p_date_id
    AND created_date_id <> p_date_id
    AND entry_type_id IN (1,2,7,10);
 
    ALTER TABLE entries_prev_owner ADD INDEX index_1 (kuser_id);
    
    INSERT INTO  temp_aggr_storage (partner_id, kuser_id, added_storage_kb, deleted_storage_kb)
    SELECT       o.partner_id, o.prev_kuser_id, 0, SUM(f.entry_additional_size_kb)
    FROM         dwh_fact_entries_sizes f, entries_prev_owner o
    WHERE        f.entry_id = o.entry_id
    AND          f.entry_size_date_id < p_date_id
    GROUP BY     o.prev_kuser_id;
    
    
    INSERT INTO  temp_aggr_storage (partner_id, kuser_id, added_storage_kb, deleted_storage_kb)
    SELECT       o.partner_id, o.kuser_id, SUM(f.entry_additional_size_kb), 0
    FROM         dwh_fact_entries_sizes f, entries_prev_owner o
    WHERE        f.entry_id = o.entry_id
    AND          f.entry_size_date_id < p_date_id
    GROUP BY     o.kuser_id;
    
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
    SUM(IF(entry_status_id IN (0,1,2,4) AND (created_date_id = p_date_id OR kuser_updated_date_id = p_date_id),1,0)),
    SUM(IF(entry_status_id = 3 AND (created_date_id <> p_date_id AND kuser_updated_date_id <> p_date_id),1,0)),
    SUM(IF(entry_status_id IN (0,1,2,4) AND (created_date_id = p_date_id OR kuser_updated_date_id = p_date_id),length_in_msecs,0)),
    SUM(IF(entry_status_id = 3 AND (created_date_id <> p_date_id AND kuser_updated_date_id <> p_date_id),length_in_msecs,0))
    FROM dwh_dim_entries e
    WHERE updated_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
    AND e.entry_type_id IN (1,2,7,10)
    GROUP BY kuser_id;
    
    INSERT INTO temp_aggr_entries(partner_id, kuser_id, added_entries, deleted_entries, added_msecs, deleted_msecs)
    SELECT o.partner_id, o.prev_kuser_id, 0, COUNT(*), 0, SUM(length_in_msecs)
    FROM entries_prev_owner o, dwh_dim_entries e
    WHERE o.entry_id = e.entry_id
    GROUP BY o.prev_kuser_id;
   
    
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
    FROM dwh_hourly_user_usage u JOIN (SELECT kuser_id, MAX(date_id) AS date_id FROM dwh_hourly_user_usage GROUP BY kuser_id) MAX
          ON u.kuser_id = max.kuser_id AND u.date_id = max.date_id; 
          
    INSERT INTO dwh_hourly_user_usage (partner_id, kuser_id, date_id, hour_id, added_storage_kb, deleted_storage_kb, total_storage_kb, added_entries, deleted_entries, total_entries, added_msecs, deleted_msecs, total_msecs)
    SELECT      aggr.partner_id, aggr.kuser_id, p_date_id, 0, SUM(added_storage_kb), SUM(deleted_storage_kb), SUM(added_storage_kb) - SUM(deleted_storage_kb) + IFNULL(latest_total.total_storage_kb,0),
                0, 0, IFNULL(latest_total.total_entries,0), 0, 0,  IFNULL(latest_total.total_msecs,0)
    FROM        temp_aggr_storage aggr LEFT JOIN latest_total ON aggr.kuser_id = latest_total.kuser_id
    WHERE added_storage_kb <> 0 OR deleted_storage_kb <> 0
    GROUP BY    aggr.kuser_id;
        
    INSERT INTO dwh_hourly_user_usage (partner_id, kuser_id, date_id, hour_id, added_storage_kb, deleted_storage_kb, total_storage_kb, added_entries, deleted_entries, total_entries, added_msecs, deleted_msecs, total_msecs)
    SELECT         aggr.partner_id, aggr.kuser_id, p_date_id, 0, 0, 0, IFNULL(latest_total.total_storage_kb,0), SUM(added_entries), SUM(deleted_entries), SUM(added_entries) - SUM(deleted_entries) + IFNULL(latest_total.total_entries,0),
            SUM(added_msecs), SUM(deleted_msecs), SUM(added_msecs) - SUM(deleted_msecs) + IFNULL(latest_total.total_msecs,0)
    FROM         temp_aggr_entries aggr LEFT JOIN latest_total ON aggr.kuser_id = latest_total.kuser_id
    WHERE added_entries <> 0 OR added_msecs <> 0 OR deleted_entries <> 0 OR deleted_msecs <> 0
    GROUP BY     aggr.kuser_id
    ON DUPLICATE KEY UPDATE added_entries = VALUES(added_entries), deleted_entries = VALUES(deleted_entries), total_entries=VALUES(total_entries), 
                            added_msecs=VALUES(added_msecs), deleted_msecs=VALUES(deleted_msecs), total_msecs=VALUES(total_msecs);
    
    
    UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'user_storage_usage' AND date_id = p_date_id; 
 
END$$

DELIMITER ;
