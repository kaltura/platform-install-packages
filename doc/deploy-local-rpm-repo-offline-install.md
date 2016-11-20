# Deploy Local Repository for Offline Install
This quick guide describes the steps required for creating and deploying Kaltura Install Packages Repository locally for offline installations (for cases where the environment you're deploying on is not connected to the internet).

### Before You Get Started Notes

* Whenever you see `#` in the beginning of a command line, this means you should run the command as root.
* Follow the steps in this document in the order they are provided.
* This guide refers to the RPM packages only.
* [Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.


## Download the repository
```
# wget -r http://installrepo.origin.kaltura.org/releases
# cp -r installrepo.origin.kaltura.org/releases/$VERSION/RPMS  /path/to/local/repo
```

If you want to only mirror one version, you can also do:
```
wget -r --level=0 -E --ignore-length --reject="index.html*" -x -k -p -erobots=off -np -N http://installrepo.origin.kaltura.org/releases/$VERSION/
```

## Create the local repository file
This step is performed on each machine you're deploying Kaltura on.   
Create the `/etc/yum.repos.d/kaltura.repo` file.    
Add to this file the following text while changing the `%LOCAL_PATH%` accordingly.    
    
`%LOCAL_PATH%` will be either a local file-system path to where the repository was downloaded to, or it can be a local apache server url.    
For example:   

* If your repository files are in an Apache server, use:
`baseurl=http://what.ever.com/path/to/repo/relative/to/docroot`
* If your repository files are local or mounted FS:
`baseurl=file:///somewhere/local/or/mounted/on/your/fs`

Make sure to replace this file accordingly when creating the `kaltura.repo` file.   

```
[Kaltura]
name = Kaltura Server
baseurl = %LOCAL_PATH%
gpgcheck = 0
enabled = 1

[Kaltura-noarch]
name = Kaltura Server arch independent
baseurl = %LOCAL_PATH%
gpgcheck = 0
enabled = 1
```

## Install Kaltura
Follow the desired install guide ([cluster deployment](https://github.com/kaltura/platform-install-packages/blob/master/doc/rpm-cluster-deployment-instructions.md) or [all-in-one install](https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md)), skipping the "Auto Set the Kaltura install repository URLs" step.
