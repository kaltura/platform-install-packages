# Deploy local repository for offline install
This quick guide describes the steps required for creating and deploying Kaltura Install Packages Repository locally for offline installations (for cases where the environment you’re deploying on is not connected to the internet).

### Notes

1. Whenever you see `#` in the beginning of a command line, this means you should run the command as root.
1. Follow the steps in this document in the order they are provided.
1. This guide refers to the RPM packages only.


## Download the repository
```
# wget -r http://installrepo.kaltura.org/releases
# cp -r installrepo.kaltura.org/releases/$CORE_VER/RPMS  %LOCAL_PATH%
```

## Create the local repository file
This step is performed on each machine you're deploying Kaltura on.
Create the `/etc/yum.repos.d/kaltura.repo` file.
Add to this file the following text while changing the `%LOCAL_PATH%` accordingly.

`%LOCAL_PATH%` will be either a local file-system path to where the repository was downloaded to, or it can be a local apache server url.
For example:
If your repository files are in an Apache server, use:
`baseurl=http://what.ever.com/path/to/repo/relative/to/docroot`
If your repository files are local or mounted FS:
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
