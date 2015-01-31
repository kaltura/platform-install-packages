USE `kalturadw`;
/*View structure for view dwh_dim_partners_v */

/*!50001 DROP TABLE IF EXISTS `dwh_dim_partners_v` */;
/*!50001 DROP VIEW IF EXISTS `dwh_dim_partners_v` */;

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER 
VIEW `dwh_dim_partners_v` AS (
    select 
        `a`.`partner_id` AS `partner_id`,
        `a`.`partner_name` AS `partner_name`,
        `a`.`url1` AS `url1`,
        `a`.`url2` AS `url2`,
        `a`.`secret` AS `secret`,
        `a`.`admin_secret` AS `admin_secret`,
        `a`.`max_number_of_hits_per_day` AS `max_number_of_hits_per_day`,
        `a`.`appear_in_search` AS `appear_in_search`,
        `a`.`debug_level` AS `debug_level`,
        `a`.`invalid_login_count` AS `invalid_login_count`,
        `a`.`created_at` AS `created_at`,
        `a`.`created_date_id` AS `created_date_id`,
        `a`.`created_hour_id` AS `created_hour_id`,
        `a`.`updated_at` AS `updated_at`,
        `a`.`updated_date_id` AS `updated_date_id`,
        `a`.`updated_hour_id` AS `updated_hour_id`,
        `a`.`partner_alias` AS `partner_alias`,
        `a`.`anonymous_kuser_id` AS `anonymous_kuser_id`,
        `a`.`ks_max_expiry_in_seconds` AS `ks_max_expiry_in_seconds`,
        `a`.`create_user_on_demand` AS `create_user_on_demand`,
        `a`.`prefix` AS `prefix`,
        `a`.`admin_name` AS `admin_name`,
        `a`.`admin_email` AS `admin_email`,
        `a`.`description` AS `description`,
        `a`.`commercial_use` AS `commercial_use`,
        `a`.`moderate_content` AS `moderate_content`,
        `a`.`notify` AS `notify`,
        `a`.`custom_data` AS `custom_data`,
        `a`.`service_config_id` AS `service_config_id`,
        `a`.`partner_status_id` AS `partner_status_id`,
        `b`.`partner_status_name` AS `partner_status_name`,
        `a`.`content_categories` AS `content_categories`,
        `a`.`partner_type_id` AS `partner_type_id`,
        `c`.`partner_type_name` AS `partner_type_name`,
        `a`.`phone` AS `phone`,
        `a`.`describe_yourself` AS `describe_yourself`,
        `a`.`adult_content` AS `adult_content`,
        `a`.`partner_package` AS `partner_package`,
        `a`.`usage_percent` AS `usage_percent`,
        `a`.`storage_usage` AS `storage_usage`,
        `a`.`eighty_percent_warning` AS `eighty_percent_warning`,
        `a`.`usage_limit_warning` AS `usage_limit_warning`,
        `a`.`dwh_creation_date` AS `dwh_creation_date`,
        `a`.`dwh_update_date` AS `dwh_update_date`,
        `a`.`ri_ind` AS `ri_ind`,
        `a`.`priority_group_id` AS `priority_group_id`,
        `a`.`work_group_id` AS `work_group_id`,
        `a`.`partner_group_type_id` AS `partner_group_type_id`,
        `d`.`partner_group_type_name` AS `partner_group_type_name`,
        `a`.`partner_parent_id` AS `partner_parent_id` 
        from (((`dwh_dim_partners` `a` 
                left join `dwh_dim_partner_status` `b` on((`a`.`partner_status_id` = `b`.`partner_status_id`))) 
                left join `dwh_dim_partner_type` `c` on((`a`.`partner_type_id` = `c`.`partner_type_id`))) 
                left join `dwh_dim_partner_group_type` `d` on((`a`.`partner_group_type_id` = `d`.`partner_group_type_id`))));

