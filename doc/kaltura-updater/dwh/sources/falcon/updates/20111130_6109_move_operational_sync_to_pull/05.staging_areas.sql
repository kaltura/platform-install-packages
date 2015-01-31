UPDATE kalturadw_ds.staging_areas
SET post_transfer_aggregations = REPLACE(post_transfer_aggregations,'\'plays_views\',','') 
WHERE id in (1,3);
