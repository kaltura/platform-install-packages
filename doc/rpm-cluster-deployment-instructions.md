# Kaltura cluster deployment

Instructions here are for a cluster with the following members:
* NFS server
* Front
* Batch server
* Sphinx and DB server
* DWH server

### On the NFS machine:
```
# yum install nfs-utils
# /etc/init.d/nfs start
# mkdir /opt/kaltura/web
```
edit `/etc/exports` to have the desired settings, for example:
`/opt/kaltura/web *(rw,sync,no_root_squash)`

Note that you may choose different NFS settings which is fine so long as:
* the kaltura and apache user are both able to write to this volume
* the kaltura and apache user are both able create files with them as owners. i.e: do not use all_squash as an option.

to export the volume:
`# exportfs -a`

On the Front:
=============
edit /etc/fstab and add:
nfs-host:/opt/kaltura/web /opt/kaltura/web nfs4

# yum install kaltura-front kaltura-widgets
# /opt/kaltura/bin/kaltura-front-config.sh

On the MySQL and Sphinx server:
===============================
# yum install kaltura-sphinx mysql-server
# mysql_secure_install
# /opt/kaltura/bin/kaltura-mysql-settings.sh
# /opt/kaltura/bin/kaltura-sphinx-config.sh
# /opt/kaltura/bin/kaltura-db-config.sh

On the batch server:
====================
edit /etc/fstab and add:
nfs-host:/opt/kaltura/web /opt/kaltura/web nfs4
# /opt/kaltura/bin/kaltura-batch-config.sh

On the DWH server:
==================
edit /etc/fstab and add:
nfs-host:/opt/kaltura/web /opt/kaltura/web nfs4
# /opt/kaltura/bin/kaltura-dwh-config.sh
