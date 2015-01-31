DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `do_tables_to_new`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `do_tables_to_new`(p_greater_than_or_equal_date_id int, p_less_than_date_id int, p_table_name varchar(256))
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
		/*Gets the select fields as an intersect of both the existing and the new table (in the case that the new table has a new column and missing a deprecated column*/
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

		UPDATE kalturadw_ds.tables_to_new SET is_copied = 1 
		WHERE greater_than_or_equal_date_id = p_greater_than_or_equal_date_id AND
                less_than_date_id = p_less_than_date_id AND
                table_name = p_table_name;
	END IF;
	
END$$

DELIMITER ;

DELIMITER $$

DROP PROCEDURE IF EXISTS `all_tables_to_new`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `all_tables_to_new`()
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
	
END$$

DELIMITER ;
