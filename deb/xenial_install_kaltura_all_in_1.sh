#!/bin/sh -e
set -e

# aptitude has a more advanced API than apt-get and is better at resolving deps. For some reason, it is not installed on all deb based system so lets see if we have it.

if which aptitude;then
        APT_TOOL="aptitude -y"
else
        APT_TOOL="apt-get -y"
fi
$APT_TOOL update
$APT_TOOL install lsb-release software-properties-common
# for Debian, the non-free repo must also be enabled
# Ubuntu: You must also make sure the multiverse repo is enabled in /etc/apt/sources.list
# Debian Jessie [8]: You must also make sure the following Wheezy repos are enabled in /etc/apt/sources.list
DISTRO=`lsb_release -s -i`
CODENAME=`lsb_release -c -s`
if [ "$DISTRO" = 'Ubuntu' ];then
        apt-add-repository multiverse
elif [ "$DISTRO" = 'Debian' ];then
        apt-add-repository non-free
        CODENAME=`lsb_release  -s -c`
        if [ "$CODENAME" != 'wheezy' ];then
                apt-add-repository "deb http://ftp.debian.org/debian/ wheezy main"
                apt-add-repository "deb http://security.debian.org/ wheezy/updates main"
        fi
fi
REPO_BASE_URL="http://installrepo.kaltura.org/repo/apt"
KALTURA_DIST="naos"
wget -O - $REPO_BASE_URL/debian/kaltura-deb.gpg.key|apt-key add -
wget -O - $REPO_BASE_URL/xenial/kaltura-deb-256.gpg.key|apt-key add -
if [ $CODENAME = 'xenial' ];then
        echo "deb [arch=amd64] $REPO_BASE_URL/$CODENAME $KALTURA_DIST main" > /etc/apt/sources.list.d/kaltura.list
        $APT_TOOL install libapache2-mod-php7.0 apache2
else
        echo "deb [arch=amd64] $REPO_BASE_URL/debian $KALTURA_DIST main" > /etc/apt/sources.list.d/kaltura.list
        # for Xenial, we do not install the mysql-server package from the distro's repo because we do not support MySQL 5.7.
        # users are suggested the Percona MySQL 5.5 deb, see:
        # https://github.com/kaltura/platform-install-packages/blob/Lynx-12.19.0/doc/install-kaltura-xenial.md#mysql-install-and-configuration
        $APT_TOOL install mysql-server
fi
$APT_TOOL update
$APT_TOOL install kaltura-postinst
$APT_TOOL install kaltura-base
$APT_TOOL install kaltura-widgets kaltura-html5lib kaltura-html5-studio
$APT_TOOL install kaltura-front
$APT_TOOL install kaltura-sphinx
php /opt/kaltura/app/generator/generate.php
$APT_TOOL install kaltura-db
$APT_TOOL install kaltura-batch
$APT_TOOL install kaltura-dwh
$APT_TOOL install kaltura-nginx
/etc/init.d/kaltura-nginx start

