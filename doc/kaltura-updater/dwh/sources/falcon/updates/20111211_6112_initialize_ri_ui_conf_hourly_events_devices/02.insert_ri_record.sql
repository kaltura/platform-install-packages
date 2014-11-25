INSERT INTO kalturadw.`ri_mapping` (`table_name`, `column_name`, `date_id_column_name`, `date_column_name`, `reference_table`, `reference_column`, `perform_check`)
      VALUES ('dwh_hourly_events_devices', 'ui_conf_id', 'date_id', '', 'dwh_dim_ui_conf', 'ui_conf_id', '1');
