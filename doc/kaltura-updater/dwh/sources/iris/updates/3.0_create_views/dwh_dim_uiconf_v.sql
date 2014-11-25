USE `kalturadw`;
/*View structure for view dwh_dim_ui_conf_v */

/*!50001 DROP TABLE IF EXISTS `dwh_dim_ui_conf_v` */;
/*!50001 DROP VIEW IF EXISTS `dwh_dim_ui_conf_v` */;

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `dwh_dim_ui_conf_v` AS (
select 
    `a`.`ui_conf_id` AS `ui_conf_id`,
    `a`.`ui_conf_type_id` AS `ui_conf_type_id`,
    `a`.`partner_id` AS `partner_id`,
    `a`.`subp_id` AS `subp_id`,
    `a`.`conf_file_path` AS `conf_file_path`,
    `a`.`ui_conf_name` AS `ui_conf_name`,
    `a`.`width` AS `width`,`a`.`height` AS `height`,
    `a`.`html_params` AS `html_params`,
    `a`.`swf_url` AS `swf_url`,
    `a`.`created_at` AS `created_at`,
    `a`.`created_date_id` AS `created_date_id`,
    `a`.`created_hour_id` AS `created_hour_id`,
    `a`.`updated_at` AS `updated_at`,
    `a`.`updated_date_id` AS `updated_date_id`,
    `a`.`updated_hour_id` AS `updated_hour_id`,
    `a`.`conf_vars` AS `conf_vars`,
    `a`.`use_cdn` AS `use_cdn`,
    `a`.`tags` AS `tags`,
    `a`.`custom_data` AS `custom_data`,
    `a`.`UI_Conf_Status_ID` AS `UI_Conf_Status_ID`,
    `a`.`description` AS `description`,
    `a`.`display_in_search` AS `display_in_search`,
    `a`.`dwh_creation_date` AS `dwh_creation_date`,
    `a`.`dwh_update_date` AS `dwh_update_date`,
    `a`.`ri_ind` AS `ri_ind`,
    `b`.`ui_conf_status_name` AS `ui_conf_status_name`,
    `c`.`ui_conf_type_name` AS `ui_conf_type_name` 
    from ((`dwh_dim_ui_conf` `a` 
            left join `dwh_dim_ui_conf_status` `b` on((`a`.`UI_Conf_Status_ID` = `b`.`ui_conf_status_id`))) 
            left join `dwh_dim_ui_conf_type` `c` on((`a`.`ui_conf_type_id` = `c`.`ui_conf_type_id`))));
