# Required Open Ports to run Kaltura
IMPORTANT NOTE: these are the default ports for the mentioned protocols. Of course, you may choose different ports, in which case you will need to adjust accordingly.

* On the API, apps (KMC/Admin Console/MediaSpace) and Batch machines - Ports 80/TCP (in the event you intend to use http) and 443/TCP (in the event you intend to use https).  
* On the front and btach machiens, you'll also need an email service, port 25/TCP by default (depending on what method you use) on the machine that will handle mail for your Kaltura server.
* If you plan on using a streaming server (e.g. Red5, F/AMS, Wowza) - you'll need 1935 (RTMP), 8088 (RTMPT), 5080 (Red5 Admin), 1936 (debug).  
* If you're planning to use Remote Storage/Drop Folders - you'll need to enable access in one of the following protocols FTP - port 21/TCP, SFTP - port 22/TCP, etc.  
* If you'll use NFS - port 2049/TCP+UDP and 111/TCP+UDP for portmap.  
* On your MySQL and DWH machines - port 3306/TCP.  
* On your Sphinx machine - ports 9312/TCP.   
* If you need LDAP with MediaSpace, you'll need port 636/TCP [LDAPs] or port 389/TCP [LDAP].  

**If you are installing an all-in-one, all these ports should be open on the machine**
