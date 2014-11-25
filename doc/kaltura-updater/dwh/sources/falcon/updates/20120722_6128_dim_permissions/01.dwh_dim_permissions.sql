DROP TABLE IF EXISTS `kalturadw`.`dwh_dim_permissions`;

CREATE TABLE `kalturadw`.`dwh_dim_permissions` (
  `permission_id` INT(11) NOT NULL,
  `type` INT(11) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `partner_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT 0,
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `ri_ind` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`permission_id`),
  KEY `partner_permission_index` (`partner_id`,`name`),
  KEY `dwh_update_date` (`dwh_update_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TRIGGER `kalturadw`.`dwh_dim_permissions_setcreationtime_oninsert` BEFORE INSERT
    ON `kalturadw`.`dwh_dim_permissions`
    FOR EACH ROW 
        SET new.dwh_creation_date = NOW();


