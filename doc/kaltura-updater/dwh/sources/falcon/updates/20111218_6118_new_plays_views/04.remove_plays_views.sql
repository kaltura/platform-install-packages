USE kalturadw;

DELIMITER &&

CREATE PROCEDURE remove_plays_views(p_date_id INT, p_hour_id INT)
BEGIN
    INSERT INTO dwh_entry_plays_views(entry_id, plays, views)
    SELECT aggr.entry_id, 0 plays, 0 views
    FROM kalturadw.dwh_hourly_events_entry aggr
    WHERE date_id = p_date_id AND hour_id = p_hour_id 
    ON DUPLICATE KEY UPDATE 
        plays = IF(plays - VALUES(plays) >= 0, plays - VALUES(plays), 0),
        views = IF(views - VALUES(views) >= 0, views - VALUES(views), 0); 

END&&