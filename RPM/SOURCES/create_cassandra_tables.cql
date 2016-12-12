CREATE KEYSPACE IF NOT EXISTS kaltura_live WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

use kaltura_live;

CREATE TABLE IF NOT EXISTS kaltura_live.current_batch (
    batch_code bigint PRIMARY KEY,
	batch_id bigint);

insert into current_batch (batch_code, batch_id) VALUES ( 0,0);

CREATE TABLE IF NOT EXISTS kaltura_live.log_files (
    file_id text,
    insert_time timestamp,
    batch_id bigint,
    PRIMARY KEY (file_id, insert_time)
)
WITH CLUSTERING ORDER BY (insert_time DESC);

CREATE INDEX log_files_batch_id
 ON log_files (batch_id);

CREATE TABLE IF NOT EXISTS kaltura_live.log_data (
	file_id text PRIMARY KEY,
	data blob);

CREATE TABLE IF NOT EXISTS kaltura_live.live_events (
	entry_id text,
	event_time timestamp,
	plays counter,
	alive counter,
	dvr_alive counter,
	bitrate counter,
	bitrate_count counter,
	buffer_time counter,
	PRIMARY KEY (entry_id,event_time)
)
WITH CLUSTERING ORDER BY (event_time DESC);

CREATE TABLE IF NOT EXISTS kaltura_live.hourly_live_events (
	entry_id text,
	event_time timestamp,
	plays counter,
	alive counter,
	dvr_alive counter,
	bitrate counter,
	bitrate_count counter,
	buffer_time counter,
	PRIMARY KEY (entry_id,event_time)
)
WITH CLUSTERING ORDER BY (event_time DESC);

CREATE TABLE IF NOT EXISTS kaltura_live.live_events_location (
	entry_id text,
	event_time timestamp,
	country text,
	city text,
	plays counter,
	alive counter,
	dvr_alive counter,
	bitrate counter,
	bitrate_count counter,
	buffer_time counter,
	PRIMARY KEY ((entry_id,event_time), country, city));

CREATE TABLE IF NOT EXISTS kaltura_live.hourly_live_events_partner (
	partner_id int,
	event_time timestamp,
	plays counter,
	alive counter,
	dvr_alive counter,
	bitrate counter,
	bitrate_count counter,
	buffer_time counter,
	PRIMARY KEY (partner_id,event_time)
)
WITH CLUSTERING ORDER BY (event_time DESC);

CREATE TABLE IF NOT EXISTS kaltura_live.hourly_live_events_referrer (
	entry_id text,
	event_time timestamp,
	referrer text,
	plays counter,
	alive counter,
	dvr_alive counter,
	bitrate counter,
	bitrate_count counter,
	buffer_time counter,
	PRIMARY KEY ((entry_id,event_time), referrer));

CREATE TABLE IF NOT EXISTS kaltura_live.live_partner_entry (
	partner_id int,
	entry_id text,
	event_time timestamp,
	PRIMARY KEY (partner_id, entry_id));

CREATE TABLE IF NOT EXISTS kaltura_live.live_entry_hourly_peak (
	entry_id text,
	event_time timestamp,
	audience bigint,
	dvr_audience bigint,
        update_time timestamp,
	PRIMARY KEY (entry_id, event_time)
)
WITH CLUSTERING ORDER BY (event_time DESC);
