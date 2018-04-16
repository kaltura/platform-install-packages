# Kaltura S3 and CloudFront Integration Guide

**THIS DOCUMENT IS A WORK IN PROGRESS. Contributions are most welcome.**

## Configuring an S3 Bucket
**NOTE: Before creating a bucket, you need to create an IAM user and generate an access key and secret. 
To do so, go to the [IAM management console](https://console.aws.amazon.com/iam/home#/home).**

Go to the [S3 management console](https://s3.console.aws.amazon.com/s3/home) and create the bucket.
S3 offers automatic content encryption and other services that this guide does not cover. 
When creating the bucket, you may want to enable the "Object-level logging" and "Server access logging" options for auditing purposes but in order for the Kaltura integration to work, none of the options under the "Set Properties" configuration view are needed. 
Under "Set Permissions", the default values can be left as they are. 
After creating the bucket, you will need to add an access policy. Go to the ```bucket configuration->Permissions->Bucket Policy```.

Amazon has a [Policy Generator](http://awspolicygen.s3.amazonaws.com/policygen.html) you can use to generate the policy JSON.
The actions you should allow are:
```
s3:GetObject
s3:ListBucket
s3:PutObject
```

Here is a sample policy generated for a bucket called ```my_ce_bucket``` that allows the ```ce-user``` to perform the actions above:
```json
    "Version": "2012-10-17",
    "Id": "Policy0",
    "Statement": [
        {
            "Sid": "Stmt0",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::AWS-account-ID:user/ce-user" },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my_ce_bucket/*"
        },
        {
            "Sid": "Stmt1",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::AWS-account-ID:user/ce-user" },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::my_ce_bucket"
        },
        {
            "Sid": "Stmt2",
            "Effect": "Allow",
            "Principal": { "AWS": "arn:aws:iam::AWS-account-ID:user/ce-user" },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::my_ce_bucket/*"
        }
    ]
}
```
You can obtain the user's principle ID from the IAM console, under ```User ARN```.

## Configuring a Kaltura S3 Remote Storage Profile
In order to push the uploaded media content to the S3 bucket, you will need to create a Remote Storage profile.
Log into the Admin Console and navigate to Publishers->Your Partner->Profiles->Remote Storage.
In the ```Protocol``` selectbox, choose ```Amazon S3``` and click on "Create New" and provide the below inputs:

- ```Remote Storage Name```:  a meaningful name for this profile
- ```Storage URL```: https://$BUCKET_NAME.s3.amazonaws.com [in our example https://my_ce_bucket.s3.amazonaws.com]
- ```Storage Base Directory```: if you want the Kaltura asset FS structure to start from the bucket's root, simply input the bucket's name here. If you want the files to be placed under a designated dir inside your bucket, concat that to the bucket's name.
For example, assuming ```Kaltura Path``` is the path manager used, inputting ```my_ce_bucket/kaltura``` will cause the FS tree inside the ```my_ce_bucket``` bucket to look like this:
```kaltura/content/entry/data```
- ```Path Manager```: Kaltura allows you to define an alternative FS layout for the media assets. This howto will not cover this option and all configuration directives here assume ```Kaltura Path``` is being used.
- ```Storage Username```: the IAM Access key ID for your desired user [ce-user in our example]
- ```Storage Password```: the IAM Access key secret for your desired user [ce-user in our example]
- ```S3 Region```: the AWS region where your bucket resides [you were prompted about this when creating the bucket].
For a list of region IDs, see https://docs.aws.amazon.com/general/latest/gr/rande.html under the header "Amazon API Gateway".
- ```Server-Side Encryption(SSE) Type```: as mentioned previously S3 supports the automatic encryption of content, this guide assumes you have not enabled that option
- ```SSE KMS Key ID```: leave empty if encryption was not enabled
- ```Signature Type```: use the default [v4]
- ```Service endpoint```: leave empty

The S3 remote storage configuration includes additional options which we will not cover at the moment. After inputting the above params, click on "Save".


## Configuring a CloudFront Distribution


## Nginx VOD Configuration
By default, kaltura-nginx is configured to work in mapped mode against your Kaltura Server. Meaning the files will be served from ```/opt/kaltura/web```, which may be a local dir on one of the server's disks or a remote volume mounted on each of the front and batch nodes [in the event of a cluster]. You can modify the Nginx configuration so that it fetches the media files from a CF endpoint.

The paths for the Nginx conf files vary between the deb and RPM packages. For RPM, the main file is ```/etc/nginx/nginx.conf```, for deb ```/opt/kaltura/nginx/conf/nginx.conf```, the Nginx and module versions are the same and so, regardless of the packaging format, apart from the paths, the contents should be the same.
Below is a very basic example of how to fetch the files from a CF endpoint but the same can be used with other vendors, of course. 

**IMPORTANT NOTE:
The below example assumes the S3 bucket is public and doesn't require a token but naturally, you can and SHOULD modify it if authorisation is required.**

ngnix.conf:
```
include /etc/nginx/conf.d/main.conf;

http {
        upstream media {
                server somecfspace.cloudfront.net;
                keepalive 32;
        }

        include /etc/nginx/conf.d/http.conf;

        # vod remote settings
        vod_mode remote;
        vod_upstream_location /media_proxy;

        server {
                listen 88;
                server_name your.nginx.server.name;
                include /etc/nginx/conf.d/server.conf;
        }
}

```

main.conf:
```
user  kaltura;
worker_processes  auto;

error_log  /opt/kaltura/log/nginx/kaltura_nginx_errors.log;

pid             /var/run/nginx.pid;

events {
        worker_connections  1024;
        worker_aio_requests 512;
        multi_accept on;
        use epoll;
}

```

http.conf:
```
include    mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $bytes_sent $request_time "$http_referer" "$http_user_agent" "-" - '
                '"$sent_http_x_kaltura" "$http_host" $pid $sent_http_x_kaltura_session - '
                '$request_length "$sent_http_content_range" "$http_x_forwarded_for" '
                '"$http_x_forwarded_server" "$http_x_forwarded_host" "$sent_http_cache_control" '
                '$connection ';

        access_log /opt/kaltura/log/nginx/kaltura_nginx_access.log main;

        # general nginx tuning
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;

        keepalive_timeout 60;
        keepalive_requests 1000;
        client_header_timeout 20;
        client_body_timeout 20;
        reset_timedout_connection on;
        send_timeout 20;

        # manifest compression
        gzip on;
        gzip_types application/vnd.apple.mpegurl video/f4m application/dash+xml text/xml text/vtt;
        gzip_proxied any;

        # shared memory zones
        vod_metadata_cache metadata_cache 512m;
        vod_response_cache response_cache 64m;
        vod_performance_counters perf_counters;

        # common vod settings
        vod_last_modified 'Sun, 19 Nov 2000 08:52:00 GMT';
        vod_last_modified_types *;
        vod_expires 100d;
        vod_expires_live 30;
        vod_expires_live_time_dependent 3;
        vod_align_segments_to_key_frames on;
        vod_output_buffer_pool 64k 32;
```

server.conf:
```

                # internal location for vod subrequests
                location ~ /media_proxy/[^/]+/(.*) {
                        internal;
                        proxy_pass http://media/$1;
                        proxy_http_version 1.1;
                        proxy_set_header Host somecfspace.cloudfront.net;
                        proxy_set_header Connection "";
                }

                # base locations
                include /etc/nginx/conf.d/base.conf;

                # serve flavor progressive
                location /pd/ {
                        vod none;

                        directio 512;
                        output_buffers 1 512k;

                        include /etc/nginx/conf.d/cors.conf;
                }

                # serve flavor HLS
                location /hls/ {
                        vod hls;
                        vod_bootstrap_segment_durations 2000;
                        vod_bootstrap_segment_durations 2000;
                        vod_bootstrap_segment_durations 2000;
                        vod_bootstrap_segment_durations 4000;

                        include /etc/nginx/conf.d/cors.conf;
                }

                # serve flavor DASH
                location /dash/ {
                        vod dash;
                        vod_segment_duration 4000;
                        vod_dash_manifest_format segmenttemplate;
                        vod_manifest_duration_policy min;

                        include /etc/nginx/conf.d/cors.conf;
                }

                # serve flavor HDS
                location /hds/ {
                        vod hds;
                        vod_segment_duration 6000;
                        vod_segment_count_policy last_rounded;

                        include /etc/nginx/conf.d/cors.conf;
                }

                # serve flavor MSS
                location /mss/ {
                        vod mss;
                        vod_segment_duration 4000;
                        vod_manifest_segment_durations_mode accurate;

                        include /etc/nginx/conf.d/cors.conf;
                }

                # static files (crossdomain.xml, robots.txt etc.) + fallback to api
                location / {
                        root   @STATIC_FILES_PATH@;
                }

```

cors.conf:

```
add_header Access-Control-Allow-Headers "Origin,Range,Accept-Encoding,Referer,Cache-Control";
add_header Access-Control-Expose-Headers "Server,Content-Length,Content-Range,Date";
add_header Access-Control-Allow-Methods "GET, HEAD, OPTIONS";
add_header Access-Control-Allow-Origin "\*";
```

base.conf:
```nginx
# nginx status page
location = /nginx_status {
stub_status on;
access_log off;
}

# vod status page
location = /vod_status {
vod_status;
access_log off;
}

# redirect server error pages to the static page /50x.html
error_page 500 502 503 504 /50x.html;

location = /50x.html {
root   html;
}
```

For detailed documentation of the VOD module configuration, see https://github.com/kaltura/nginx-vod-module.


## Alternative media assets FS layout
**IMPORTANT NOTE: 
The steps below are only necessary in the event you'd like to change the default FS layout.**

In the Remote Storage profile configuration view, there is a selectbox called "Path Manager".
Set that to ```XSL Path``` and go to the ```Advanced``` section.
There, in the ```Path Manager Params (JSON)``` textarea, you can input a JSON that contains a XSL describing an alternative structure.
For example, inputting this:

```xsl
[{"key":"path_format","value":"<xsl:value-of select=\"$partnerId\" \/><xsl:text>\/<\/xsl:text><xsl:value-of select=\"php:function('date', 'Y', $currentTime)\"\/><xsl:text>-<\/xsl:text><xsl:value-of select=\"php:function('date', 'm', $currentTime)\"\/><xsl:text>\/<\/xsl:text><xsl:value-of select=\"php:function('date', 'd', $currentTime)\"\/><xsl:text>\/<\/xsl:text><xsl:value-of select=\"$entryId\" \/><xsl:text>_<\/xsl:text><xsl:value-of select=\"$objectId\"\/><xsl:text>.<\/xsl:text><xsl:value-of select=\".\/content\/@extension\"\/>","relatedObjects":null}]
```

Would create the following structure under your remote volume's root:

$REMOTE_STORAGE_ROOT/$PARTNER_ID/%Y-%m/%d/$ENTRY_ID_$FLAVOR_ID.$FILE_EXT

For example:

$REMOTE_STORAGE_ROOT/101/2018-01/10/0_mka2lp86_0_lfo55tdw.mp4

**This will only take affect when uploading new entries. Previously uploaded entries will still be served from the original location. You can move them and then adjust the file_sync table but it's a risky operation that should be carefully tested outside of production and I'd advise against it unless it is absolutely necessary.**

