Currently we have the following packages:

kaltura-base - this package is needed for all main Kaltura server roles, i.e:
kaltura-batch
kaltura-front
kaltura-sphinx
kaltura-dwh

The base package includes the entire source code.
The Kaltura architecture is such that you can configure all roles on one machine, or a machine per role or any number of roles according to your needs.
This means you may choose to configure both front and DWH to run on the same machine, for instance.
The package segmentation ensures you will be able to get the flexibility of various setups by simply deciding which package you wish to install where.
You can also reconfigure a node to assume additional or different roles after the initial installment.

Since RPM does not allow interactive configuration prompting and the Kaltura installation does require user input for various params such as VIP hostname, DB host, passwds, etc, the following packages will also be included:
kaltura-mysql-config
kaltura-postinst

The flow would be:
0. Install the packages matching the server roles you wish to assign
1. Run post install scripts to configure the ENV.

For dpkg, which does have a good interactive prompting mechanism built it, these packages will not be needed.
The ability to configure/reconfigure a package is already built into the Debain installation tools.

We also have a meta package called kaltura-server which depends on kaltura-batch, kaltura-front, kaltura-sphinx, kaltura-dwh and kaltura-widgets.
This will allow an easy installment of an 'all in one' instance. Saving the user from the need to manually specify all packages needed for this purpose.

kaltura-ffmpeg, kaltura-ffmpeg-aux - packages supply ffmpeg built by Kaltura with the specific versions and compilation flags needed to fully utilize it in an optimized manner.
These two packages depend on quite a few libraries, seeing how the RHEL/CentOS/FC official repos do not offer these packages, we created spec files for them and built the RPMs on the same ENV.
These packages will be part of the official Kaltura repo and will all reside under the /opt/kaltura tree. 
This is important because we do not wish to make users add unofficial repos in order to install the Kaltura platform but, on the other hand, we also wish to allow them to use these additional repos if they wish, w/o causing conflicts with our own packages.
The supporting packages for ffmpeg are:

kaltura-a52dec
kaltura-faac
kaltura-lame
kaltura-libass
kaltura-x264
kaltura-rtmpdump
kaltura-opencore-amr

The kaltura-base package utilizes a watchdog tool called monit, we therefore provide:
kaltura-monit
Again, the package is installed under the /opt/kaltura tree.

The kaltura-batch and kaltura-front packages also require a few dependencies not found in the official repos, these are:

PHP extensions:
php-mcrypt - needed for KS generation and handling
kaltura-libmcrypt - needed for the PHP Mcrypt extension
php-pecl-memcached - memcache bindings
kaltura-libmemcached - needed for the PHP Memcached extension
php-pecl-ssh2 - needed for sFTP drop folder configurations mostly.

Flash widgets:
kaltura-widgets - a meta package which depends on:
kaltura-kcw
kaltura-kdp
kaltura-kdp3
kaltura-kdp3wrapper
kaltura-kmc
kaltura-krecord
kaltura-kvpm

In addition, for some sFTP configs, the sshpass package is needed:
kaltura-sshpass

The kaltura-dwh package requires Penthao, it is supplied by:
kaltura-pentaho

Red5 support is available with this package:
kaltura-red5

Next steps:
===========
We are currently at is finalizing the post install scripts.
We will then be ready for beta testing of the RPMs.
A repository will be placed on Akamai's CDN, allowing access from www.

In parallel, work on the deb packages will commence. The outline is already exists and the package hierarchy and post install steps are the same so the variation is mostly in the packaging spec files format.
This means we should be able to rapidly work on these and release them sometime next week.

