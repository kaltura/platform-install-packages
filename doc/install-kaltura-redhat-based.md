# Installing Kaltura on a Single All-In-One Server (RPM)
This guide describes installation of an all-in-one Kaltura server and applies to all major RH based Linux distros including Fedora Core, RHEL, CentOS, etc. ([Note the supported distros and versions](http://kaltura.github.io/platform-install-packages/#supported-distros)).       

##### Notes

* Please review the [frequently answered questions](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-packages-faq.md) document for general help before posting to the forums or issue queue.
* This guide describes the installation and upgrade of an all-in-one machine where all the Kaltura components are installed on the same server. For cluster deployments, please refer to [cluster deployment document](http://bit.ly/kipp-cluster-yum), or [Deploying Kaltura using Opscode Chef](https://github.com/kaltura/platform-install-packages/blob/master/doc/rpm-chef-cluster-deployment.md).
* To learn about monitoring, please refer to [configuring platform monitors](http://bit.ly/kipp-monitoring).
* Testers using virtualization: [@DBezemer](https://github.com/DBezemer) created a basic CentOS template virtual server vailable here in OVF format: https://www.dropbox.com/s/luai7sk8nmihrkx/20140306_CentOS-base.zip
* Alternatively you can find VMWare images at - http://www.thoughtpolice.co.uk/vmware/ --> Make sure to only use compatible OS images; either RedHat or CentOS 5.n, 6.n or FedoraCore 18+.
* [Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.

## Installing on a new machine

##### Pre-Install notes

* **Resolveable host names** - When installing, you will be promopted for each server's resolvable hostname. Note that it is crucial that all host names will be resolveable by other servers in the cluster (and outside the cluster for front machines). Before installing, verify the /etc/hosts file is properly configured and that all Kaltura server hostnames are resolveable in your network.
* **ROOT is REQUIRED** - Before you begin, make sure you're logged in as the system root. root access is required to install Kaltura. ```sudo su - ```

##### iptables and ports
Kaltura requires certain ports to be open for proper operation. [See the list of required open ports](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-required-ports.md).   
If you're just testing and don't mind an open system, you can use the below to disbale iptables altogether:
```bash
iptables -F
chkconfig iptables off
```
##### Disable SELinux - REQUIRED (currently Kaltura can't run properly with SELinux)
```bash 
setenforce permissive
# To verify SELinux will not revert to enabled next restart:
# Edit /etc/selinux/config
# Set SELINUX=permissive
# Save /etc/selinux/config
```
##### Auto Set the Kaltura install repository URLs 

```bash
rpm -ihv http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
```

This will enable the stable repo, to enable the nightly one in addition to it, please run:
```bash   
yum install yum-utils
yum-config-manager --enable Kaltura-testing-noarch
yum-config-manager --enable Kaltura-testing
```
Alternatively, you can just edit /etc/yum.repos.d/kaltura.repo directly and set 'enabled=1' on the testing repos.

##### Note about SSL certificates

You can run Kaltura with or without SSL (state the correct protocol and certificates during the installation).  
It is recommended that you use a properly signed certificate and avoid self-signed certificates due to limitations of various browsers in properly loading websites using self-signed certificates.    
You can generate a free valid cert using [http://cert.startcom.org/](http://cert.startcom.org/).    
To verify the validity of your certificate, you can then use [SSLShoper's SSL Check Utility](http://www.sslshopper.com/ssl-checker.html).  

Depending on your certificate, you may also need to set the following directives in `/etc/httpd/conf.d/zzzkaltura.ssl.conf`: 
```
SSLCertificateChainFile
SSLCACertificateFile
```

To use the [monit](http://mmonit.com/monit/) Monitoring tab in admin console, you will need to also configure the SSL certificate for monit. Run the following using root:
```bash
/usr/bin/openssl req -new -x509 -days 365 -nodes -out /opt/kaltura/app/configurations/monit.pem -keyout /opt/kaltura/app/configurations/monit.pem
chmod 600 /opt/kaltura/app/configurations/monit.pem
/usr/bin/openssl gendh 512 >> /opt/kaltura/app/configurations/monit.pem
```
Then edit: `/opt/kaltura/app/configurations/monit/monit.conf`    
And add:
```
SSL ENABLE
PEMFILE /opt/kaltura/app/configurations/monit.pem
ALLOWSELFCERTIFICATION
```
Finally, run: `/etc/init.d/kaltura-monit restart`

##### Install the Kaltura Packages
```bash
yum clean all
yum install kaltura-server
# enable daemons at init:
# The memcache and ntp RPMs used by Kaltura server are taken from the official disto's repo. 
# Unfortuantely, the postinst scripts for these packages do not set it to start at init time.
# To set this up:
chkconfig memcached on
chkconfig ntpd on
```

##### Install and configure MySQL 5.1.n (if you’re going to use DB on the same server)
Please note that currently, only MySQL 5.1 is supported, we recommend using the official package supplied by the RHEL/CentOS repos which is currently 5.1.73.
```bash
yum install mysql-server
/etc/init.d/mysqld start
mysql_secure_installation
```
**Make sure to say Y** for the `mysql_secure_install` install, and follow through all the mysql install questions before continuing further.    
Failing to properly run `mysql_secure_install` will cause the kaltura mysql user to run without proper permissions to access your mysql DB.    

```bash
# Run the my.cnf configuration script ON THE MYSQL server
/opt/kaltura/bin/kaltura-mysql-settings.sh
# Enable MySQL at init time:
chkconfig mysqld on
```

##### Configure your email server and MTA - REQUIRED
If your machine doesn't have postfix email configured before the Kaltura install, you will not receive emails from the install system nor publisher account activation mails. 

By default Amazon Web Services (AWS) EC2 machines are blocked from sending email via port 25. For more information see [this thread on AWS forums](https://forums.aws.amazon.com/message.jspa?messageID=317525#317525).  
Two working solutions to the AWS EC2 email limitations are:

* Using SendGrid as your mail service ([setting up ec2 with Sendgrid and postfix](http://www.zoharbabin.com/configure-ssmtp-or-postfix-to-send-email-via-sendgrid-on-centos-6-3-ec2)).
* Using [Amazon's Simple Email Service](http://aws.amazon.com/ses/). 

##### Configure the Kaltura installation
```bash
/opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```
`[answers-file-path]` is an optional flag, in case you have an answers file ready, you can use it to perform a silent install (See [kaltura.template.ans](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura.template.ans) for documention of needed variables.).    
If you don't have an answers file, simply omit it (`/opt/kaltura/bin/kaltura-config-all.sh`). The answers file is automatically generated post the installation and is placed in `/tmp/kaltura*.ans`.     

When asked, answer all the post-install script questions (or provide an answers file to perform a silent install) -
* For CDN host: and Apache virtual host: use the resolvable domain name of your server (not always the default value, which will be the hostname).
* For Service URL: enter protocol + domain (e.g. https://mykalturasite.com).

Once the configuration phase is done, you may wish to run the sanity tests, for that, run:
```base
/opt/kaltura/bin/kaltura-sanity.sh
```

##### Configure Red5 server
1. Request http://hostname:5080
1. Click 'Install a ready-made application'
1. Mark 'OFLA Demo' and click 'Install'
1. Edit /usr/lib/red5/webapps/oflaDemo/index.html and replace 'localhost' with your actual Red5 hostname or IP
1. Test OflaDemo by making a request to http://hostname:5080/oflaDemo/ and playing the sample videos
1. Run: 

```bash
/opt/kaltura/bin/kaltura-red5-config.sh
```

You can now record a video using KMC->Upload->Record from Webcam.

## Upgrade an existing Kaltura installation 
*This will only work if the initial install was using this packages based install, it will not work for old Kaltura deployments using the PHP installers*
```bash
yum clean all
yum update "*kaltura*"
```
Then follow the on-screen instructions (in case any further actions required).   
Once the upgrade completes, please run:
```bash
/opt/kaltura/bin/kaltura-db-update.sh
/opt/kaltura/bin/kaltura-config-all.sh
```
To upgrade your DB schema.

## Fresh Database Installation
Use this in cases where you want to clear the database and start from fresh.
```bash
/opt/kaltura/bin/kaltura-drop-db.sh
/opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```

## Complete REinstall 
This will completely remove Kaltura, then download and install from scratch.
```bash
/opt/kaltura/bin/kaltura-drop-db.sh
yum remove "*kaltura*"
rm -rf /opt/kaltura
rpm -ihv http://installrepo.kaltura.org/releases/stable/RPMS/noarch/kaltura-release.noarch.rpm
yum clean all
yum install kaltura-server
/opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```
*Note that the repository URL will change soon, this is just the test repository*
