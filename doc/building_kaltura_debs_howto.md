Required debs for build
=======================
build-essential git svn wget dos2unix

Extra repos
===========
Debian build ENV, the non-free repo must be enabled.

For a Debian Jessie ENV, you must also make sure the following Wheezy repos are enabled:
```
deb http://ftp.debian.org/debian/ wheezy main
deb http://security.debian.org/ wheezy/updates main
```

Ubuntu build ENV: You must also make sure the multiverse repo is enabled.


GIT repo
========
$ git clone https://github.com/kaltura/platform-install-packages

dir structure
========================
~/sources

platform-install-packages/build dir
================================================
* sources.rc - this file has the ENV vars needed for building from sources. When versions of components are upgraded, they should be modified there.

* packager.rc - should have the following vars:
```
PACKAGER_NAME="First Last"
PACKAGER_MAIL="packager@example.com"
```

* package_*.sh - each component has a wrapper script that fetches the sources from the needed version and packages them so that the RPM can be built.

You will need to edit sources.rc and change:
```
PACKAGER_NAME=""
PACKAGER_MAIL=""
SVN_USER=""
```
You may also change these two although defaults should be fine:
TMP_DIR=/tmp
SOURCE_PACKAGING_DIR=~/sources

And of course:
```
$ mkdir $SOURCE_PACKAGING_DIR
```
Utility scripts
===============
under build/deb-specific:

* bounce_core_ver.sh - utiliy script to bounce core version for kaltura-base, kaltura-front and kaltura-batch. Should be run whenever a new branch is created

Deployment instructions
================================
Each deployment has instructions here:
https://kaltura.atlassian.net/wiki/display/QAC/QA.Core+Production+Deployments
That includes the new versions for updated components as well as PHP/SQL scripts to run.
The versions should be updated in platform-install-packages/build/sources.rc

Step by step release process
============================
1. read instructions at: https://kaltura.atlassian.net/wiki/display/QAC/QA.Core+Production+Deployments

2. update versions in platform-install-packages/build/sources.rc.

3. run platform-install-packages/build/deb-specifc/bounce_core_ver.sh $NEW_VER $DIST
This will update the Core version in the various relevant spec files. $DIST is the release codename, for example, 10.n.n codename is 'jupiter'.

4. update specs for additional components according to versions in the deployment doc, i.e:
if KMC is of a new version then update deb/kaltura-kmc/debian/changelog, for kdp3, update deb/kaltura-kdp3/debian/changelog, etc

5. Add changelog entries according to what is stated in the deployment doc to each component.

6. for the modified components, run the respective package_*.sh script, for instance, if KMC was updated run:
platform-install-packages/build/package_kaltura_kmc.sh
for KDP3 run:
platform-install-packages/build/package_kaltura_kdp3.sh
and so on.
If a new package is introduces, make sure to create a wrapper script for it as well. 

7. build the deb:
```
cd kaltura-$PACKAGE_NAME && dpkg-buildpackage -b -uc
```
if the source retrieval succeeded but build failed, you can simply correct what needs correction and then run:
```
$ dpkg-buildpackage -b -uc
```
once more, no need to repackage for that.

8. once all debs are built, use: 
$ cd /root/repo/path && sudo reprepro --basedir=. includedeb jupiter ~jess/sources/platform-install-packages/deb/path/to/deb

9. run sanity on the test machine using kaltura-sanity.sh and make sure all passes successfully.
