USE `kalturadw_ds`;

ALTER TABLE aggr_name_resolver 
	DROP COLUMN aggr_join_stmt,
	CHANGE aggr_id_field aggr_id_field VARCHAR(1024) NOT NULL DEFAULT '',
	ADD dim_id_field VARCHAR(1024) NOT NULL DEFAULT '' AFTER aggr_id_field;
	
UPDATE kalturadw_ds.aggr_name_resolver
	SET dim_id_field = 'entry_id', aggr_id_field = ''
WHERE aggr_name = 'entry';

UPDATE kalturadw_ds.aggr_name_resolver
	SET dim_id_field = 'entry_media_type_id', aggr_id_field = 'country_id,location_id,os_id,browser_id,ui_conf_id'
WHERE aggr_name = 'devices';

UPDATE kalturadw_ds.aggr_name_resolver
	SET dim_id_field = 'kuser_id', aggr_id_field = ''
WHERE aggr_name = 'uid';