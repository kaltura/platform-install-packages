USE kalturadw;

DROP TABLE IF EXISTS dwh_dim_hours;

CREATE TABLE `dwh_dim_hours` (
  hour_id INT
) ENGINE=MYISAM DEFAULT CHARSET=latin1;

INSERT INTO dwh_dim_hours 
VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15), (16), (17), (18), (19), (20), (21), (22), (23);
