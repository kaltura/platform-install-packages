USE kalturadw;

CREATE TABLE dwh_entry_plays_views_20120812 LIKE dwh_entry_plays_views;
INSERT INTO dwh_entry_plays_views_20120812 SELECT * FROM dwh_entry_plays_views;

DROP TABLE IF EXISTS tmp_pv;
CREATE TEMPORARY TABLE tmp_pv
SELECT * FROM (SELECT entry_id, IFNULL(SUM(count_plays),0) p , IFNULL(SUM(count_loads),0) v
FROM kalturadw.dwh_hourly_events_entry
GROUP BY entry_id
UNION 
SELECT * FROM entry_plays_views_before_08_2009) tmp;

ALTER TABLE tmp_pv ADD INDEX entry_id (entry_id);

UPDATE dwh_entry_plays_views op_pv 
LEFT OUTER JOIN tmp_pv ON op_pv.entry_id = tmp_pv.entry_id
SET op_pv.views = IFNULL(tmp_pv.v,0),
	op_pv.updated_at = NOW()
WHERE IFNULL(op_pv.views,0) <> IFNULL(tmp_pv.v, 0);



