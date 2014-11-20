ALTER TABLE kalturadw_ds.aggr_name_resolver ADD COLUMN aggr_type VARCHAR(60) NOT NULL;
UPDATE kalturadw_ds.aggr_name_resolver SET aggr_type = 'events';

INSERT INTO kalturadw_ds.aggr_name_resolver (aggr_name, aggr_table, aggr_id_field, aggr_type)
VALUES('bandwidth_usage', 'dwh_hourly_partner_usage', 'bandwidth_source_id', 'bandwidth'), ('devices_bandwidth_usage', 'dwh_hourly_events_devices', 'country_id, location_id','bandwidth');
