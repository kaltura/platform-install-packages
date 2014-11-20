USE `kalturadw`;

INSERT INTO dwh_hourly_partner_usage (date_id, hour_id, partner_id, bandwidth_source_id,  billable_storage_mb)

SELECT 
	all_time.day_id date_id, 0 hour_id, 
	partner_id, 1 bandwidth_source_id,
	SUM(count_storage_mb) / DAY(LAST_DAY(day_id)) billable_storage_mb
FROM dwh_hourly_partner_usage u, dwh_dim_time all_time
WHERE 
	all_time.day_id <= DATE(NOW())*1 AND all_time.day_id >= date_id
AND count_storage_mb <> 0
AND hour_id = 0
	GROUP BY all_time.day_id , partner_id
	ON DUPLICATE KEY UPDATE billable_storage_mb = VALUES(billable_storage_mb);
