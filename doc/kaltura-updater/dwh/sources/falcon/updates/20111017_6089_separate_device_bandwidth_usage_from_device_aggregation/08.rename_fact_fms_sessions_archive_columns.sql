ALTER TABLE kalturadw.dwh_fact_fms_sessions_archive
	CHANGE session_client_location_id location_id int(11), 
	CHANGE session_client_country_id country_id int(11);
