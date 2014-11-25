DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `dwh_fact_events_v`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `dwh_fact_events_v` AS (
SELECT
  `dwh_fact_events`.`file_id`          AS `file_id`,
  `dwh_fact_events`.`event_id`         AS `event_id`,
  `dwh_fact_events`.`event_type_id`    AS `event_type_id`,
  `dwh_fact_events`.`client_version`   AS `client_version`,
  `dwh_fact_events`.`event_time`       AS `event_time`,
  `dwh_fact_events`.`event_date_id`    AS `event_date_id`,
  `dwh_fact_events`.`event_hour_id`    AS `event_hour_id`,
  `dwh_fact_events`.`session_id`       AS `session_id`,
  `dwh_fact_events`.`partner_id`       AS `partner_id`,
  `dwh_fact_events`.`entry_id`         AS `entry_id`,
  `dwh_fact_events`.`unique_viewer`    AS `unique_viewer`,
  `dwh_fact_events`.`widget_id`        AS `widget_id`,
  `dwh_fact_events`.`ui_conf_id`       AS `ui_conf_id`,
  `dwh_fact_events`.`uid`              AS `uid`,
  `dwh_fact_events`.`current_point`    AS `current_point`,
  `dwh_fact_events`.`duration`         AS `duration`,
  `dwh_fact_events`.`user_ip`          AS `user_ip`,
  `dwh_fact_events`.`user_ip_number`   AS `user_ip_number`,
  `dwh_fact_events`.`country_id`       AS `country_id`,
  `dwh_fact_events`.`location_id`      AS `location_id`,
  `dwh_fact_events`.`process_duration` AS `process_duration`,
  `dwh_fact_events`.`control_id`       AS `control_id`,
  `dwh_fact_events`.`seek`             AS `seek`,
  `dwh_fact_events`.`new_point`        AS `new_point`,
  `dwh_fact_events`.`domain_id`        AS `domain_id`,
  `dwh_fact_events`.`referrer`         AS `referrer`
FROM `dwh_fact_events`
WHERE ((`dwh_fact_events`.`event_date_id` between cast((curdate() + interval -(1) day) as unsigned) and 
                                                  cast((curdate() + interval -(0) day) as unsigned))) 
LIMIT 100)$$

DELIMITER ;