ALTER TABLE kalturadw.dwh_dim_file_sync 
CHANGE COLUMN id id BIGINT(20),
ADD COLUMN deleted_id BIGINT(20) DEFAULT '0' AFTER `ri_ind`;

ALTER TABLE kalturadw.dwh_dim_file_sync 
DROP INDEX unique_key;

ALTER TABLE kalturadw.dwh_dim_file_sync 
ADD UNIQUE KEY unique_index (object_id,object_type,version,object_sub_type,dc,deleted_id);

 