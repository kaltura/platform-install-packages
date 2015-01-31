USE `kalturadw`;

ALTER TABLE kalturadw.`dwh_hourly_partner_usage`
ADD COLUMN billable_storage_mb DECIMAL(19,4);
