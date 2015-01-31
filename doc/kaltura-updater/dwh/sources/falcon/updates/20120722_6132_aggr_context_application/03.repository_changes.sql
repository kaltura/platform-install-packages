INSERT INTO kalturadw_ds.aggr_name_resolver (aggr_name, aggr_table, aggr_id_field, dim_id_field, aggr_type, join_table, join_id_field)
VALUES ('context', 'dwh_hourly_events_context_app', 'context_id,application_id', '', 'events', 'dwh_dim_user_reports_allowed_partners', 'partner_id');

UPDATE kalturadw_ds.staging_areas  SET post_transfer_aggregations = REPLACE(post_transfer_aggregations, ')',',\'context\')') WHERE process_id in (1,3);
