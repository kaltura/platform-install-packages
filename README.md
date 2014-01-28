# Kaltura Installation Packages Project
To enable the of use standard binary packages and package managers to deploy the Kaltura platform.

This project features official deployment packages to install the Kaltura platform on a server or cluster environments using native OS package managers.

To learn more and keep track of project status, review [the project page](http://kaltura.github.io/platform-install-packages/).


## Installing Kaltura using Standard Packages
* [Installing on RedHat based Linux distros (including FC, RHEL and CentOS)](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md).
* Installing on Debian based Linux distros (including Ubuntu) - *Coming Soon*


## Repository Server Release Name Convension
The repository URL will be structured as follow:    
* RPM: http://REPOSITORY_DOMAIN/BRANCH/noarch/kaltura-release.noarch.rpm
* DEB: http://REPOSITORY_DOMAIN/debian/dists/BRANCH

**BRANCH** - will be replaced with the name of the desired install release branch.   
We will eventually have the following branches:
* nightly - latest testing release, built every night from latest dev branch.
* stable-latest - latest recommended production release.
* Kaltura official major release names (e.g. eagle, falcon, gemini, hercules, iris, etc.).

<<<<<<< HEAD
```
###### Install and configure MySQL server
```bash
# yum install mysql-server
# /etc/init.d/mysqld start
# mysql_secure_installation
If installing locally, run the MySQL configuration script. You may also copy it to your MySQL server and run it there.
# /opt/kaltura/bin/kaltura-mysql-settings.sh
```
###### Configure your email server and MTA - REQUIRED
If your machine doesn't have postfix email configured before the Kaltura install, you will not receive emails from the install system nor publisher account activation mails. 
=======
##### Current TEST repository URL:
At the moment we're in early alpha testing of the RPM repository.     
**The URL of the repository will change when we reach beta phase.**     
`http://54.211.235.142/nightly/noarch/kaltura-release.noarch.rpm`
>>>>>>> 589d368b5538fc050c33a06edda84d28db586778


## License and Copyright Information
All code in this project is released under the [AGPLv3 license](http://www.gnu.org/licenses/agpl-3.0.html) unless a different license for a particular library is specified in the applicable library path. 

Copyright © Kaltura Inc. All rights reserved.

Authors [@jessp01](https://github.com/jessp01), [@zoharbabin](https://github.com/zoharbabin) and many others.
