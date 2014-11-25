USE kalturadw;

DROP TABLE IF EXISTS `dwh_dim_upload_token_object_type`;
CREATE TABLE `dwh_dim_upload_token_object_type` (
  `upload_token_object_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `upload_token_object_type_name` varchar(127) NOT NULL,
  PRIMARY KEY (`upload_token_object_type_id`),
  UNIQUE KEY `browser` (`upload_token_object_type_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
