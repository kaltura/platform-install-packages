General
=======
The query cache is a generic mechanism for caching the results of database queries using memcache. 

The query cache uses a single shared memcache that will be added to each datacenter (not machine local memcaches). 

How does it work?

Example:
========

mysql> select * from flavor_asset where entry_id=x and partner_id=y and ...

The first time this query is performed, it will get to the database. After the query completes and the Propel objects are populated, the objects are serialized and stored to the memcache. The key used for caching is a function of the query string: QCQ-<query type>-<md5(serialize($criteria))>, where query type is 'sel' for doSelect and 'cnt' for doCount (we use serialize($criteria) to avoid building the query string unnecessarily). The next time the same query is performed it will return the results from the memcache.

What is the performance gain?
=============================
Complex select queries that have several conditions / count queries will be replaced by a simple retrieveByPK-like query on the memcache.

The query cache stores serialized objects, saving the time of the Propel hydration process. 

How do we know when a cached query is valid?
============================================
Every query that is cached is associated with at least one 'invalidation key', each invalidation key holds the time of the last relevant change to the database, in the example above, we use the key: 'QCI-flavor_asset:entry_id=x'. Before we return a cached query from the memcache, we compare the time of the cached query to the time saved in all relevant invalidation keys. If one of the invalidation keys is newer than the cached query, the cached query is treated as invalid and won't be used.

When do we update the invalidation keys?
========================================
Whenever a flavor asset object of entry_id x is saved, it will also update the time saved in the memcache under 'flavor_asset:entry_id=x', thus invalidating all the queries that contained entry_id=x. On single datacenter environments the invalidation keys can be updated automatically by the 'save' functions. On multi datacenter environments this won't work, because it won't invalidate the queries that are cached on the remote DC. So, instead, we'll define triggers on the database that will perform the invalidation - whether the database was modified locally or by the replication.

How to add a new query to the cache?
====================================
Override <peer>::getCacheInvalidationKeys to return a list of invalidation keys that should be checked before the supplied $criteria can be returned from the cache.
Override <object>::getCacheInvalidationKeys to return a list of invalidation keys that should be updated when $this object is saved.
The list of invalidation keys to update should also be added to $INVALIDATION_KEYS in deployment/base/scripts/createQueryCacheTriggers.php. 

Use the following samples:
    Basic cache: asset.php & assetPeer.php.
    Multiple invalidation fields: kuser.php & kuserPeer.php.
    IN criteria caching: permission.php & permissionPeer.php. 

What is the process for setting up the query cache?
===================================================

Set up a single machine on each datacenter that will run the shared memcached. Configure the hostname and port of this memcache in local.ini (global_memcache_host / global_memcache_port).
Single datacenter environment only
On all servers, set query_cache_enabled and query_cache_invalidate_on_change to true in kConfLocal
Multi datacenter environment only
Perform the following on one of the mysql slaves in each datacenter:

* Install memcached on a dedicated server, and configure two memcached instances
* Make sure you have a mysql master and slave replication pair
* Compile and install 'Memcached Functions for MySQL'
* Install the functions on the database slave by running: mysql kaltura < memcached_functions_mysql-1.1/sql/install_functions.sql 
* Configure the 'Memcached Functions for MySQL' library to use the shared memcache server by adding the command 'select memc_servers_set('<global memcache host>:<global memcache port>');' to the mysql init script.
    Note: To add an init script for mysql, add the switch 'init-file=<mysql init script path>' to the section [mysqld] in my.cnf and make sure that mysql user has acess to this file
* Restart mysql
* Install the triggers by running from deployment/base/scripts: php createQueryCacheTriggers.php create <slave-host> <user> <password> 
* On all servers, set query_cache_enabled to true in local.ini (query_cache_invalidate_on_change should be left false).

Pre-requisites
==============

CentOS / RHEL:
```
# yum install libmemcached-devel mysql-devel gcc
```

Ubuntu/Debian:
```
apt-get install libmemcached-dev libmysqld-dev build-essential
```
Compile
=======
```
# wget https://launchpad.net/memcached-udfs/trunk/1.1/+download/memcached_functions_mysql-1.1.tar.gz
# tar -xvf ./memcached_functions_mysql-1.1.tar.gz
# cd ./memcached_functions_mysql-1.1
```
```
#./configure --with-mysql=/usr/bin/mysql_config 
# make install
```

Install plugin
=======
CentOS / RHEL:
```
# cp /usr/local/lib/libmemcached_functions_mysql.so /usr/lib64/mysql/plugin/
```
Ubuntu/Debian:
```
# cp /usr/local/lib/libmemcached_functions_mysql.so /usr/lib/mysql/plugin/
```

Install plugin functions
=======
```
mysql -u root -p --database kaltura < memcached_functions_mysql-1.1/sql/install_functions.sql 
```

Configure memcached server
=======
```
echo "select memc_servers_set('<global memcache host>:<global memcache port>');" > /var/lib/mysql/mysql.init
echo "select memc_servers_behavior_set('MEMCACHED_BEHAVIOR_NO_BLOCK', 1);" >> /var/lib/mysql/mysql.init
chown mysql:mysql /var/lib/mysql/mysql.init
```

Configure init script
=======
Add to my.cnf in [mysqld] section:
```
init-file=/var/lib/mysql/mysql.init
```

Restart MySQL
=======
```
service mysqld restart
```

Install Kaltura Triggers
=======
On API server:
```
php /opt/kaltura/app/deployment/base/scripts/createQueryCacheTriggers.php create <db-slave-host> <db-user> <db-password> realrun
```

Configure API servers to use Query Cache
=======
In /opt/kaltura/app/configurations/local.ini
```
query_cache_enabled = true
query_cache_invalidate_on_change = true
```

In /opt/kaltura/app/configurations/cache.ini
```
[memcacheBig:memcacheBase]
port = <global memcache port>
host = <global memcache host>

[memcacheKeys:memcacheBase]
port = <global memcache port+1>
host = <global memcache host>

[mapping]
fileSync = memcacheBig
permissionManager = apcSerialized,memcacheBig
queryCacheKeys = memcacheKeys
queryCacheQueries = memcacheBig
sphinxStickySessions = memcacheBig
feedEntry = memcacheBig
apiExtraFieldsCache = apc
ps2Cache = memcacheLocal
apiV3Cache = memcacheLocal,memcacheBig
playManifest = memcacheLocal,memcacheBig
apiV3Feed = filesystemApiV3Feed
lockKeys = memcacheKeys
apiWarmup = apc,memcacheBig
kwidgetSwf = memcacheBig
partnerSecrets = apc,memcacheBig
liveMediaServer_0 = memcacheBig
liveMediaServer_1 = memcacheBig
sphinxExecutedServer = apc
```

Activate configuration
=======
```
touch /opt/kaltura/app/cache/base.reload
```
