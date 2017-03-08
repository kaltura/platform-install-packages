# Live Streaming with Nginx and the RTMP module
Kaltura CE includes the kaltura-nginx package, which is compiled with the [Nginx RTMP module](https://github.com/arut/nginx-rtmp-module).

## Nginx RTMP Configuration
The paths to the configuration files for kaltura-nginx vary depending on rather you use the Deb or the RPM package.
For deb, the main file is here:
/opt/kaltura/nginx/conf/nginx.conf
For RHEL:
/etc/nginx/nginx.conf


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

