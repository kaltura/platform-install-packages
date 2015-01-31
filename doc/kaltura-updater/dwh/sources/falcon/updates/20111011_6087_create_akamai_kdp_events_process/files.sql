UPDATE kalturadw_ds.files
SET process_id = 3 
WHERE file_name like 'akamai_%'
AND process_id = 1
