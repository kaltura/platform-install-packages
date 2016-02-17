UPDATE kalturadw.dwh_dim_bandwidth_source SET bandwidth_source_name = 'akamai_HD_1.0' WHERE bandwidth_source_id = 7;
INSERT INTO kalturadw.dwh_dim_bandwidth_source (bandwidth_source_id,bandwidth_source_name, is_live) values (8,'akamai_HD_2.0(HDS)', 0);
