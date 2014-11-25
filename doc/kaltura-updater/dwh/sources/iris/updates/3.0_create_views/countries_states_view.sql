DELIMITER $$

DROP VIEW IF EXISTS `kalturadw`.`dwh_dim_countries_states`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `kalturadw`.`dwh_dim_countries_states` AS 
(
	SELECT `dwh_dim_locations`.`country` AS `country`,`dwh_dim_locations`.`country_id` AS `country_id` 
		, `dwh_dim_locations`.`state` as `state` , `dwh_dim_locations`.`state_id` as `state_id` 
	FROM `kalturadw`.`dwh_dim_locations` 
	WHERE (`dwh_dim_locations`.`location_type_name` = 'state' )
)$$

DELIMITER ;