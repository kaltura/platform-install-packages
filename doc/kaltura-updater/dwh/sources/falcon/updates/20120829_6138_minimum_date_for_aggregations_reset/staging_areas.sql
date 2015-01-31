alter table kalturadw_ds.staging_areas
	ADD column reset_aggregations_min_date date not null default '1970-01-01' after post_transfer_aggregations;