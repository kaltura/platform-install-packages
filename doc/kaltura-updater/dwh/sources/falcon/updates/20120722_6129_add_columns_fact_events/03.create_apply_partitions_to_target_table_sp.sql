USE kalturadw;

DELIMITER $$

DROP PROCEDURE IF EXISTS `apply_table_partitions_to_target_table`$$
CREATE DEFINER=`etl`@`localhost` PROCEDURE `apply_table_partitions_to_target_table`(p_table_name VARCHAR(255))
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
END$$

DELIMITER ;

CALL apply_table_partitions_to_target_table('dwh_fact_events_archive');
CALL apply_table_partitions_to_target_table('dwh_fact_events');

DROP PROCEDURE IF EXISTS `apply_table_partitions_to_target_table`;
