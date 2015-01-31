INSERT INTO kalturadw_ds.processes(id, process_name, max_files_per_cycle) 
VALUES (3, 'akamai_events',20);
INSERT INTO kalturadw_ds.staging_areas (id, process_id, source_table, target_table, on_duplicate_clause, staging_partition_field, post_transfer_sp, aggr_date_field, hour_id_field, post_transfer_aggregations)
VALUES (3, 3, 'ds_events', 'kalturadw.dwh_fact_events', NULL, 'cycle_id', NULL, 'event_date_id', 'event_hour_id', '(\'country\',\'domain\',\'entry\',\'partner\',\'plays_views\',\'uid\',\'widget\',\'domain_referrer\',\'devices\')');
