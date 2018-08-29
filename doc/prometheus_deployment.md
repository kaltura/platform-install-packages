# Kaltura Prometheus Deployment doc
This document is meant to provide general guidelines for deploying the Kaltura Prometheus, Alertmanager, Consul and Prometheus exporter packages.

## Available packages
**Note about users:
The Prometheus and Alertmanager daemons run as the ```prometheus``` user which is created during the RPM's %pre hook.
The Consul daemons run as the ```consul``` user which is created during the RPM's %pre hook.
All exporters run as the ```prometheus``` user and are shipped with an init script [CentOS/RHEL6] or a systemd unit file [CentOS/RHEL 7 and above].**

### kaltura-prometheus
This package provides the Prometheus daemon and configuration.
Main config file: /opt/kaltura/prometheus/etc/prometheus.yml
Rules config dir: /opt/kaltura/prometheus/etc/rules/

prometheus.yml relies on Consul for the service discovery, see #kaltura-consul.
The default prometheus.yml expects the kaltura-alertmanager to be installed on the same machine.

For security reasons, the Prometheus daemon is bound to loopback [port 9090, TCP].
If access to the web I/F is needed, a load balancer with basic authentication should be set up in front of it. 
While deploying, it is sometimes useful to access it directly, in which case, the value for ```--web.listen-address``` should be changed ```/usr/lib/systemd/system/kaltura-prometheus.service```. Once done, run:
```
# systemctl daemon-reload
# service kaltura-prometheus restart
```

**In production ENVs, at least two instances of Prometheus and Alertmanager should be deployed. In order to avoid duplicate alerts, only one Alertmanager instance should be enabled at any given moment.**

#### Adding rules
Rules should be added under /opt/kaltura/prometheus/etc/rules.
Ideally, each service should have its dedicated YML file under the scandir, containing all rules pertaining to that service.

### kaltura-alertmanager
This package provides the Prometheus Alertmanager daemon and configuration.
Main config file: /opt/kaltura/prometheus/alertmanager/etc/alertmanager.yml
Before starting the service, edit /opt/kaltura/prometheus/alertmanager/etc/alertmanager.yml and replace the following tokens:
```
@SMTP_HOST@
@FROM_EMAIL@
@DEFAULT_ALERTING_EMAIL_ADDR@
```

If your MTA requires authentication, you will also need to replace:
```
@SMTP_USER@
@SMTP_PASSWD@
```

#### Customising email templates
Templates are stored under:
/opt/kaltura/prometheus/alertmanager/etc/templates

See ```/opt/kaltura/prometheus/alertmanager/etc/templates/kaltura.tmpl```

### kaltura-consul
This package provides the Consul daemon, configurations and init scripts [CentOS/RHEL6] or systemd unit files [CentOS/RHEL 7 and above].

When deploying a server, edit ```/opt/kaltura/consul/etc/consul.d/server/config.json``` and replace the following tokens:
```
@DATA_CENTER@ - a descriptive name for the cluster
@SECRET@ - used to encrypt data between server and agents nodes. Should be the same string across cluster nodes.
```
Once done, start the Consul daemon with:
```
# service kaltura-consul-server start
```

When deploying an agent, edit ```/opt/kaltura/consul/etc/consul.d/client/config.json``` and replace the following tokens:
```
@DATA_CENTER@ - a descriptive name for the cluster
@SECRET@ - used to encrypt data between server and agents nodes. Should be the same string across cluster nodes.
@CONSUL_SERVER_HOST@ - the hostname/IP of the Consul server
```
Once done, start the Consul daemon with:
```
# service kaltura-consul-client start
```

### Prometheus Exporter packages
The following packages are currently available:

- kaltura-apache-exporter
- kaltura-nginx-exporter
- kaltura-mysql-exporter
- kaltura-memcached-exporter
- kaltura-sphinx-exporter
- kaltura-node-exporter

All exporters run as the ```prometheus``` user and are shipped with an init script [CentOS/RHEL6] or a systemd unit file [CentOS/RHEL 7 and above].

When deploying the kaltura-mysql-exporter, one must edit ```/etc/sysconfig/kaltura-mysqld-exporter``` and set the DATA_SOURCE_NAME ENV var.

It is recommended that you create a dedicated MySQL user for the use of this exporter, for example:
```
mysql> CREATE USER 'exporter'@'EXPORTER_HOST' IDENTIFIED BY 'XXXXXXXX' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'EXPORTER_HOST';
```

The other exporters should work out of the box and do not require additional configuration.
