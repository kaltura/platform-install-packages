# Installing Kaltura on RedHat Linux
This guide applies to all major RH based Linux distros including Fedora Core, RHEL, CentOS, etc.

## Installing on a new machine
Before you begin, make sure you're logged in as the system root. root access is required to install Kaltura. ```sudo sudo su - ```

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
# Edit /etc/selinux/config, Set SELINUX=permissive and save
```
###### Auto Set the Kaltura install repository links 
**Note: that this is currently our test URL, the repo URL will change soon.**
```rpm -ihv http://54.211.235.142/kaltura-ce-rpm/noarch/kaltura-release-9.7.0-$REVISION.noarch.rpm```   
*Jan 26, 2014*: At the time of this release the revision is 3 but please browse http://54.211.235.142/kaltura-ce-rpm/noarch/ to find the latest.
###### Install and configure MySQL (if you’re going to use DB on the same server)
```bash
yum install mysql-server
/etc/init.d/mysqld start
mysql_secure_installation
# Run the my.cnf configuration script
/opt/kaltura/bin/kaltura-mysql-settings.sh
```
###### Configure your email server and MTA - REQUIRED
If your machine doesn't have postfix email configured before the Kaltura install, you will not receive emails from the install system nor publisher account activation mails. 

By default Amazon Web Services (AWS) EC2 machines are blocked from sending email via port 25. For more information see [this thread on AWS forums](https://forums.aws.amazon.com/message.jspa?messageID=317525#317525).  
Two working solutions to the AWS EC2 email limitations are:

* Using SendGrid as your mail service ([setting up ec2 with Sendgrid and postfix](http://www.zoharbabin.com/configure-ssmtp-or-postfix-to-send-email-via-sendgrid-on-centos-6-3-ec2)).
* Using [Amazon's Simple Email Service](http://aws.amazon.com/ses/). 

###### Configure the Kaltura installation (post-install script)
```bash
/opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```
`[answers-file-path]` is an optional flag, in case you have an answers file ready, you can use it to perform a silent install. If you don't have an answers file, simply omit it (`/opt/kaltura/bin/kaltura-config-all.sh`).   
When asked, answer all the post-install script questions (or provide an answers file to perform a silent install)
* For CDN host: and Apache virtual host: use the resolvable domain name of your server (not always the default value, which will be the hostname)
* For Service URL: enter protocol + domain (e.g. https://mykalturasite.com)

## Upgrading an existing Kaltura installation 
*This will only work if the initial install was using this packages based install, it will not work for old Kaltura deployments using the PHP installers*
```bash
yum clean all
yum update "*kaltura*"
/opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```

## Fresh Database Installation
Use this in cases where you want to clear the database and start from fresh
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
rpm -ihv http://54.211.235.142/kaltura-ce-rpm/noarch/kaltura-release-9.7.0-$REVISION.noarch.rpm
yum clean all
yum install kaltura-server
/opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```
*Note that the repository URL will change soon, this is just the test repository*
