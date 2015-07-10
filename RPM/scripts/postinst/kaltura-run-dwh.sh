#!/bin/sh
rm /opt/kaltura/dwh/logs/*
logrotate -vvv -f /etc/logrotate.d/kaltura_apache
su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_hourly.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_update_dims.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_daily.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_perform_retention_policy.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
su kaltura -c "/opt/kaltura/app/alpha/scripts/dwh/dwh_plays_views_sync.sh >> /opt/kaltura/log/cron.log"
