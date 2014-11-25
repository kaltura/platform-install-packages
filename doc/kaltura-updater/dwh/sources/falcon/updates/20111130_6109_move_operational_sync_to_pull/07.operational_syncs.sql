USE kalturadw_ds;

DROP TABLE IF EXISTS operational_syncs;

CREATE TABLE operational_syncs (
	operational_sync_id INT(11),
	operational_sync_name VARCHAR(1024),
	group_column VARCHAR(1024),
	entity_table VARCHAR(1024),
	aggregation_phrase VARCHAR(1024),
	aggregation_table VARCHAR(1024),
	bridge_entity VARCHAR(1024),
	bridge_table VARCHAR(1024),
	last_execution_parameter_id INT,	
	execution_start_time_parameter_id INT,
	PRIMARY KEY (operational_sync_id)
	);
	
INSERT INTO operational_syncs 
	(operational_sync_id, operational_sync_name, group_column, entity_table, aggregation_phrase, aggregation_table, 
	bridge_entity, bridge_table, last_execution_parameter_id, execution_start_time_parameter_id)
	VALUES
	(1, 'entry', 'entry_id', 'kalturadw.dwh_dim_entries', 'ifnull(sum(count_plays), 0) plays, ifnull(sum(count_loads), 0) views', 'kalturadw.dwh_hourly_events_entry', NULL, NULL, 4, 5),
	(2, 'kuser', 'kuser_id', 'kalturadw.dwh_dim_kusers', 'ifnull(sum(entry_additional_size_kb), 0) storage_size', 'kalturadw.dwh_fact_entries_sizes', 'entry_id', 'kalturadw.dwh_dim_entries', 6, 7);


