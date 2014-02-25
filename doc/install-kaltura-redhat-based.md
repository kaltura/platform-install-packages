# Installing Kaltura on RedHat Linux
This guide describes installation of an all-in-one Kaltura server and applies to all major RH based Linux distros including Fedora Core, RHEL, CentOS, etc. ([Note the supported distros and versions](http://kaltura.github.io/platform-install-packages/#supported-distros)).       

While already supported by the code, this document doesn't yet describe cluster deployment. Instructions for specific server-roles/groups and cluster configuration will soon be added. If you're eager to test cluster deployment, contact us over IRC #kaltura on freenode.net.

Note for testers using VMWare: You can find solid VMWare images at - http://www.thoughtpolice.co.uk/vmware/ --> Make sure to only use compatible OS images; either RedHat or CentOS 5.n, 6.n or FedoraCore 18+.

## Installing on a new machine

###### Pre-Install notes

* **Resolveable host names** - When installing, you will be promopted for each server's resolvable hostname. Note that it is crucial that all host names will be resolveable by other servers in the cluster (and outside the cluster for front machines). Before installing, verify the /etc/hosts file is properly configured and that all Kaltura server hostnames are resolveable in your network.
* **ROOT is REQUIRED** - Before you begin, make sure you're logged in as the system root. root access is required to install Kaltura. ```sudo su - ```

###### iptables and ports
Kaltura requires certain ports to be open for proper operation. [See the list of required open ports](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-required-ports.md).   
If you're just testing and don't mind an open system, you can use the below to disbale iptables altogether:
```bash
iptables -F
chkconfig iptables off
```
###### Disable SELinux - REQUIRED (currently Kaltura can't run properly with SELinux)
```bash 
setenforce permissive
# To verify SELinux will not revert to enabled next restart:
# Edit /etc/selinux/config
# Set SELINUX=permissive
# Save /etc/selinux/config
```
###### Auto Set the Kaltura install repository links 
**Note: that this is currently our test URL, the repo URL will change soon.**
For nightly builds use:
```bash   
\\#rpm -Uhv http://54.211.235.142/releases/nightly/RPMS/noarch/kaltura-release-9.11.0-3.noarch.rpm
```
For stable updates:
```bash
\\# rpm -ihv
http://54.211.235.142/releases/stable/RPMS/noarch/kaltura-release.noarch.rpm
```

###### Install the Kaltura Packages
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

###### Install and configure MySQL (if you’re going to use DB on the same server)
```bash
yum install mysql-server
/etc/init.d/mysqld start
mysql_secure_installation
# Run the my.cnf configuration script ON THE MYSQL server
/opt/kaltura/bin/kaltura-mysql-settings.sh
# Enable MySQL at init time:
chkconfig mysqld on
```
###### Configure your email server and MTA - REQUIRED
If your machine doesn't have postfix email configured before the Kaltura install, you will not receive emails from the install system nor publisher account activation mails. 

By default Amazon Web Services (AWS) EC2 machines are blocked from sending email via port 25. For more information see [this thread on AWS forums](https://forums.aws.amazon.com/message.jspa?messageID=317525#317525).  
Two working solutions to the AWS EC2 email limitations are:

* Using SendGrid as your mail service ([setting up ec2 with Sendgrid and postfix](http://www.zoharbabin.com/configure-ssmtp-or-postfix-to-send-email-via-sendgrid-on-centos-6-3-ec2)).
* Using [Amazon's Simple Email Service](http://aws.amazon.com/ses/). 

###### Configure the Kaltura installation
```bash
/opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```
`[answers-file-path]` is an optional flag, in case you have an answers file ready, you can use it to perform a silent install. If you don't have an answers file, simply omit it (`/opt/kaltura/bin/kaltura-config-all.sh`). The answers file is automatically generated post the installation and is placed in `/tmp/kaltura*.ans`.     
When asked, answer all the post-install script questions (or provide an answers file to perform a silent install) -
* For CDN host: and Apache virtual host: use the resolvable domain name of your server (not always the default value, which will be the hostname).
* For Service URL: enter protocol + domain (e.g. https://mykalturasite.com).

###### Configure Red5 server
- Request http://hostname:5080
- Click 'Install a ready-made application'
- Mark 'OFLA Demo' and click 'Install'
- Edit /usr/lib/red5/webapps/oflaDemo/index.html and replace 'localhost' with your actual Red5 hostname or IP
- Test OflaDemo by making a request to http://hostname:5080/oflaDemo/ and playing the sample videos
- Run: 
```bash
 # /opt/kaltura/bin/kaltura-red5-config.sh
```
You can now record a video using KMC->Upload->Record from Webcam.

## Upgrade an existing Kaltura installation 
*This will only work if the initial install was using this packages based install, it will not work for old Kaltura deployments using the PHP installers*
```bash
yum clean all
yum update "*kaltura*"
```
Then follow the on-screen instructions (in case any further actions required).   


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
rpm -ihv http://54.211.235.142/nightly/RPMS/noarch/kaltura-release.noarch.rpm
yum clean all
yum install kaltura-server
/opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```
*Note that the repository URL will change soon, this is just the test repository*
