### Setting up Amazon CloudFront CDN for RTMP

1. Go to [Amazon Cloudfront CDN Access Panel] (https://console.aws.amazon.com/cloudfront/home)

2. Create a new **Distribution** of type **RTMP**, and Origin Domain Name select your bucket from list

3. Distribution State want to be **Enabled**

4. Click on **Create Distribution**

5. Copy your CloudFront RTMP domain name (example: s22xxxxxxxxxxxx.cloudfront.net) for later use.

![selection_015](https://raw.githubusercontent.com/blackyboy/Centos-Linux-Stuffs/master/setup-images/setting_up_amazon_cloudfront_cdn_for_rtmp.png)


Next we need to configure the Remote Storage Profile. In order to do this, we must click on the partner’s left drop-down box (under **Profiles**) and select **Remote Storage**. You should see the **Remote Storage Profiles** page for your publisher (If you haven’t yet set up any remote storage profiles, the list should be empty).

There was our s3 storage will be listed as we have done in above Step, 

1. Select action Click **configure** 

2. Under Delivery Details Below http & https we need to enter the rtmp url of cloudnfront
Prefix must be our Directory which was created in s3 bucket

Note : There is no slash after /st
Note : There is no slash after /kaltura

```
RTMP Delivery Base URL:   rtmp://s22xxxxxxxxxxx.cloudfront.net/cfx/st

RTMP stream URL prefix:   /kaltura
```

![selection_011](https://raw.githubusercontent.com/blackyboy/Centos-Linux-Stuffs/master/setup-images/setting_up_amazon_cloudfront_cdn_for_rtmp_1.png)


3. Save the Remote Storage Profile

This will make works both RTMP & RTMPE Video Streaming.

Bunch of thanks to @jessp01 from Kaltura team for guiding me.
