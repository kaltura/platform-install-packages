# Setting up Kaltura platform monitoring

### Before You Get Started Notes

* If you see a `#` at the beginning of a line, this line should be run as `root`.
* Please review the [frequently answered questions](kaltura-packages-faq.md) document for general help before posting to the forums or issue queue.
* [Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.

### Using JaM - a PHP monitoring system that supports storing PHP errors (events) into different storage backends
JaM packages are available in the Kaltura CE repository, for instructions see:
https://github.com/kaltura/jam#basic-setup

### Kaltura specific monitors
The Kaltura server includes extensive monitoring scripts, making use of our PHP5 API.   
Apart from the scripts themselves, template configuration files for the Nagios monitoring system [http://www.nagios.com] are also supplied.   
The monitors operate on partner -4, created as part of the installation and dedicated to this purpose.   

* The configuration for the API monitors is auto generated and placed here:
`/opt/kaltura/app/tests/monitoring/config.ini`
* The nagios templates can be found here:
`/opt/kaltura/app/plugins/monitor/nagios/config/`

If you wish to use the monitors with a monitoring system different than Nagios, it is very easy.   
Simple adopt the commands available here: 
`/opt/kaltura/app/plugins/monitor/nagios/config/commands.cfg`    
And make similar configurations for your monitoring system.    

All these monitors can run equally as well from the shell so they can also be placed as cron jobs.   

For example:   
```bash
# php /opt/kaltura/app/plugins/monitor/nagios/exec.php --error-threshold 0 --script "/opt/kaltura/app/tests/monitoring/dwh/lockedProcesses.php --daily
All processes released
```

```bash
# /usr/bin/php /opt/kaltura/app/plugins/monitor/nagios/exec.php --warning-threshold 1 --error-threshold 2 --script "/opt/kaltura/app/tests/monitoring/
Multi-request execution time: 0.27060580253601 seconds
```

```bash
# /usr/bin/php /opt/kaltura/app/plugins/monitor/nagios/exec.php --script "/opt/kaltura/app/tests/monitoring/db/sphinxIntegrity.php --hostname amdb --time-offset 3600 --
3 Tag objects changed, updated in the log and in the sphinx
```

In addition, the platform utilizes [Monit](http://mmonit.com/monit) as a watchdog for its daemons, you can see the status in the Admin Console, under the 'Monitoring' tab.
