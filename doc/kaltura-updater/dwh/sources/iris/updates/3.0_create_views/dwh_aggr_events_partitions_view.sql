DELIMITER $$

DROP VIEW IF EXISTS `kalturadw`.`dwh_aggr_events_entry_partitions`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER 
VIEW `kalturadw`.`dwh_aggr_events_entry_partitions` AS SELECT `partitions`.`TABLE_NAME` AS `table_name`,`partitions`.`PARTITION_NAME` AS `partition_name`,`partitions`.`PARTITION_DESCRIPTION` AS `partition_description`,`partitions`.`TABLE_ROWS` AS `table_rows`,`partitions`.`CREATE_TIME` AS `create_time` FROM `information_schema`.`partitions` 
WHERE (`partitions`.`TABLE_NAME` 
	IN ('dwh_aggr_events_entry','dwh_aggr_events_country','dwh_aggr_events_domain' , 'dwh_aggr_partner' , 'dwh_aggr_events_widget'))$$

DELIMITER ;