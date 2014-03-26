# Deploying Kaltura Clusters

Below are **RPM** based instructions for deploying Kaltura Clusters.    
Refer to the [all-in-one installation guide](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md) for more notes about deploying Kaltura in RPM supported environments.    
Refer to the [Deploying Kaltura Clusters Using Chef](https://github.com/kaltura/platform-install-packages/blob/master/doc/rpm-chef-cluster-deployment.md) for automated Chef based deployments.

#### Notes
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

#### Instructions here are for a cluster with the following members:
* [NFS server]()
* [DB and Sphinx server]()
* [Front]()
* [Batch server]()
* [DWH server]()

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

### The MySQL and Sphinx server
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
