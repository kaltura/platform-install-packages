### Nginx SSL configuration

The kaltura-nginx package is used for two functions:
- On-the-fly repackaging of MP4 files to DASH, HDS, HLS, MSS using [VOD module](https://github.com/kaltura/nginx-vod-module)
- RTMP Live Streaming using the [RTMP module](https://github.com/arut/nginx-rtmp-module)

**A general note about SSL: if you have a CE cluster, as opposed to an all in one instance, it is wise to use a load balancer configured to perform SSL offloading to the various Kaltura API and Nginx nodes.**
You can read more about load balancing here:

[RPM cluster howto](rpm-cluster-deployment-instructions.md#apache-load-balancer)

[deb cluster howto](deb-cluster-deployment-instructions.md#apache-load-balancer)

During the post install configuration phase, you will be prompted about whether or not you'd like to configure Nginx over SSL.
In the event you choose to do so, you will be prompted for the SSL certificate and key files as well as the port you'd like to use [default SSL port is 8443 since 443 is used by Apache].
Once the configuration is done, you should also adjust the delivery_profile.url column like so:
```
# mysql -h$DB1_HOST -u $DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME
mysql> UPDATE delivery_profile SET url = REPLACE(url, 'http://$NGINX_HOST:$NGINX_NON_SLL_PORT', 'https://$NGINX_HOST:$NGINX_SLL_PORT') WHERE url LIKE 'http://$NGINX_HOST:$NGINX_NON_SLL_PORT%';
```

So, for example, if your Nginx host is test.kaltura.org and your Nginx port is 88 [the default non-SSL port when configuring kaltura-nginx], then the update statement would be:
```
mysql> UPDATE delivery_profile SET url = REPLACE(url, 'http://test.kaltura.org:88', 'https://test.kaltura.org:8443') WHERE url LIKE 'http://test.kaltura.org:88/%';
```

If your Kaltura API endpoint is over SSL and you are using a port different than 443, you should also edit the nginx.conf file [/etc/nginx/nginx.conf in the RPM package, /opt/kaltura/nginx/conf/nginx.conf in deb]  so that the ```server``` directive includes a port, like so:
```
http {
        upstream kalapi {
                server $KALTURA_BASE_ENDPOINT:$KALTURA_BASE_ENDPOINT_PORT;
        }
	...
}
```
And then restart the Nginx daemon with:
```
# service kaltura-nginx restart
```

**It is important to note that if your Kaltura API base endpoint [service URL] is configured over SSL, Nginx must also be configured over SSL, otherwise, modern browsers will block the requests.**
