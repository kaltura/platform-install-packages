INSERT INTO kalturadw.ri_mapping
(table_name, column_name, date_id_column_name, date_column_name, reference_table, reference_column, perform_check)
VALUES ('dwh_hourly_errors', 'partner_id', 'date_id', '', 'dwh_dim_partners', 'partner_id', '1');
