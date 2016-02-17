UPDATE kalturadw_ds.aggr_name_resolver
SET 	aggr_id_field = 'country_id,location_id,os_id,browser_id,ui_conf_id, entry_media_type_id'
WHERE aggr_name = 'devices';
