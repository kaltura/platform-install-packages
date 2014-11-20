ALTER TABLE kalturadw.dwh_dim_batch_job_sep MODIFY dwh_id bigint NOT NULL AUTO_INCREMENT,
MODIFY id bigint DEFAULT NULL,
MODIFY parent_job_id bigint DEFAULT NULL,
MODIFY bulk_job_id bigint DEFAULT NULL,
MODIFY root_job_id bigint DEFAULT NULL,
MODIFY batch_job_lock_id bigint DEFAULT NULL;