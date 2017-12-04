# Installing Kaltura on a Single Server (RPM)
This guide describes RPM installation of an all-in-one Kaltura server and applies to all major RH based Linux distros including Fedora Core, RHEL, CentOS, etc.
([Note the supported distros and versions](http://kaltura.github.io/platform-install-packages/#supported-distros)).

[Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.

#### Table of Contents
[Prerequites](https://github.com/kaltura/platform-install-packages/blob/master/doc/pre-requisites.md)

[Non-SSL Step-by-step Installation](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#non-ssl-step-by-step-installation)

[SSL Step-by-step Installation](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#ssl-step-by-step-installation)

[Unattended Installation](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#unattended-installation)

[Live Streaming with Nginx and the RTMP module](install-kaltura-redhat-based.md#live-streaming-with-nginx-and-the-rtmp-module)

[Upgrade Kaltura](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#upgrade-kaltura)

[Remove Kaltura](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#remove-kaltura)

[Troubleshooting](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#troubleshooting)

[Additional Information](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#additional-information)

[How to contribute](https://github.com/kaltura/platform-install-packages/blob/master/doc/CONTRIBUTERS.md)

## Non-SSL Step-by-step Installation

### Pre-Install notes
* This install guides assumes that you did a clean, basic install of one of the RHEL based OS's in 64bit architecture.
* When installing, you will be prompted for each server's resolvable hostname. Note that it is crucial that all host names will be resolvable by other servers in the cluster (and outside the cluster for front machines). Before installing, verify that your /etc/hosts file is properly configured and that all Kaltura server hostnames are resolvable in your network.
* Before you begin, make sure you're logged in as the system root. Root access is required to install Kaltura, and you should execute ```sudo -i``` or ```su -```to make sure that you are indeed root.

#### Firewall requirements
Kaltura requires certain ports to be open for proper operation. [See the list of required open ports](kaltura-required-ports.md).
If you're **just testing locally** and don't mind an open system, you can use the below to disbale iptables altogether:
```bash
iptables -F
service iptables stop
chkconfig iptables off
```
#### Set SELinux to permissive mode - REQUIRED
**Currently Kaltura doesn't properly support running with SELinux in ```enforcing``` mode, things will break if you don't set it to permissive**.

```bash
setenforce permissive
```

To verify SELinux will not revert to enabled next restart:

1. Edit the file `/etc/selinux/config`
1. Verify or change the value of SELINUX to permissive: `SELINUX=permissive`
1. Save the file `/etc/selinux/config`

### Start of Kaltura installation
This section is a step-by-step guide of a Kaltura installation without SSL.

#### Setup the Kaltura RPM repository

```bash
rpm -ihv http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
```

## Note on RHEL/CentOS 7 
Depending on what repos you have enabled, you may also need to add the EPEL or CentOS repos to resolve all dependencies.

#### Installing on AWS EC2 instances
Depending on your setup, you may need to enable two additional repos: rhui-REGION-rhel-server-extras and rhui-REGION-rhel-server-optional.
This can be done by editing /etc/yum.repos.d/redhat-rhui.repo and changing:
```
enabled=0
```
to:
```
enabled=1
```
under the following sections:
```
rhui-REGION-rhel-server-optional
rhui-REGION-rhel-server-extras
```

Or by running the following commands:
```
# yum -y install yum-utils
# yum-config-manager --enable rhui-REGION-rhel-server-extras rhui-REGION-rhel-server-optional
```

#### Enabling the EPEL repo
To add the EPEL repo:
```
# rpm -ihv https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
```


#### MySQL Install and Configuration
For MySQL versions higher 5.5 and above, note that you must disable strict mode for the deployment to succeed.
Please see the following document:
https://dev.mysql.com/doc/refman/5.5/en/sql-mode.html#sql-mode-setting

RHEL/CentOS 6 setup:
```bash
yum install mysql-server
service mysqld start
mysql_secure_installation
chkconfig mysqld on
```

RHEL/CentOS 7 setup:
```bash
yum install mariadb-server
service mariadb start
mysql_secure_installation
chkconfig mariadb on
```

**Make sure to answer YES for all steps in the `mysql_secure_install` install, and follow through all the mysql install questions before continuing further.
Failing to properly run `mysql_secure_install` will cause the kaltura mysql user to run without proper permissions to access your mysql DB, and require you to start over again.

#### Mail Server (MTA) Install and Configuration
If your machine doesn't have postfix email configured before the Kaltura install, you will not receive emails from the install system nor publisher account activation mails.
If postfix runs without further configuration starting it is sufficient to make Kaltura work.
```bash
service postfix restart
```

If you are using Amazon Web Services (AWS) please note that by default EC2 machines are blocked from sending email via port 25. For more information see [this thread on AWS forums](https://forums.aws.amazon.com/message.jspa?messageID=317525#317525).

##### Note regarding desktop installations

When installing on a "desktop" environment there may be package conflicts with media encoding/decoding plugins.

In Redhat 6.5 you should run the following to remove the conflicting packages:
`rpm -e gstreamer-plugins-bad-free totem totem-nautilus`

#### Install Kaltura Server

Install the basic Kaltura Packages:
```bash
yum clean all
yum install kaltura-server
```

Configure MySQL with the required Kaltura Settings
```bash
/opt/kaltura/bin/kaltura-mysql-settings.sh
```

Start required service and configure them to run at boot:
```bash
service memcached restart
service ntpd restart
chkconfig memcached on
chkconfig ntpd on
```

### Start of Kaltura Configuration
```bash
/opt/kaltura/bin/kaltura-config-all.sh
```

The below is a sample question answer format, replace the input marked by <> with your own details:

```bash
[Email\NO]: "<your email address>"
CDN hostname [kalrpm.lcl]: "<your hostname>"
Apache virtual hostname [kalrpm.lcl]: "<your hostname>"
Which port will this Vhost listen on [80]?:

DB hostname [127.0.0.1]: "<127.0.0.1>"
DB port [3306]: "<3306>"
MySQL super user [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "<root>"
MySQL super user passwd [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "<your root password>"
Analytics DB hostname [127.0.0.1]: "<127.0.0.1>"
Analytics DB port [3306]: "<3306>"
Sphinx hostname [127.0.0.1]: "<127.0.0.1>"

Secondary Sphinx hostname: [leave empty if none] "<empty>"

VOD packager hostname [kalrpm.lcl]: "<http://kaltura-nginx-hostname>"

VOD packager port to listen on [88]: 

Service URL [http://kalrpm.lcl:80]: "<http://apache-hostname:80>"

Kaltura Admin user (email address): "<your email address>"
Admin user login password (must be minimum 8 chars and include at least one of each: upper-case, lower-case, number and a special character): "<your kaltura admin password>"
Confirm passwd: "<your kaltura admin password>"

Your time zone [see http://php.net/date.timezone], or press enter for [Europe/Amsterdam]: "<your timezone>"
How would you like to name your system (this name will show as the From field in emails sent by the system) [Kaltura Video Platform]? "<your preferred system name>"
Your website Contact Us URL [http://corp.kaltura.com/company/contact-us]: "<your contact URL>"
'Contact us' phone number [+1 800 871 5224]? "<your phone numer>"

Is your Apache working with SSL?[Y/n] "<n>"
It is recommended that you do work using HTTPs. Would you like to continue anyway?[N/y] "<y>"
Which port will this Vhost listen on? [80] "<80>"
Please select one of the following options [0]: "<0>"
```

Your install will now automatically perform all install tasks.



**Your Kaltura installation is now complete.**

## SSL Step-by-step Installation
### Pre-Install notes
* This install guides assumes that you did a clean, basic install of one of the support RHEL based OS's in 64bit architecture.
* Currently, the Nginx VOD module does not support integration with Kaltura over HTTPs, only HTTP is supported. 
* When installing, you will be prompted for each server's resolvable hostname. Note that it is crucial that all host names will be resolvable by other servers in the cluster (and outside the cluster for front machines). Before installing, verify that your /etc/hosts file is properly configured and that all Kaltura server hostnames are resolvable in your network.
* Before you begin, make sure you're logged in as the system root. Root access is required to install Kaltura, and you should execute ```sudo -i``` or ```su -``` to make sure that you are indeed root.
* It is recommended that you use a properly signed certificate and avoid self-signed certificates due to limitations of various browsers in properly loading websites using self-signed certificates.
  * You can generate a free valid cert using [http://cert.startcom.org/](http://cert.startcom.org/).
  * To verify the validity of your certificate, you can then use [SSLShoper's SSL Check Utility](http://www.sslshopper.com/ssl-checker.html).

#### Firewall requirements
Kaltura requires certain ports to be open for proper operation. [See the list of required open ports](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-required-ports.md).
If you're just testing and don't mind an open system, you can use the below to disbale iptables altogether:
```bash
iptables -F
service iptables stop
chkconfig iptables off
```
#### Disable SELinux - REQUIRED
**Currently Kaltura doesn't properly support running with SELinux, things will break if you don't set it to permissive**.

```bash
setenforce permissive
```

To verify SELinux will not revert to enabled next restart:

1. Edit the file `/etc/selinux/config`
1. Verify or change the value of SELINUX to permissive: `SELINUX=permissive`
1. Save the file `/etc/selinux/config`

### Start of Kaltura installation
This section is a step-by-step guide of a Kaltura installation with SSL.

#### Setup the Kaltura RPM repository

```bash
rpm -ihv http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
```



#### MySQL Install and Configuration
Please note that currently, only MySQL 5.1 is supported, we recommend using the official package supplied by the RHEL/CentOS repos which is currently 5.1.73.

For RHEL/CentOS 7, MariaDB version 5.5.40 is supported. 

RHEL/CentOS 6 setup:
```bash
yum install mysql mysql-server
service mysqld start
mysql_secure_installation
chkconfig mysqld on
```

RHEL/CentOS 7 setup:
```bash
yum install mariadb-server
service mariadb start
mysql_secure_installation
chkconfig mariadb on
```

**Make sure to answer YES for all steps in the `mysql_secure_install` install, and follow through all the mysql install questions before continuing further.
Failing to properly run `mysql_secure_install` will cause the kaltura mysql user to run without proper permissions to access your mysql DB, and require you to start over again.

#### Mail Server (MTA) Install and Configuration
If your machine doesn't have postfix email configured before the Kaltura install, you will not receive emails from the install system nor publisher account activation mails.
If postfix runs without further configuration starting it is sufficient to make Kaltura work.
```bash
service postfix restart
```

If you are using Amazon Web Services (AWS) please note that by default EC2 machines are blocked from sending email via port 25. For more information see [this thread on AWS forums](https://forums.aws.amazon.com/message.jspa?messageID=317525#317525).

#### Install Kaltura Server

Note: prior to installing Kaltura, while not a must, we recommend you update the installed packages to latest by running:
```bash
yum update
```

Install the basic Kaltura Packages:
```bash
yum clean all
yum update "*kaltura*" 
yum install kaltura-server
```

Configure MySQL with the required Kaltura Settings
```bash
/opt/kaltura/bin/kaltura-mysql-settings.sh
```

Start required service and configure them to run at boot:
```bash
service memcached restart
service ntpd restart
chkconfig memcached on
chkconfig ntpd on
```

### Start of Kaltura Configuration
```bash
/opt/kaltura/bin/kaltura-config-all.sh
```

The below is a sample question answer format, replace the input marked by <> with your own details:

```bash
[Email\NO]: "<your email address>"
CDN hostname [kalrpm.lcl]: "<your hostname>"
Apache virtual hostname [kalrpm.lcl]: "<your hostname>"
Which port will this Vhost listen on [80]?: "<443>"

DB hostname [127.0.0.1]: "<127.0.0.1>"
DB port [3306]: "<3306>"
MySQL super user [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "<root>"
MySQL super user passwd [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "<your root password>"
Analytics DB hostname [127.0.0.1]: "<127.0.0.1>"
Analytics DB port [3306]: "<3306>"
Sphinx hostname [127.0.0.1]: "<127.0.0.1>"

Secondary Sphinx hostname: [leave empty if none] "<empty>"

VOD packager hostname [kalrpm.lcl]: "<http://kaltura-nginx-hostname>"

VOD packager port to listen on [88]: 

Service URL [http://kalrpm.lcl:443]: "<http://your-hostname:443>"

Kaltura Admin user (email address): "<your email address>"
Admin user login password (must be minimum 8 chars and include at least one of each: upper-case, lower-case, number and a special character): "<your kaltura admin password>"
Confirm passwd: "<your kaltura admin password>"

Your time zone [see http://php.net/date.timezone], or press enter for [Europe/Amsterdam]: "<your timezone>"
How would you like to name your system (this name will show as the From field in emails sent by the system) [Kaltura Video Platform]? "<your preferred system name>"
Your website Contact Us URL [http://corp.kaltura.com/company/contact-us]: "<your contact URL>"
'Contact us' phone number [+1 800 871 5224]? "<your phone numer>"

Is your Apache working with SSL?[Y/n]: "<Y>"
Please input path to your SSL certificate: "</path/to/my/ssl/certificate>"
Please input path to your SSL key: "</path/to/my/ssl/key>"
Please input path to your SSL chain file or leave empty in case you have none: "</path/to/my/ssl/chainfile>"
Which port will this Vhost listen on? [443] "<443>"
Please select one of the following options [0]: "<0>"
```

Your install will now automatically perform all install tasks.

### Live Streaming with Nginx and the RTMP module
Kaltura CE includes the kaltura-nginx package, which is compiled with the [Nginx RTMP module](https://github.com/arut/nginx-rtmp-module).

Please see documentation here [nginx-rtmp-live-streaming.md](nginx-rtmp-live-streaming.md)

A longer post about it can be found at https://blog.kaltura.com/free-and-open-live-video-streaming


### SSL Certificate Configuration

Set the following directives in `/etc/httpd/conf.d/zzzkaltura.ssl.conf`:
```
SSLCertificateChainFile
SSLCACertificateFile
```

To use the [monit](http://mmonit.com/monit/) Monitoring tab in admin console, you will need to also configure the SSL certificate for monit.
To use the same certificate as you used for Kaltura they will need to be in PEM format. If it is not see [Generate PEM Instructions](http://www.digicert.com/ssl-support/pem-ssl-creation.htm)

Edit: `/opt/kaltura/app/configurations/monit/monit.conf` and add:
```
SSL ENABLE
PEMFILE /path/to/your/certificate.pem
```

Finally, run: ```/etc/init.d/kaltura-monit restart```

**Your Kaltura installation is now complete.**

## Unattended Installation
All Kaltura scripts accept an answer file as their first argument.
In order to preform an unattended [silent] install, simply edit the [template](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura.template.ans) and pass it along to kaltura-config-all.sh.

## Upgrade Kaltura
*This will only work if the initial install was using this packages based install, it will not work for old Kaltura deployments using the PHP installers*
```bash
# rpm -Uhv http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
# yum clean all
# yum update "*kaltura*"
```
Then follow the on-screen instructions (in case any further actions required).
Once the upgrade completes, please run:
```bash
/opt/kaltura/bin/kaltura-config-all.sh
```

/opt/kaltura/bin/kaltura-config-all.sh can accept an answer file as its first argument, allowing for an unattended deployment/upgrade.
For more on that, see: https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura.template.ans 

In the event you would like to see what changes the package includes before deciding whether or not you wish to upgrade, run:
```bash
yum install yum-plugin-changelog
yum changelog all kaltura-package-name-here
```

## Remove Kaltura
Use this in cases where you want to clear the database and start from fresh.
```bash
/opt/kaltura/bin/kaltura-drop-db.sh
yum remove "*kaltura*"
rm -rf /opt/kaltura
```

## Troubleshooting
Once the configuration phase is done, you may wish to run the sanity tests, for that, run:
```base
/opt/kaltura/bin/kaltura-sanity.sh
```

If you experience unknown, unwanted or erroneous behaviour, the logs are a greta place to start, to get a quick view into errors and warning run:
```bash
kaltlog
```

If this does not give enough information, increase logging verbosity:
```bash
sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' /opt/kaltura/app/configurations/logger.ini
```

To revert this logging verbosity run:
```bash
sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*4@writers.\1.filters.priority.priority=7@g' /opt/kaltura/app/configurations/logger.ini
```

Or output all logged information to a file for analysis:
```bash
allkaltlog > /path/to/mylogfile.log
```

For posting questions, please go to:
(http://forum.kaltura.org)

## Additional Information
* Please review the [frequently answered questions](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-packages-faq.md) document for general help before posting to the forums or issue queue.
* This guide describes the installation and upgrade of an all-in-one machine where all the Kaltura components are installed on the same server. For cluster deployments, please refer to [cluster deployment document](http://bit.ly/kipp-cluster-yum), or [Deploying Kaltura using Opscode Chef](https://github.com/kaltura/platform-install-packages/blob/master/doc/rpm-chef-cluster-deployment.md).
* To learn about monitoring, please refer to [configuring platform monitors](http://bit.ly/kipp-monitoring).
* Testers using virtualization: [@DBezemer](https://github.com/kaltura) created a basic CentOS 6.4 template virtual server vailable here in OVF format: https://www.dropbox.com/s/luai7sk8nmihrkx/20140306_CentOS-base.zip
* Alternatively you can find VMWare images at - https://www.osboxes.org/vmware-images --> Make sure to only use compatible OS images; either RedHat or CentOS 5.n, 6.n or FedoraCore 18+.
* Two working solutions to the AWS EC2 email limitations are:
  * Using SendGrid as your mail service ([setting up ec2 with Sendgrid and postfix](http://www.zoharbabin.com/configure-ssmtp-or-postfix-to-send-email-via-sendgrid-on-centos-6-3-ec2)).
  * Using [Amazon's Simple Email Service](http://aws.amazon.com/ses/).
* [Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.
