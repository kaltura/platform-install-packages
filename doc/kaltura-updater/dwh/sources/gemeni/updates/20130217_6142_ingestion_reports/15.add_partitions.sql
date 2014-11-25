DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `add_partitions`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `add_partitions`()
BEGIN
	CALL add_daily_partition_for_table('dwh_fact_events');
	CALL add_daily_partition_for_table('dwh_fact_fms_session_events');
	CALL add_daily_partition_for_table('dwh_fact_fms_sessions');
	CALL add_daily_partition_for_table('dwh_fact_bandwidth_usage');
	CALL add_daily_partition_for_table('dwh_fact_api_calls');
	CALL add_daily_partition_for_table('dwh_fact_incomplete_api_calls');
    CALL add_daily_partition_for_table('dwh_fact_errors');
    CALL add_daily_partition_for_table('dwh_fact_file_sync');
	CALL add_monthly_partition_for_table('dwh_fact_entries_sizes');
	CALL add_monthly_partition_for_table('dwh_hourly_events_entry');
	CALL add_monthly_partition_for_table('dwh_hourly_events_domain');
	CALL add_monthly_partition_for_table('dwh_hourly_events_country');
	CALL add_monthly_partition_for_table('dwh_hourly_events_widget');
	CALL add_monthly_partition_for_table('dwh_hourly_events_uid');
	CALL add_monthly_partition_for_table('dwh_hourly_events_domain_referrer');
	CALL add_monthly_partition_for_table('dwh_hourly_partner');
	CALL add_monthly_partition_for_table('dwh_hourly_partner_usage');
	CALL add_monthly_partition_for_table('dwh_hourly_events_devices');
	CALL add_monthly_partition_for_table('dwh_hourly_api_calls');
    CALL add_monthly_partition_for_table('dwh_hourly_errors');
	CALL add_monthly_partition_for_table('dwh_hourly_events_context_entry_user_app');
	CALL add_monthly_partition_for_table('dwh_hourly_events_context_app');
	CALL add_monthly_partition_for_table('dwh_hourly_user_usage');
	CALL add_monthly_partition_for_table('dwh_daily_ingestion');
	CALL add_monthly_partition_for_table('dwh_daily_partner_ingestion');
END$$

DELIMITER ;