# Deploying Kaltura Clusters

Below are **RPM** based instructions for deploying Kaltura Clusters.    
Refer to the [all-in-one installation guide](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md) for more notes about deploying Kaltura in RPM supported environments.    
Refer to the [Deploying Kaltura Clusters Using Chef](https://github.com/kaltura/platform-install-packages/blob/master/doc/rpm-chef-cluster-deployment.md) for automated Chef based deployments.

### Instructions here are for a cluster with the following members:

* [Load Balancer](#apache-load-balancer)
* [NFS server](#the-nfs)
* [DB and Sphinx](#the-mysql-db-and-sphinx)
* [Front servers](#the-front)
* [Batch servers](#the-batch)
* [DWH server](#the-datawarehouse)

### Important Notes
* If you see a `#` at the beginning of a line, this line should be run as `root`.
* All post-install scripts accept answers-file as parameter, this can used for silent-automatic installs.

##### iptables and ports
Kaltura requires certain ports to be open for proper operation. [See the list of required open ports](https://github.com/kaltura/platform-install-packages/blob/master/doc/kaltura-required-ports.md).   

##### Disable SELinux
This is REQUIRED on all machines, currently Kaltura can't run properly with SELinux.
```bash 
setenforce permissive
# To verify SELinux will not revert to enabled next restart:
# Edit /etc/selinux/config
# Set SELINUX=permissive
# Save /etc/selinux/config
```

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

##### Configure your email server and MTA - REQUIRED
If your machine doesn't have postfix email configured before the Kaltura install, you will not receive emails from the install system nor publisher account activation mails. 

By default Amazon Web Services (AWS) EC2 machines are blocked from sending email via port 25. For more information see [this thread on AWS forums](https://forums.aws.amazon.com/message.jspa?messageID=317525#317525).  
Two working solutions to the AWS EC2 email limitations are:

* Using SendGrid as your mail service ([setting up ec2 with Sendgrid and postfix](http://www.zoharbabin.com/configure-ssmtp-or-postfix-to-send-email-via-sendgrid-on-centos-6-3-ec2)).
* Using [Amazon's Simple Email Service](http://aws.amazon.com/ses/). 


### Apache Load Balancer

Load balancing is recommended to scale your front and streaming server (e.g. Red5, Wowza) machines.   
To deploy an Apache based load balancer, refer to the [Apache Load Balancer configuration file example](https://github.com/kaltura/platform-install-packages/blob/master/doc/apache_balancer.conf).   
This example config uses the `proxy_balancer_module` and `proxy_module` Apache modules to setup a simple Apache based load balancer (refer to official docs about [proxy_balancer_module](http://httpd.apache.org/docs/2.2/mod/mod_proxy_balancer.html) and [proxy_module](http://httpd.apache.org/docs/2.2/mod/mod_proxy.html) to learn more).    
To configure the load balancer on your environment: 

1. Replace all occurances of `balancer.domain.org` with the desired hostname for the load balanacer (the main end-point your end-users will reach).
1. Replace all occurances of `node0.domain.org` with the first front machine hostname and `node1.domain.org` with the second front machine hostname.    
1. In order to add more front machines to the load balancing poll, simply clone the nodeX.domain.org lines and change to the hostnames of the new front machines.

Note that the port in the example file is 80 (standard HTTP port), feel free to change it if you're using a non-standard port.

##### SSL Offloading on a Load Balancer
Load Balancers have the ability to perform SSL offloading (aka [SSL Acceleration](http://en.wikipedia.org/wiki/SSL_Acceleration)). Using SSL offloading can dramatically reduce the load on the systems by only encrypting the communications between the Load Balancer and the public network while communicating on non-encrypted http with the internal network (in Kaltura's case, between the Load Balancer and the front machines).

Kaltura recommends that you utilize offloading. I this case, you will only need to deploy the SSL certificates on your Load Balancer.    
However, if network requirements dictates (noting that this will hurt performance) Kaltura will work just as well with double encryption - But be sure to deploy the SSL certificates on the front machines as well as the load balancer.

##### Self-Balancing Components
The following server roles should not be load-balanced:

* Batche machines are very effective at scaling on themselves, by simply installing more batch servers in your cluster they will seamlessly register against the DB on their own and begin to take jobs independantly.
* Sphinx machines are balanced in the Kaltura application level.
* MySQL DB has a [master-slave architecture](https://dev.mysql.com/doc/refman/5.0/en/replication-howto.html) of its own.

### The NFS
The NFS is the shared network storage between all machines in the cluster. To learn more about NFS read [this wikipedia article about NFS](http://en.wikipedia.org/wiki/Network_File_System).
```
# yum install nfs-utils-lib
# chkconfig nfs on
# service rpcbind start
# service nfs start
# mkdir -p /opt/kaltura/web
```
Edit `/etc/exports` to have the desired settings, for example:
`/opt/kaltura/web *(rw,sync,no_root_squash)`

Note that you may choose different NFS settings which is fine so long as:
* the kaltura and apache user are both able to write to this volume
* the kaltura and apache user are both able create files with them as owners. i.e: do not use all_squash as an option.

Then set priviliges accordingly:
```
# groupadd -r kaltura -g7373
# useradd -M -r -u7373 -d /opt/kaltura -s /bin/bash -c "Kaltura server" -g kaltura kaltura
# groupadd -g 48 -r apache
# useradd -r -u 48 -g apache -s /sbin/nologin -d /var/www -c "Apache" apache
# usermod -a -G kaltura apache
# chown -R kaltura /opt/kaltura
```

To export the volume run: `# exportfs -a`

### The MySQL DB and Sphinx
```
# rpm -Uhv http://installrepo.kaltura.org/releases/nightly/RPMS/noarch/kaltura-release.noarch.rpm
# yum install kaltura-sphinx mysql-server mysql
# /opt/kaltura/bin/kaltura-mysql-settings.sh
# /opt/kaltura/bin/kaltura-sphinx-config.sh
# mysql_secure_installation
```
**Make sure to say Y** for the `mysql_secure_install` install, and follow through all the mysql install questions before continuing further.    
Failing to properly run `mysql_secure_install` will cause the kaltura mysql user to run without proper permissions to access your mysql DB.    
```
# mysql -uroot -pYOUR_DB_ROOT_PASS
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
```

### The Front
Front in Kaltura represents the machines hosting the user-facing components, including the Kaltura API, the KMC and Admin Console, MediaSpace and all client-side widgets. 
```
# rpm -Uhv http://installrepo.kaltura.org/releases/nightly/RPMS/noarch/kaltura-release.noarch.rpm
# /opt/kaltura/bin/kaltura-nfs-client-config.sh
# yum install kaltura-front kaltura-widgets kaltura-html5lib kaltura-html5-studio
# /opt/kaltura/bin/kaltura-front-config.sh
# /opt/kaltura/bin/kaltura-db-config.sh
```

### The Batch
Batch in Kaltura represents the machines running all async operations. To learn more, read: [Introduction to Kaltura Batch Processes](http://knowledge.kaltura.com/node/230).
```
# rpm -Uhv http://installrepo.kaltura.org/releases/nightly/RPMS/noarch/kaltura-release.noarch.rpm
# /opt/kaltura/bin/kaltura-nfs-client-config.sh
# yum install kaltura-batch
# /opt/kaltura/bin/kaltura-batch-config.sh
```

### The DataWarehouse
The DWH is Kaltura's Analytics server.
```
# rpm -Uhv http://installrepo.kaltura.org/releases/nightly/RPMS/noarch/kaltura-release.noarch.rpm
# yum install kaltura-dwh
# /opt/kaltura/bin/kaltura-nfs-client-config.sh
# /opt/kaltura/bin/kaltura-dwh-config.sh
```
