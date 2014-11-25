DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `dwh_view_entry_type_display`$$

CREATE VIEW `kalturadw`.`dwh_view_entry_type_display` AS 
SELECT
  t.entry_type_id, t.entry_type_name, m.entry_media_type_id, m.entry_media_type_name,
    ifnull(d.display, concat(t.entry_type_name,'-',m.entry_media_type_name)) as display
FROM dwh_dim_entry_type_display d,
dwh_dim_entry_type t,
dwh_dim_entry_media_type m
WHERE t.entry_type_id = d.entry_type_id AND m.entry_media_type_id = d.entry_media_type_id
$$

DELIMITER ;
