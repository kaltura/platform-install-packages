INSERT INTO kalturadw.aggr_managment (aggr_name, aggr_day, hour_id, aggr_day_int, is_calculated)
SELECT DISTINCT 'errors', aggr_day, hour_id, aggr_day_int, IF(aggr_day_int>=date(now())*1,0,1)
FROM kalturadw.aggr_managment;
