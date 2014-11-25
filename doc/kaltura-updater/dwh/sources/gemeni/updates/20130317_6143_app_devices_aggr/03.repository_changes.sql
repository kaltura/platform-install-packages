INSERT INTO kalturadw_ds.aggr_name_resolver (aggr_name, aggr_table, aggr_id_field, dim_id_field, aggr_type)
VALUES ('app_devices', 'dwh_hourly_events_context_app_devices', 'context_id,application_id,os_id,browser_id', '', 'events');

UPDATE kalturadw_ds.staging_areas  SET post_transfer_aggregations = REPLACE(post_transfer_aggregations, ')',',\'app_devices\')') WHERE process_id in (1,3);
