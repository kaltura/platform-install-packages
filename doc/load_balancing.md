# Load Balancing

## SSL Offloading on a Load Balancer
Load Balancers can perform SSL offloading (aka [SSL Acceleration](http://en.wikipedia.org/wiki/SSL_Acceleration)). Using SSL offloading can dramatically reduce the load on the systems by only encrypting the communications between the Load Balancer and the public network while communicating over http with the internal nodes.

We recommend that you utilise SSL offloading. In such a case, you will only need to deploy the SSL certificates on your Load Balancer.    

### Self-Balancing Components
The following server roles should not be load-balanced:

* Sphinx machines are balanced at the Kaltura application level.
* See below the notes regarding MySQL replication and scaling.

### HAProxy Load Balancer
Load balancing is recommended in order to scale your front and streaming machines.   

Make sure you have HAProxy compiled with SSL support. It seems the official packages on several Linux distros are compiled without it [propbably due to licensing considerations]  and so, you may need to compile your own. 
This can be done with these simple steps [replace $HA_PROXY_VERSION with whatever the latest stable happens to be at the time of reading this]:

```
# wget http://www.haproxy.org/download/1.5/src/haproxy-$HA_PROXY_VERSION.tar.gz
# tar zxvf haproxy-$HA_PROXY_VERSION.tar.gz
# cd haproxy-$HA_PROXY_VERSION
# make USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 USE_CRYPT_H=1 USE_LIBCRYPT=1
# make install
```

Please refer to the [configuration file example](haproxy.cfg).
To configure the load balancer on your environment:

1. Replace all occurances of `node0.domain.org` with the first front machine hostname and `node1.domain.org` with the second front machine hostname.
2. In order to add more front machines to the load balancing poll, simply clone the nodeX.domain.org line and change to the hostnames of the new front machines and change the server cookie ID (after the cookie keyword).

If you want to have logging for HAProxy with the sample configuration, add the following lines to the syslog/rsyslog configuration (for rsyslog you can put this in the file /etc/rsyslog.d/haproxy.conf):
```
$ModLoad imudp
$UDPServerRun 514

local0.* -/var/log/haproxy_0.log
local1.* -/var/log/haproxy_1.log
```

And restart syslog/rsyslog:
```
restart rsyslog
```

### Apache Load Balancer

Load balancing is recommended in order to scale your front and streaming machines.   
To deploy an Apache based load balancer, refer to the [Apache Load Balancer configuration file example](apache_balancer.conf).   
This example config uses the `proxy_balancer_module` and `proxy_module` Apache modules to setup a simple Apache based load balancer (refer to official docs about [proxy_balancer_module](http://httpd.apache.org/docs/2.2/mod/mod_proxy_balancer.html) and [proxy_module](http://httpd.apache.org/docs/2.2/mod/mod_proxy.html) to learn more).    
To configure the load balancer on your environment: 

1. Replace all occurances of `balancer.domain.org` with the desired hostname for the load balanacer (the main end-point your end-users will reach).
1. Replace all occurances of `node0.domain.org` with the first front machine hostname and `node1.domain.org` with the second front machine hostname.    
1. In order to add more front machines to the load balancing poll, simply clone the nodeX.domain.org lines and change to the hostnames of the new front machines and the route.

Note that the port in the example file is 80 (standard HTTP port), feel free to change it if you're using a non-standard port.

