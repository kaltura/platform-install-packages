DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_partner_billing_storage_per_category`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `calc_partner_billing_storage_per_category`(p_start_date_id INT, p_end_date_id INT ,p_partner_id INT)
BEGIN
   -- Fetch storage per entry of this partner (as seen on selected date)
    
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
    
    DROP TEMPORARY TABLE IF EXISTS temp_storage_2;
    CREATE TEMPORARY TABLE temp_storage_2 AS SELECT * FROM temp_storage;
    
    -- add aggr_storage
    DROP TEMPORARY TABLE IF EXISTS temp_aggr_storage;
    CREATE TEMPORARY TABLE temp_aggr_storage(
        category_name       VARCHAR(255) ,
        date_id             INT(11) NOT NULL,
        aggr_storage_mb    DECIMAL(19,4) NOT NULL
    ) ENGINE = MEMORY;
    
    INSERT INTO     temp_aggr_storage
    SELECT         a.category_name, a.date_id, SUM(b.count_storage_mb)
    FROM         temp_storage a, temp_storage_2 b 
    WHERE         a.category_name=b.category_name AND p_end_date_id >=a.date_id AND a.date_id >= b.date_id AND b.count_storage_mb<>0
    GROUP BY     a.date_id, a.category_name;
        
    DROP TEMPORARY TABLE IF EXISTS temp_aggr_storage_inner;
    CREATE TEMPORARY TABLE temp_aggr_storage_inner AS SELECT * FROM temp_aggr_storage;
    
    -- fetch results per category
    
    SELECT
        category_name,
        SUM(continuous_aggr_storage/DAY(LAST_DAY(continuous_category_storage.date_id))) avg_continuous_aggr_storage_mb
    FROM
    (    
        SELECT  all_times.day_id date_id,
            category_name,
            (SELECT aggr_storage_mb FROM temp_aggr_storage_inner inner_a_p
             WHERE  inner_a_p.category_name = stor.category_name
                    AND inner_a_p.date_id<=all_times.day_id 
                    AND inner_a_p.aggr_storage_mb IS NOT NULL 
                    ORDER BY inner_a_p.date_id DESC LIMIT 1) continuous_aggr_storage
                    FROM temp_aggr_storage stor, dwh_dim_time all_times
                WHERE   all_times.day_id BETWEEN 20081230 AND p_end_date_id
        GROUP BY category_name, all_times.day_id
    ) continuous_category_storage
    WHERE date_id BETWEEN p_start_date_id AND p_end_date_id
    GROUP BY category_name;
    
END$$

DELIMITER ;
