USE kalturadw;

ALTER TABLE kalturadw.dwh_hourly_partner_usage
ADD COLUMN added_storage_mb DECIMAL(19,4) DEFAULT 0 AFTER count_storage_mb,
ADD COLUMN deleted_storage_mb DECIMAL(19,4) DEFAULT 0 AFTER added_storage_mb;



