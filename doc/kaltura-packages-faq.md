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

Edit the answers file you've used to install Kaltura, then run:   
`# /opt/kaltura/bin/kaltura-front-config.sh /path/to/updated/ans/file`

If you've lost your installation answers file, you can recreate one using the [Kaltura Install Answers File Example](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura.template.ans).

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

#### Analytics issues
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
rm /opt/kaltura/dwh/logs/*
logrotate -vvv -f /etc/logrotate.d/kaltura_apache
su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_hourly.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_update_dims.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_daily.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
su kaltura -c "/opt/kaltura/dwh/etlsource/execute/etl_perform_retention_policy.sh -p /opt/kaltura/dwh -k /opt/kaltura/pentaho/pdi/kitchen.sh"
su kaltura -c "/opt/kaltura/app/alpha/scripts/dwh/dwh_plays_views_sync.sh >> /opt/kaltura/log/cron.log"
```

In order to remove the Analytics DBs and repopulate them:

0. Backup all Kaltura DBs using: https://github.com/kaltura/platform-install-packages/blob/Jupiter-10.2.0/doc/rpm-cluster-deployment-instructions.md#backup-and-restore-practices 
1. Drop the current DWH DBs: 
```
PASSW=$MYSQL_SUPER_USER_PASSWD for i in `mysql -N -p$PASSWD kalturadw -e "show tables"`;do mysql -p$PASSWD kalturadw -e "drop table $i";done for i in `mysql -N -p$PASSWD kalturadw_ds -e "show tables"`;do mysql -p$PASSWD kalturadw_ds -e "drop table $i";done for i in `mysql -N -p$PASSWD kalturalog -e "show tables"`;do mysql -p$PASSWD kalturalog -e "drop table $i";done for i in `mysql -p$PASSWD -e "Show procedure status" |grep kalturadw|awk -F " " '{print $2}'`;do mysql kalturadw -p$PASSWD -e "drop procedure $i;";done for i in `mysql -p$PASSWD -e "Show procedure status" |grep kalturadw_ds|awk -F " " '{print $2}'`;do mysql kalturadw_ds -p$PASSWD -e "drop procedure $i;";done 
```

2. Reinstall and config DWH:
```
# yum reinstall kaltura-dwh 
# kaltura-dwh-config.sh
```

#### Cannot login to Admin Console
To manually reset the passwd, following this procedure:
mysql> select * from user_login_data where login_email='you@mail.com'\G

Then, update sha1_password and salt to read:
      sha1_password: 44e8c1db328d6d2f64de30a8285fb2a1c9337edb
               salt: a6a3209b8827759fa4286d87a33f99df

This should reset your passwd to 'admin123!'
