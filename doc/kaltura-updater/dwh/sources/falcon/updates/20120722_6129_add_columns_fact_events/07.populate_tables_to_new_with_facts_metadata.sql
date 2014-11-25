use kalturadw_ds;

DROP TABLE IF EXISTS tables_to_new;
CREATE TABLE tables_to_new AS
SELECT partition_name, table_name, partition_expression column_name, @last_partition_description last_p,
IF(@last_partition_description<=partition_description,@last_partition_description, 0) greater_than_or_equal_date_id, @last_partition_description:=partition_description AS less_than_date_id, 0 is_copied
FROM information_schema.PARTITIONS p
WHERE p.table_name = 'dwh_fact_events'
ORDER BY table_name, partition_ordinal_position;
