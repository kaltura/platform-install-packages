DELIMITER $$

USE `kalturadw_ds`$$

DROP PROCEDURE IF EXISTS `unify_incomplete_api_calls`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `unify_incomplete_api_calls`(p_cycle_id INTEGER)
BEGIN
    DROP TABLE IF EXISTS unified_api_calls;
    CREATE TEMPORARY TABLE unified_api_calls
    SELECT     cycle_calls.file_id,
        cycle_calls.line_number,
        cycle_calls.session_id,
        cycle_calls.request_index,
        IFNULL(cycle_calls.api_call_time, old_calls.api_call_time) api_call_time,
        IFNULL(cycle_calls.api_call_date_id, old_calls.api_call_date_id) api_call_date_id,
        IFNULL(cycle_calls.api_call_hour_id, old_calls.api_call_hour_id) api_call_hour_id,
        IFNULL(cycle_calls.partner_id, old_calls.partner_id) partner_id,
        IFNULL(cycle_calls.action_id, old_calls.action_id) action_id,
        IFNULL(cycle_calls.os_id, old_calls.os_id) os_id,
        IFNULL(cycle_calls.browser_id, old_calls.browser_id) browser_id,
        IFNULL(cycle_calls.client_tag_id, old_calls.client_tag_id) client_tag_id ,
        IFNULL(cycle_calls.is_admin, old_calls.is_admin) is_admin,
        IFNULL(cycle_calls.pid, old_calls.pid) pid,
        IFNULL(cycle_calls.host_id, old_calls.host_id) host_id,
        IFNULL(cycle_calls.user_ip, old_calls.user_ip) user_ip,
        IFNULL(cycle_calls.user_ip_number, old_calls.user_ip_number) user_ip_number,
        IFNULL(cycle_calls.country_id, old_calls.country_id) country_id,
        IFNULL(cycle_calls.location_id, old_calls.location_id) location_id,
        IFNULL(cycle_calls.master_partner_id, old_calls.master_partner_id) master_partner_id,
        IFNULL(cycle_calls.ks, old_calls.ks) ks,
        IFNULL(cycle_calls.kuser_id, old_calls.kuser_id) kuser_id,
        IFNULL(cycle_calls.is_in_multi_request, old_calls.is_in_multi_request) is_in_multi_request,
        IFNULL(cycle_calls.success, old_calls.success) success,
        IFNULL(cycle_calls.error_code_id, old_calls.error_code_id) error_code_id,
        IFNULL(cycle_calls.duration_msecs, old_calls.duration_msecs) duration_msecs
    FROM 
        kalturadw.dwh_fact_incomplete_api_calls cycle_calls, 
        kalturadw.dwh_fact_incomplete_api_calls old_calls
    WHERE 
        cycle_calls.session_id = old_calls.session_id
        AND cycle_calls.request_index = old_calls.request_index
        AND cycle_calls.cycle_id = p_cycle_id
        AND old_calls.cycle_id <> p_cycle_id
        AND IFNULL(cycle_calls.api_call_date_id, old_calls.api_call_date_id) IS NOT NULL
                AND IFNULL(cycle_calls.duration_msecs, old_calls.duration_msecs) IS NOT NULL;
 
        
    INSERT INTO kalturadw.dwh_fact_api_calls (file_id, line_number, session_id, request_index, api_call_time, api_call_date_id, 
                        api_call_hour_id, partner_id, action_id, os_id, browser_id, client_tag_id, is_admin,
                        pid, host_id, user_ip, user_ip_number, country_id, location_id, master_partner_id, 
                        ks, kuser_id, is_in_multi_request, success, error_code_id, duration_msecs)
    SELECT file_id, line_number, session_id, request_index, api_call_time, api_call_date_id, 
                        api_call_hour_id, partner_id, action_id, os_id, browser_id, client_tag_id, is_admin,
                        pid, host_id, user_ip, user_ip_number, country_id, location_id, master_partner_id, 
                        ks, kuser_id, is_in_multi_request, success, error_code_id, duration_msecs
    FROM unified_api_calls;
     
        
    INSERT INTO kalturadw.dwh_fact_errors
        (file_id, line_number, partner_id, 
        error_time, error_date_id, error_hour_id, 
        error_object_id, error_object_type_id, error_code_id)
    SELECT     file_id, line_number, partner_id, 
        api_call_time, api_call_date_id, api_call_hour_id,
        CONCAT(session_id, '_', request_index), error_object_type_id, error_code_id
    FROM unified_api_calls u, kalturadw.dwh_dim_error_object_types eot
    WHERE eot.error_object_type_name = 'API Call'
    AND error_code_id IS NOT NULL;
    
    DELETE kalturadw.dwh_fact_incomplete_api_calls
    FROM     kalturadw.dwh_fact_incomplete_api_calls, 
        unified_api_calls unified_calls
    WHERE 
        kalturadw.dwh_fact_incomplete_api_calls.session_id = unified_calls.session_id
        AND kalturadw.dwh_fact_incomplete_api_calls.request_index = unified_calls.request_index;
END$$

DELIMITER ;
