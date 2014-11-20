INSERT INTO kalturadw_ds.processes (id, process_name, max_files_per_cycle) VALUES (10, 'bandwidth_usage_AKAMAI_LIVE_URTMP', 50);


INSERT INTO kalturadw.dwh_dim_bandwidth_source (bandwidth_source_id,bandwidth_source_name, is_live) VALUES (9, 'akamai_live_urtmp',1);

INSERT INTO kalturadw.dwh_dim_http_delivery_source(process_id,bandwidth_source_id,file_regex) 
VALUES (10,9,'_172678\\.|_213019\\.');

INSERT INTO kalturadw_ds.staging_areas
        (id,
        process_id,
        source_table,
        target_table_id,
        on_duplicate_clause,
        staging_partition_field,
        post_transfer_sp,
		post_transfer_aggregations,
		aggr_date_field,
		hour_id_field)
VALUES
        (12,      10,
         'ds_bandwidth_usage',
         2,
         NULL,
         'cycle_id',
         NULL,
	'(\'bandwidth_usage\',\'devices_bandwidth_usage\')',
	'activity_date_id',
	'activity_hour_id');
