# Live Streaming with Nginx and the RTMP module
Kaltura CE includes the kaltura-nginx package, which is compiled with the [Nginx RTMP module](https://github.com/arut/nginx-rtmp-module).

## Nginx RTMP Configuration
The paths to the configuration files for kaltura-nginx vary depending on rather you use the Deb or the RPM package.

For deb, the main file is here:
```
/opt/kaltura/nginx/conf/nginx.conf
```
For RHEL:
```
/etc/nginx/nginx.conf
```

```
rtmp {
    server {
      listen 1935; # Listen on standard RTMP port
      chunk_size 4000;

        # This application is to accept incoming stream
        application kLive {
          live on; # Allows live input from above
          dash on; # create DASH fragments and manifest
        # Sets MPEG-DASH playlist and fragment directory
          dash_path /var/tmp/dashme; 
          hls on; # create HLS fragments and manifest
          hls_cleanup on;
          hls_sync 100ms;
          hls_fragment 2s;
        # Sets HLS playlist and fragment directory
          hls_path /var/tmp/hlsme/;
     }
   }
}
```

*IMPORTANT NOTE: when balancing between nodes, the hls_path and dash_path directives must point to directories that are shared between the Nginx nodes*

## Creating a Live Stream Entry
To create the Kaltura Live Entry that will make use of the HLS stream, go to to ```KMC->Upload->Live Stream Entry```.

For Live Stream Type, select ```Manual Live Stream URLs```, provide a meaningful name for the entry, for example ```My Live Test```, and input ```http://$YOUR_NGINX_HOST:$NGINX_PORT/hlsme/$DESIRED_STREAM_NAME.m3u8``` in the "HLS stream URL" text box.

## Streaming
Streaming can be done using various tools. A very basic FFMPEG CLI command to stream is:
```
ffmpeg -re -i /path/too/your/video/file -c copy -f flv \
"rtmp://$NGINX_HOST:$PORT/kLive/$DESIRED_STREAM_NAME"
```
In addition, one can make use of the [OBS Studio](https://obsproject.com) which is FOSS and makes use of the FFMPEG libs.
Any other tool capable of streaming using the RTMP protocol should work.

## Testing playback
Now, all that's left is playing the stream. 
Go to ```KMC->your Live Stream Entry->Actions->Preview & Embed```, select your HTML5 player from the list and hit play:)
In the same view, you will also find the HTML code needed to embed the player onto external websites.

## Additional Nginx RTMP configuration
An important next step is to restrict publishing access [and perhaps playback too, depending on your needs]. 
To that end, see https://github.com/arut/nginx-rtmp-module/wiki/Directives#access

## Nginx's RTMP module and the Kaltura API
Using the Nginx RTMP module exec hooks, we now support auto provisioning a Kaltura Live entry upon initiating an RTMP stream.
A VOD recording of the stream is automatically uploaded as a separate entry once the streaming session concludes.
The VOD entry name will be a concatenation of the stream's original name and the string '-VOD'. 

### Kaltura entry auto provisioning (requires Kaltura CE 14.4.0 and above)
When streaming, the following params must be passed to the Nginx RTMP endpoint:
> partner_id
> partner_secret - the partner's ADMIN secret
> service_url - the Kaltura endpoint WITHOUT the protocol (http[s])
> nginx_endpoint - the Nginx hostname
> is_ssl - set to 'true', 'y' or 1 if the connection is to be done over SSL
> entry_name - the Kaltura live entry name

For example:
```sh
$ ffmpeg -re -i /path/to/vid/file -c:v copy -c:a copy -f flv -rtmp_live 1 \
 "rtmp://$NGINX_HOST:$NGINX_RTMP_PORT/kLive/$STREAM_NAME?partner_id=103&partner_secret=somesecret&service_url=$KALTURA_ENDPOINT&nginx_endpoint=$NGINX_HOST:$NGINX_PORT&entry_name=my_entry&is_ssl=true"
```

By default, `$NGINX_RTMP_PORT` is 1935. For SSL, `$NGINX_PORT` is 8443, otherwise, it's 88.
All these defaults may be changed during the kaltura-nginx configuration phase.

### Adaptive bitrate support
This can be accomplished by using `ffmpeg` to transform the source stream into 4 separate streams, each with a different bitrate.
The configuration is disabled by default as the operation is CPU and RAM intensive. If you opt to enable it, ensure you have sufficient HW resources.

To enable, edit `/etc/nginx/nginx.conf` [RPM] or `/opt/kaltura/nginx/conf/nginx.conf` [deb], uncomment the `exec /opt/kaltura/bin/ffmpeg` block under `application kLive` and reload the daemon.

