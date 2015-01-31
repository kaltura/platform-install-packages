CREATE TABLE kalturadw.`dwh_dim_http_delivery_source` (
  `process_id` INT(10) NOT NULL,
  `bandwidth_source_id` INT(11) NOT NULL,
  `file_regex` VARCHAR(100) NOT NULL DEFAULT '.*',
  UNIQUE KEY (`process_id`,`bandwidth_source_id`, `file_regex`)
);

INSERT INTO kalturadw.`dwh_dim_http_delivery_source`
			(`process_id`,`bandwidth_source_id`,`file_regex`) 
VALUES 		(4,4,'_77660\\.|_113110\.|_146829\\.'),(4,7,'_105515\\.|_146836\\.|_146832\\.'),(4,8,'_159949\.'),(6,3,'.*');