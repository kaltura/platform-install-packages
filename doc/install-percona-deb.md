## Installing the MySQL 5.5 Percona deb package
The Kaltura Server currently supports all MySQL versions between 5.1 and 5.6. 
If your distro's official repos include a higher version, it is necessary to install the MySQL packages from an alternative repo.

For Ubuntu Xenial [16.04], we recommend the use of the Percona deb packages but any MySQL 5.5 distribution should work equally well.
To install the Percona MySQL 5.5 deb packages, run the following commands:
```
# wget https://repo.percona.com/apt/percona-release_0.1-4.xenial_all.deb
# dpkg -i percona-release_0.1-4.xenial_all.deb
# apt-get update
# apt-get install percona-server-server-5.5
```

*Please be aware that these packages cannot co-exist with the Xenial mysql-server packages.*

After installing the percona-server-server-5.5 deb and all its dependencies, run:
```
# mysql_secure_installation
```

**Be sure to set a MySQL root password.**

**When installing an all in one Kaltura instance, simply input 'Y' whenever prompted by `mysql_secure_installation`. 
When deploying a cluster, input 'Y' in response to all prompts EXCEPT for "Disallow root login remotely?" to which you should reply with 'N'.**

Edit /etc/mysql/my.cnf so that it incldues the following directives under the ```[mysqld]``` section:
```
lower_case_table_names = 1
innodb_file_per_table
innodb_log_file_size=32M
open_files_limit = 20000
max_allowed_packet = 16M
```

Then:
```
# rm /var/lib/mysql/ib_logfile*
```

And restart the MySQL daemon.

*Note that the values mentioned above are the min values the Kaltura Server can work with, depending on your resources and needs you may want to set higher values.*

To make sure the values are now correct, you can run this commands from the MySQL console:
```
mysql> select @@open_files_limit;
+--------------------+
| @@open_files_limit |
+--------------------+
|              20000 |
+--------------------+
1 row in set (0.00 sec)

mysql> select @@lower_case_table_names;
+--------------------------+
| @@lower_case_table_names |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.00 sec)

mysql> select @@innodb_log_file_size;
+------------------------+
| @@innodb_log_file_size |
+------------------------+
|               33554432 |
+------------------------+
1 row in set (0.00 sec)

mysql> select @@max_allowed_packet;
+----------------------+
| @@max_allowed_packet |
+----------------------+
|             16777216 |
+----------------------+
1 row in set (0.00 sec)
```
