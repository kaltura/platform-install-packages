use kalturadw_ds;
ALTER TABLE etl_servers
	ADD column lb_constant float NOT NULL DEFAULT 1;
