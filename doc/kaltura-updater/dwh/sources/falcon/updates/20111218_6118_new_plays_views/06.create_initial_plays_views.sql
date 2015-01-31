USE kalturadw;

DROP PROCEDURE IF EXISTS calc_plays_views;

DELIMITER &&

CREATE PROCEDURE calc_plays_views()
BEGIN
    DECLARE v_date_id INT(11);
    DECLARE v_hour_id INT(11);
    DECLARE v_done INT(1) DEFAULT 0;

    DECLARE c_partitions CURSOR FOR SELECT DISTINCT date_id, hour_id FROM kalturadw.dwh_hourly_events_entry;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;

    OPEN c_partitions;

    TRUNCATE TABLE dwh_entry_plays_views;

    INSERT INTO dwh_entry_plays_views (entry_id, plays, views, updated_at)
    SELECT entry_id, plays, views, DATE(20000101)
    FROM entry_plays_views_before_08_2009;

    read_loop: LOOP
        FETCH c_partitions INTO v_date_id, v_hour_id;
        IF v_done = 1 THEN
         LEAVE read_loop;
        END IF;

        INSERT INTO dwh_entry_plays_views(entry_id, plays, views)
        SELECT aggr.entry_id, IFNULL(SUM(count_plays), 0) plays, IFNULL(SUM(count_loads), 0) views
        FROM kalturadw.dwh_hourly_events_entry aggr
        WHERE date_id BETWEEN v_date_id AND v_date_id AND hour_id = v_hour_id
        group by entry_id
        ON DUPLICATE KEY UPDATE
        plays = plays + VALUES(plays),
        views = views + VALUES(views),
        updated_at = DATE(20000101);
    END LOOP read_loop;
    CLOSE c_partitions;

    UPDATE dwh_entry_plays_views p, dwh_dim_entries e
    SET p.updated_at = e.operational_measures_updated_at
    WHERE e.entry_id = p.entry_id;

END&&

DELIMITER ;

call calc_plays_views();

DROP PROCEDURE IF EXISTS calc_plays_views;