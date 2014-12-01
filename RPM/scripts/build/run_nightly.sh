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
NIGHTLY_V=`curl https://api.github.com/repos/kaltura/server -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`
wget https://github.com/kaltura/server/archive/$NIGHTLY_V.zip -O /home/jess/rpmbuild/SOURCES/$NIGHTLY_V.zip 
unzip -j /home/jess/rpmbuild/SOURCES/$NIGHTLY_V.zip server-$NIGHTLY_V/configurations/base.ini -d "tmp/"
KMC_VER=`grep ^kmc_version tmp/base.ini |awk -F "=" '{print $2}'|sed 's@\s*@@g'`
KMC_LOGIN_VER=`grep ^kmc_login_version tmp/base.ini |awk -F "=" '{print $2}'|sed 's@\s*@@g'`
STUDIO_VER=`grep ^studio_version tmp/base.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
# if kmc_version -ne version in sources.rc
KMC_BRANCH=`curl https://api.github.com/repos/kaltura/kmc -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/'| sed 's@\s*@@g'`

