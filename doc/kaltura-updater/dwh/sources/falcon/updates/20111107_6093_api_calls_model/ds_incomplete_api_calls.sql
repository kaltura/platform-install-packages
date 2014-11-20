USE kalturadw_ds;

DROP TABLE IF EXISTS `ds_incomplete_api_calls`;
CREATE TABLE `ds_incomplete_api_calls` (
  `cycle_id` INT(11) NOT NULL,
  `file_id` INT(11) NOT NULL,
  `line_number` INT(11) NOT NULL,
  `api_call_time` DATETIME DEFAULT NULL,
  `api_call_date_id` INT(11) DEFAULT NULL,
  `api_call_hour_id` TINYINT(4) DEFAULT NULL,
  `session_id` VARCHAR(50) NOT NULL,
  `request_index` INT(11) DEFAULT NULL,
  `partner_id` INT(11) DEFAULT NULL,
  `action_id` INT(11) NOT NULL DEFAULT '0', 
  `os_id` INT(11) DEFAULT NULL,
  `browser_id` INT(11) DEFAULT NULL,
  `client_tag_id` INT(11) DEFAULT NULL,
  `is_admin` BOOL DEFAULT NULL,
  `pid` INT(11) DEFAULT NULL,
  `host_id` INT(11) DEFAULT NULL,
  `user_ip` VARCHAR(15) DEFAULT NULL,
  `user_ip_number` INT(10) UNSIGNED DEFAULT NULL,
  `country_id` INT(11) DEFAULT NULL,
  `location_id` INT(11) DEFAULT NULL,
  `master_partner_id` INT(11) DEFAULT NULL,
  `ks` VARCHAR(100) DEFAULT NULL,
  `kuser_id` INT(11) DEFAULT NULL,
  `is_in_multi_request` BOOL DEFAULT NULL,  
  `success` BOOL DEFAULT NULL,  
  `error_code_id` INT(11) DEFAULT NULL,
  `duration_msecs` INT(11) DEFAULT NULL
) ENGINE=INNODB DEFAULT CHARSET=utf8
PARTITION BY LIST(cycle_id) 
(PARTITION p_0 VALUES IN (0));
