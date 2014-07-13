# Frequently Asked Questions

### Before You Get Started Notes
* If you see a `#` at the beginning of a line, this line should be run as `root`.

### Commercial Editions and Paid Support

The Open Source Kaltura Platform is provided under the [AGPLv3 license](http://www.gnu.org/licenses/agpl-3.0.html) and with no commercial support or liability.  

[Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.

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

#### No playback on iOS
This is a known issue resolved in 9.13.0.
However, if your DB was created earlier, the solution is this:


Dump the flavor_asset table as bck with:
```bash
mysqldump -uroot -p flavor_asset > /tmp/flavor_asset.sql
mysql> update flavor_params set tags='mobile,web,mbr,iphone' where id in (2,3);
mysql> update flavor_params set tags='mobile,web,mbr,ipad' where id in (5,6);
mysql> update flavor_params set tags='mbr' where id in (35,34);
mysql> update flavor_asset set tags='mobile,web,mbr,ipad' where tags='mobile,web,mbr,ipad,ipadnew';
mysql> update flavor_asset set tags='mobile,web,mbr,iphone' where tags='mobile,web,mbr,iphone,iphonenew';
```
Entries should now play on iOS.
If something went wrong, restore the original data using:
```bash
mysql -uroot -p < /tmp/flavor_asset.sql
```
#### Creating Distribution profile
We will get the error "The usage of feature [contentDistribution] is forbidden" while creating the distributing profile, unless the feature is enabled in Publicher's configuration settings. Please follow the below steps to enable it and to create a distribution profile.

1. Login to Kaltura Admin Console.
2. In Publishers tab, click on 'Actions' dropdown for a perticular publisher anf select 'Configure' option.
3. Publisher Specific Configuration window will be opened and in 'Enable/Disable Features' section, check the box for 'Content Distribution Module'.
4. Click on 'Save'.
5. Click on 'Profiles' dropdown in Publishers tab, for a perticular publisher and select 'Distribution Profiles'.
6. Select 'Provider' as YoutubeApi or Tvinci or Generic as per the provider and click on 'Create New'.
7. Fill the required information in 'Profile Setup Configuration' window. Eg. for YoutubeApi, provide Youtube user name, password and click on save. Now Distribution Profile is created.
8. Login to KMC and go to the 'Content' tab.
9. Select the 'View Details' option for the desired Vidoe and click on the 'Distribution' option in left side menu.
10. Select the required Distributor.
11. Click on 'Save and Close'
12. We can track the initiated Distribution jobs, in the 'Batch Process Control' tab in Admin Console.

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



