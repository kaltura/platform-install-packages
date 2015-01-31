UPDATE kalturadw.dwh_hourly_partner_usage SET added_storage_mb = IF(count_storage_mb > 0, count_storage_mb, 0), deleted_storage_mb = IF(count_storage_mb < 0, count_storage_mb*-1, 0);

