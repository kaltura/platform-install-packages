UPDATE kalturadw_ds.staging_areas
SET post_transfer_aggregations = IF(id IN (1,3), '(\'country\',\'domain\',\'entry\',\'partner\',\'plays_views\',\'uid\',\'widget\',\'domain_referrer\',\'devices\')','(\'bandwidth_usage\',\'devices_bandwidth_usage\')')
