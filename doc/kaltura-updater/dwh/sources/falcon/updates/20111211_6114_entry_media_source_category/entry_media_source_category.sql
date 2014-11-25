ALTER TABLE kalturadw.dwh_dim_entry_media_source ADD entry_media_source_category VARCHAR(25) NOT NULL DEFAULT 'IMPORT' AFTER entry_media_source_name ;

UPDATE kalturadw.dwh_dim_entry_media_source 
	SET entry_media_source_category = CASE entry_media_source_id WHEN 1 THEN 'UPLOAD' WHEN 2 THEN 'WEBCAM' ELSE 'IMPORT' END
