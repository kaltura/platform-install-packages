DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_partner_billing_storage_per_category`$$

CREATE PROCEDURE `calc_partner_billing_storage_per_category`(p_start_date_id INT, p_end_date_id INT ,p_partner_id INT)
BEGIN
   
    
    DROP TEMPORARY TABLE IF EXISTS temp_storage;
    CREATE TEMPORARY TABLE temp_storage(
        category_name       VARCHAR(255) ,
        date_id             INT(11) NOT NULL,
        count_storage_mb    DECIMAL(19,4) NOT NULL
    ) ENGINE = MEMORY;
      
    INSERT INTO     temp_storage (category_name, date_id, count_storage_mb)
    SELECT  IF(ec.updated_at IS NULL OR c.category_name IS NULL,'-', c.category_name) category_name,  
        entry_size_date_id, 
        SUM(entry_additional_size_kb)/1024 aggr_storage_mb
    FROM    kalturadw.dwh_fact_entries_sizes es
        LEFT OUTER JOIN kalturadw.dwh_dim_entry_categories ec ON (ec.entry_id = es.entry_id AND ec.partner_id = es.partner_id)     
        LEFT OUTER JOIN kalturadw.dwh_dim_categories c ON (ec.category_id = c.category_id)
        LEFT OUTER JOIN kalturadw.dwh_dim_entries e ON (ec.partner_id = e.partner_id AND ec.entry_id = e.entry_id AND ec.updated_at = e.updated_at)
    WHERE es.partner_id = p_partner_id
    AND es.entry_size_date_id <= p_end_date_id    
    GROUP BY  IF(ec.updated_at IS NULL OR c.category_name IS NULL,'-', c.category_name) ,  es.entry_size_date_id;
      
 
    DROP TABLE IF EXISTS snapshot_storage;
    CREATE TEMPORARY TABLE snapshot_storage
    SELECT category_name, SUM(count_storage_mb) count_storage_mb
    FROM temp_storage
    GROUP BY category_name;

    DROP TABLE IF EXISTS avg_storage;
    CREATE TEMPORARY TABLE avg_storage
    SELECT s.category_name, SUM(s.count_storage_mb)/DAY(LAST_DAY(DATE(all_times.day_id))) avg_continuous_aggr_storage_mb
    FROM   dwh_dim_time all_times, temp_storage s 
    WHERE  all_times.day_id BETWEEN p_start_date_id AND p_end_date_id 
    AND all_times.day_id >= s.date_id 
    AND s.count_storage_mb<>0
    GROUP BY s.category_name;

    SELECT s.category_name, avg_continuous_aggr_storage_mb avg_storage_mb, count_storage_mb snapshot_storage_mb FROM avg_storage a 
    LEFT OUTER JOIN snapshot_storage s
    ON a.category_name = s.category_name;
        
END$$

DELIMITER ;
