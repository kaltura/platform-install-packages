USE kalturadw;

DROP PROCEDURE IF EXISTS load_categories;

DELIMITER $$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `load_categories`()
BEGIN
    DECLARE v_entry_id VARCHAR(60);
    DECLARE v_partner_id INT(11);
    DECLARE v_categories VARCHAR(256);
    DECLARE v_updated_at TIMESTAMP;
    DECLARE v_category_name VARCHAR(256);
    DECLARE v_category_id INT;
    DECLARE v_categories_done INT;
    DECLARE v_categories_idx INT;
    DECLARE v_category_exists INT;
    DECLARE done INT DEFAULT 0;
    DECLARE entries CURSOR FOR
    SELECT partner_id, entry_id, categories, updated_at
    FROM dwh_dim_entries
    WHERE categories IS NOT NULL
    ORDER BY partner_id, entry_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN entries;

    read_loop: LOOP
        FETCH entries INTO v_partner_id, v_entry_id, v_categories, v_updated_at;
        IF done THEN
             LEAVE read_loop;
        END IF;

        SET v_categories_done = 0;
        SET v_categories_idx = 1;

        WHILE NOT v_categories_done DO
            SET v_category_name = TRIM(SUBSTRING(v_categories, v_categories_idx,
                    IF(LOCATE(',', v_categories, v_categories_idx) > 0,
                    LOCATE(',', v_categories, v_categories_idx) - v_categories_idx,
                    LENGTH(v_categories))));

            IF LENGTH(v_category_name) > 0 THEN
                SET v_categories_idx = v_categories_idx + LENGTH(v_category_name) + 1;
                -- add the category if it doesnt already exist
                SET v_category_id = NULL;
                
                SELECT COUNT(*) INTO v_category_exists FROM dwh_dim_categories WHERE category_name = v_category_name;
		IF NOT v_category_exists THEN
			INSERT INTO dwh_dim_categories (category_name) VALUES (v_category_name);
		END IF;
		SELECT category_id INTO v_category_id FROM dwh_dim_categories WHERE category_name = v_category_name;
		
                -- add the entry category
                INSERT IGNORE INTO dwh_dim_entry_categories (partner_id, entry_id, category_id, updated_at) VALUES (v_partner_id, v_entry_id, v_category_id, v_updated_at);
            ELSE
                SET v_categories_done = 1;
            END IF;
        END WHILE;
    END LOOP;
END$$

DELIMITER ;


CALL load_categories();

DROP PROCEDURE load_categories;
