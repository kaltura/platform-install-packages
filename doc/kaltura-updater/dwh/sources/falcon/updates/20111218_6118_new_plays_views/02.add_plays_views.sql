USE kalturadw;

DELIMITER &&

CREATE PROCEDURE add_plays_views(p_date_id INT, p_hour_id INT)
BEGIN
    INSERT INTO dwh_entry_plays_views(entry_id, plays, views)
    SELECT aggr.entry_id, IFNULL(count_plays, 0) plays, IFNULL(count_loads, 0) views
    FROM kalturadw.dwh_hourly_events_entry aggr
    WHERE date_id = p_date_id AND hour_id = p_hour_id 
    ON DUPLICATE KEY UPDATE 
        plays = plays + VALUES(plays) ,
        views = views + VALUES(views); 

END&&