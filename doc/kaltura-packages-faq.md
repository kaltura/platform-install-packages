# Frequently Asked Questions

### Before You Get Started Notes
* If you see a `#` at the beginning of a line, this line should be run as `root`.

### Commercial Editions and Paid Support

The Open Source Kaltura Platform is provided under the [AGPLv3 license](http://www.gnu.org/licenses/agpl-3.0.html) and with no commercial support or liability.  

[Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.

### How to contribute
We value contributions from our CE user base very much. To make a contribution, follow the [See our CONTRIBUTERS doc](https://github.com/kaltura/platform-install-packages/blob/IX-9.19.0/doc/CONTRIBUTERS.md).


### Changing Apache configurations post install.

Sometimes, you may want to change deployment settings post installation, for example: replacing the domain, port or protocol, or changing the system to use SSL or stop using SSL.   
You can run `/opt/kaltura/bin/kaltura-front-config.sh` as many times as you'd like with different values. The script will re-configure the system accordingly.   
For instance, you may want to change the service URL, port or protocol.

#### For RPM packages:
Edit the answers file you've used to install Kaltura, then run:   
`# /opt/kaltura/bin/kaltura-front-config.sh /path/to/updated/ans/file`

If you've lost your installation answers file, you can recreate one using the [Kaltura Install Answers File Example](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura.template.ans).

#### For deb packages:
```
# dpkg-reconfigure kaltura-base
# dpkg-reconfigure kaltura-front
# dpkg-reconfigure kaltura-batch
```

In addition, when changing the CDN hostname, the kaltura.delivery_profile table must be updated.
```
# mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME

mysql> select id,name,url,host_name from delivery_profile;
```
Then use update statements to reset the url and hostname.


### Deploy Local Repository for Offline Install

On rare ocaasions, you may encounter the need to deploy Kaltura on an offline environment where internet connection is not available, and thus you can't reach the Kaltura packages install repository (http://installrepo.kaltura.org/releases/).

On such cases, the solution is to download the packages, deploy a local repository and install from it instead of the online repository.   
**Note** that when following this path, you will need to re-deploy your local repository for every new version upgrade.

To perform an offline install, follow the [Deploy Local Repository for Offline Install guide](https://github.com/kaltura/platform-install-packages/blob/master/doc/deploy-local-rpm-repo-offline-install.md).

### Fresh Database Installation

On occasions where you'd like to drop the database and content and re-install Kaltura. Follor the below commands:    
```bash
# /opt/kaltura/bin/kaltura-drop-db.sh
# /opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```

### Troubleshooting Help


#### General troubleshoot procedure

Increase log verbosity to 7 using the following method.        
Run the following command:    
```bash
# sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' /opt/kaltura/app/configurations/logger.ini
```
Then restart your Apache.    

Run `# kaltlog`, which will continuously track (using `tail`) an error grep from all Kaltura log files.

You can also use: `# allkaltlog` (using root), which will dump all the error lines from the Kaltura logs once. Note that this can result in a lot of output, so the best way to use it will be to redirect to a file: `# allkaltlog > errors.txt`.
This output can be used to analyze past failures but for active debugging use the kaltlog alias.   

### Analytics issues

#### General Flow
- When a user hits play, an API request similar to the below [service=stats&action=collect], is made by the player:
```
 api_v3/index.php?service=stats&apiVersion=3.1&expiry=86400&clientTag=kwidget%3Av2.53.2&format=1&ignoreNull=1&action=collect&event:eventType=3&event:clientVer=2.53.2&event:currentPoint=0&event:duration=29&event:eventTimestamp=1488213859683&event:isFirstInSession=false&event:objectType=KalturaStatsEvent&event:partnerId=102&event:sessionId=1b92c640-b6de-3e22-4736-0755706220d7&event:uiconfId=23448199&event:seek=false&event:entryId=0_wl3vd05h&event:historyEvents=111000000000000000000000-3-3&event:widgetId=_102&event
```
- This in turn is recorded in the Apache access log for the Kaltura VHost [/opt/kaltura/log/kaltura_apache_access.log]
- The access logs from each front node are then rotated to /opt/kaltura/web/logs using /etc/logrotate.d/kaltura_apache, in particular:
```
/opt/kaltura/log/kaltura_apache_access.log {
 rotate 5
 daily
 missingok
 compress
 dateext
 notifempty
 lastaction
 mv /opt/kaltura/log/kaltura_apache_access.log-`/bin/date +%Y%m%d`.gz /opt/kaltura/web/logs/`hostname`-kaltura_apache_access.log-`/bin/date +%Y%m%d-%H`.gz
 service httpd reload
 endscript
 su root kaltura
}
```
- On the DWH machine, the relevant scripts are run by crond, because of this file: /etc/cron.d/kaltura-dwh
- As a first step, the following config file is looked at /opt/kaltura/dwh/.kettle/kettle.properties, in it, the path to the log dir and the pattern to look for are defined like so:
```
EventsLogsDir = /opt/kaltura/web/logs
EventsWildcard = .*kaltura.*_access.*.log-.*
``` 

In summary, when troubleshooting Analytics issues:
- Make sure /opt/kaltura/web/logs exist on the NFS
- Make sure the volume is mounted on all front and batch machines and that at least /opt/kaltura/web/logs is mounted on the DWH machine [it does not need the other dirs though you can mount the entire volume]
- Make sure /etc/logrotate.d/kaltura_apache exists on all front machines and the access log files are rotated

*Note that analytics are not updated in real time but rather processed by running the cron jobs defined here /etc/cron.d/kaltura-dwh*

#### Troubleshooting Analytics Issues

check if a process lock is stuck:
```
mysql> select * from kalturadw_ds.locks ;
```
if lock_state says 1 for any of these, make sure you have no stuck dwh procs running, update it to read 0 and retry.

check if access files were processed:
```
mysql> select * from kalturadw_ds.files where insert_time >=%Y%m%d;
```
check if actual data about entries play and views was inserted:
```
mysql> select * from kalturadw.dwh_fact_events where event_date_id >=%Y%m%d ;
```

Try to run each step manually:
```
# rm /opt/kaltura/dwh/logs/*
# logrotate -vvv -f /etc/logrotate.d/kaltura_apache
# su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_hourly.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
# su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_update_dims.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
# su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_daily.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
# su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_perform_retention_policy.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
# su kaltura -c "/opt/kaltura/app/alpha/scripts/dwh/dwh_plays_views_sync.sh >> /opt/kaltura/log/cron.log"
```

Or use the wrapper script to run all steps:
```
/opt/kaltura/bin/kaltura-run-dwh.sh
```

In order to remove the Analytics DBs and repopulate them:

0. Backup all Kaltura DBs using: https://github.com/kaltura/platform-install-packages/blob/Jupiter-10.2.0/doc/rpm-cluster-deployment-instructions.md#backup-and-restore-practices 
1. Drop the current DWH DBs: 
```
PASSW=$MYSQL_SUPER_USER_PASSWD 
for i in `mysql -N -p$PASSWD kalturadw -e "show tables"`;
do mysql -p$PASSWD kalturadw -e "drop table $i";done 
for i in `mysql -N -p$PASSWD kalturadw_ds -e "show tables"`;do mysql -p$PASSWD kalturadw_ds -e "drop table $i";done 
for i in `mysql -N -p$PASSWD kalturalog -e "show tables"`;do mysql -p$PASSWD kalturalog -e "drop table $i";done 
for i in `mysql -p$PASSWD -e "Show procedure status" |grep kalturadw|awk -F " " '{print $2}'`;do mysql kalturadw -p$PASSWD -e "drop procedure $i;";done 
for i in `mysql -p$PASSWD -e "Show procedure status" |grep kalturadw_ds|awk -F " " '{print $2}'`;do mysql kalturadw_ds -p$PASSWD -e "drop procedure $i;";done 
```

2. Reinstall and config DWH

on RPM based systems:
```
# yum reinstall kaltura-dwh 
# kaltura-dwh-config.sh
```

on deb based systems:
```
# dpkg-reconfigure kaltura-dwh
``` 

#### Couldn't execute SQL: CALL move_innodb_to_archive()
Running:
```
mysql> call kalturadw.add_partitions();
```
Should resolve the issue.

#### Table has no partition for value

- verify that your DB timezone settings are the same as PHP timezone settings (php.ini)
- Re-sync dimension tables from the day you installed your server:
    - Update kalturadw_ds.parameters where parameter_name = 'dim_sync_last_update'. You need to set date_value to the date you installed your server.
    - Run /opt/kaltura/dwh/etlsource/execute/etl_update_dims.sh
    -Verify that kalturadw.dwh_dim_entries was populated (If not check /opt/kaltura/dwh/logs/etl_update_dims-YYYTMMDD-HH.log for errors)
- Update kalturadw.aggr_managment to run all aggregation again. Update kalturadw.aggr_managment set data_insert_time = NOW();
- Run /opt/kaltura/dwh/etlsource/execute/etl_daily.sh


### Cannot login to Admin Console
To manually reset the passwd, following this procedure:
mysql> select * from user_login_data where login_email='you@mail.com'\G

Then, update sha1_password and salt to read:
      sha1_password: 44e8c1db328d6d2f64de30a8285fb2a1c9337edb
               salt: a6a3209b8827759fa4286d87a33f99df

This should reset your passwd to 'admin123!'

### kmc is routed to a SSL link
If you try to access /kmc and get routed to https://vod.linnovate.net/index.php/kmc/kmc4 -
(even if you prompted to work in non SSL mode...

run the following commands...
```
  mysql kaltura
  select id from permission WHERE permission.NAME='FEATURE_KMC_ENFORCE_HTTPS';
```
If you get a response use that in the next query
```
  delete from permission where id = NUM_YOU_GOT_ABOVE
```
