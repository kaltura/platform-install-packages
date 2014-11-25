ALTER TABLE kalturadw.dwh_hourly_events_devices ADD KEY (date_id,hour_id);
ALTER TABLE kalturadw.dwh_hourly_events_widget ADD KEY (date_id,hour_id);
ALTER TABLE kalturadw.dwh_hourly_events_uid ADD KEY (date_id,hour_id);
