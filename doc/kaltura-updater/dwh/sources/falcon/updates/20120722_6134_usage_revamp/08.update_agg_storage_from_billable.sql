USE kalturadw;

UPDATE kalturadw.dwh_hourly_partner_usage SET aggr_storage_mb = DAY(LAST_DAY(DATE(date_id)))*billable_storage_mb WHERE bandwidth_source_id = 1 AND aggr_storage_mb IS NULL;