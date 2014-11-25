UPDATE kalturadw.dwh_hourly_user_usage SET deleted_storage_kb = IF(added_storage_kb < 0, added_storage_kb*-1, 0), 
                                           deleted_entries = IF(added_entries < 0, added_entries*-1, 0),
										   deleted_msecs = IF(added_msecs < 0, added_msecs*-1, 0);
										   
update kalturadw.dwh_hourly_user_usage SET added_storage_kb = 0 where added_storage_kb < 0;
update kalturadw.dwh_hourly_user_usage SET added_entries = 0 where added_entries < 0;
update kalturadw.dwh_hourly_user_usage SET added_msecs = 0 where added_msecs < 0;


