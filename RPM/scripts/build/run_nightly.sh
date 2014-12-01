#!/bin/bash - 
#===============================================================================
#          FILE: run.sh
#         USAGE: ./run.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/01/14 10:17:05 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
mkdir -p tmp
KALTURA_SERVER_VERSION=`curl https://api.github.com/repos/kaltura/server -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`
wget https://github.com/kaltura/server/archive/$KALTURA_SERVER_VERSION.zip -O /home/jess/rpmbuild/SOURCES/$CORE_NIGHTLY_V.zip 
unzip -j /home/jess/rpmbuild/SOURCES/$KALTURA_SERVER_VERSION.zip server-$CORE_NIGHTLY_V/configurations/base.ini -d "tmp/"
KMC_VERSION=`grep ^kmc_version tmp/base.ini |awk -F "=" '{print $2}'|sed 's@\s*@@g'`
KMC_LOGIN_VERSION=`grep ^kmc_login_version tmp/base.ini |awk -F "=" '{print $2}'|sed 's@\s*@@g'`
HTML5_APP_STUDIO_VERSION=`grep ^studio_version tmp/base.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
HTML5LIB_VERSION=`curl https://api.github.com/repos/kaltura/mwembed -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`
