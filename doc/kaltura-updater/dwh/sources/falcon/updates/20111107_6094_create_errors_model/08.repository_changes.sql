INSERT INTO kalturadw_ds.staging_areas (id, process_id, source_table, target_table, on_duplicate_clause, staging_partition_field, post_transfer_sp,  aggr_date_field, hour_id_field, post_transfer_aggregations)
VALUES (11, 8, 'ds_errors', 'kalturadw.dwh_fact_errors', NULL, 'cycle_id', NULL, 'error_date_id', 'error_hour_id', '(\'errors\')');

INSERT INTO kalturadw_ds.retention_policy (table_name, archive_start_days_back, archive_delete_days_back, archive_last_partition)
VALUES ('dwh_fact_errors', 365, 2000, DATE(20110101));

INSERT INTO kalturadw_ds.aggr_name_resolver (aggr_name, aggr_table, aggr_id_field, aggr_type)
VALUES ('errors','dwh_hourly_errors','error_code_id','errors');
