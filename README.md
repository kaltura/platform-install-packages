# Kaltura Installation Packages Project
To enable the of use standard binary packages and package managers to deploy the Kaltura platform.

This project features official deployment packages to install the Kaltura platform on a server or cluster environments using native OS package managers.

To learn more and keep track of project status, review [the project page](http://kaltura.github.io/platform-install-packages/).


# Installing Kaltura using Standard Packages

### RedHat based Linux distros (Fedora Core, RHEL, CentOS, etc.)

#### Installing on a new machine
Before you begin, make sure you're logged in as the system root. root access is required to install Kaltura. ```sudo sudo su - ```

###### iptables and ports
Kaltura requires certain ports to be open for proper operation. [See a list of required open ports below](#required-open-ports-to-run-kaltura).   
If you're just testing and don't mind an open system, you can use the below to disbale iptables altogether:
```bash
# iptables -F
# chkconfig iptables off
```
###### Disable SELinux - REQUIRED (currently Kaltura can't run properly with SELinux)
```bash 
# setenforce permissive
# edit /etc/selinux/config,set SELINUX=permissive and save
```
###### Auto Set the Kaltura install repository links, note that this is currently our test URL, the repo URL will change soon.
```bash
# rpm -ihv http://54.211.235.142/kaltura-ce-rpm/noarch/kaltura-release-9.7.0-$REVISION.noarch.rpm
Note: at the time of this release the revision is 3 but please browse http://54.211.235.142/kaltura-ce-rpm/noarch/ to find the latest.

```
###### Install and configure MySQL (if you’re going to use DB on the same server)
```bash
# yum install mysql-server
# /etc/init.d/mysqld start
# mysql_secure_installation
#Run the my.cnf configuration script
# /opt/kaltura/bin/kaltura-mysql-settings.sh
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
When asked, answer all the post-install script questions (or provide an answers file to perform a silent install)
* For CDN host: and Apache virtual host: use the resolvable domain name of your server (not always the default value, which will be the hostname)
* For Service URL: enter protocol + domain (e.g. https://mykalturasite.com)


#### Upgrading an existing Kaltura installation 
*This will only work if the initial install was using this packages based install, it will not work for old Kaltura deployments using the PHP installers*
```bash
# yum clean all
# yum update "*kaltura*"
# /opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```

#### Fresh Database Installation
Use this in cases where you want to clear the database and start from fresh
```bash
# /opt/kaltura/bin/kaltura-drop-db.sh
# /opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```

#### Complete REinstall 
This will completely remove Kaltura, then download and install from scratch.
```bash
# /opt/kaltura/bin/kaltura-drop-db.sh
# yum remove "*kaltura*"
# rm -rf /opt/kaltura
# rpm -ihv http://54.211.235.142/kaltura-ce-rpm/noarch/kaltura-release-9.7.0-$REVISION.noarch.rpm
# yum clean all
# yum install kaltura-server
# /opt/kaltura/bin/kaltura-config-all.sh [answers-file-path]
```
*Note that the repository URL will change soon, this is just the test repository*

## Debian based Linux distros (Debian, Ubuntu, etc.)
*Coming Soon*

## Required Open Ports to run Kaltura
IMPORTANT NOTE: these are the default ports for the mentioned protocols. Of course, you may choose different ports, in which case you will need to adjust accordingly.

* On the API, apps (KMC/Admin Console/MediaSpace) and Batch machines - Ports 80/TCP (in the event you intend to use http) and 443/TCP (in the event you intend to use https).  
* If you need LDAP with MediaSpace, you'll need port 636/TCP [LDAPs] or port 389/TCP [LDAP].  
* You'll also need an email, port 25/TCP by default (depending on what method you use) on the machine that will handle mail for your Kaltura server.
* If you plan on using a streaming server (e.g. Red5, FMS, Wowza) - you'll need 1935 (RTMP), 8088 (RTMPT), 5080 (Red5 Admin), 1936 (debug).  
* If you're planning to use Remote Storage/Drop Folders - you'll need to enable access in one of the following protocols FTP - port 21/TCP, SFTP - port 22/TCP, etc.  
* If you'll use NFS - port 2049/TCP+UDP and 111/TCP+UDP for portmap.  
* On your MySQL and DWH machines - port 3306/TCP.  
* On your Sphinx machine - ports 9312/TCP.   

**If you are installing an all-in-one, all these ports should be open on the machine**


# License and Copyright Information
All code in this project is released under the [AGPLv3 license](http://www.gnu.org/licenses/agpl-3.0.html) unless a different license for a particular library is specified in the applicable library path. 

Copyright © Kaltura Inc. All rights reserved.

Authors [@jessp01](https://github.com/jessp01), [@zoharbabin](https://github.com/zoharbabin) and many others.
