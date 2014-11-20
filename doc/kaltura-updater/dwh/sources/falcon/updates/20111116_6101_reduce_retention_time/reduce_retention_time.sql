UPDATE kalturadw_ds.retention_policy
SET archive_start_days_back = 30
WHERE archive_start_days_back = 60;