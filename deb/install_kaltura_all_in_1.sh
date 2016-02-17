#!/bin/sh -e
set -e
wget -O - http://installrepo.kaltura.org/repo/apt/debian/kaltura-deb.gpg.key|apt-key add -
echo "deb [arch=amd64] http://installrepo.kaltura.org/repo/apt/debian jupiter main" > /etc/apt/sources.list.d/kaltura.list

# aptitude has a more advanced API then apt-get and is better at resolving deps. For some reason, it is not installed on all deb based system so lets see if we haveit.

if which aptitude;then
        APT_TOOL="aptitude -y"
else
        APT_TOOL="apt-get -y"
fi
$APT_TOOL update
$APT_TOOL install lsb-release 
# for Debian, the non-free repo must also be enabled
# Ubuntu: You must also make sure the multiverse repo is enabled in /etc/apt/sources.list
# Debian Jessie [8]: You must also make sure the following Wheezy repos are enabled in /etc/apt/sources.list
DISTRO=`lsb_release -s -i`
if [ "$DISTRO" = 'Ubuntu' ];then
	apt-add-repository multiverse
elif [ "$DISTRO" = 'Debian' ];then
	$APT_TOOL install software-properties-common
	apt-add-repository non-free
	CODENAME=`lsb_release  -s -c`
	if [ "$CODENAME" != 'wheezy' ];then
		apt-add-repository "deb http://ftp.debian.org/debian/ wheezy main"
		apt-add-repository "deb http://security.debian.org/ wheezy/updates main"
	fi
fi
$APT_TOOL install mysql-server
$APT_TOOL install kaltura-postinst
$APT_TOOL install kaltura-base
$APT_TOOL install kaltura-widgets kaltura-html5lib kaltura-html5-studio
$APT_TOOL install kaltura-front
$APT_TOOL install kaltura-sphinx
$APT_TOOL install kaltura-db
$APT_TOOL install kaltura-batch
$APT_TOOL install kaltura-dwh
$APT_TOOL install kaltura-nginx
/etc/init.d/kaltura-nginx start

