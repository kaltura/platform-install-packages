USE `kalturadw`;

DROP TABLE IF EXISTS `dwh_dim_file_sync_new`;

CREATE TABLE `dwh_dim_file_sync_new` (
  `id` int (11),
	`partner_id` int (11),
	`object_type` int (4),
	`object_id` varchar (60),
	`version` varchar (60),
	`object_sub_type` tinyint (4),
	`dc` varchar (6),
	`original` tinyint (4),
	`created_at` datetime ,
	`updated_at` datetime ,
	`ready_at` datetime ,
	`sync_time` int (11),
	`status` tinyint (4),
	`file_type` tinyint (4),
	`linked_id` int (11),
	`link_count` int (11),
	`file_root` varchar (192),
	`file_path` varchar (384),
	`file_size` bigint (20),  
	`dwh_creation_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
	`dwh_update_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`ri_ind` TINYINT(4) NOT NULL DEFAULT '0'
) ENGINE=MYISAM; 

INSERT INTO kalturadw.dwh_dim_file_sync_new 
SELECT * FROM kalturadw.dwh_dim_file_sync;

ALTER TABLE kalturadw.dwh_dim_file_sync_new
  ADD PRIMARY KEY (`id`), 
  ADD UNIQUE KEY `unique_key` (`object_type`,`object_id`,`object_sub_type`,`version`,`dc`),
  ADD KEY `updated_at` (`updated_at`),
  ADD KEY `ready_at` (`ready_at`),
  ADD KEY `dwh_update_date` (`dwh_update_date`);
  
DROP TABLE kalturadw.dwh_dim_file_sync;
RENAME TABLE kalturadw.dwh_dim_file_sync_new TO kalturadw.dwh_dim_file_sync;
