ALTER TABLE kalturadw_ds.staging_areas
	ADD ignore_duplicates_on_transfer BOOLEAN NOT NULL DEFAULT 0;

UPDATE kalturadw_ds.staging_areas
	SET ignore_duplicates_on_transfer = 1
	WHERE process_id = 8;
