#!/bin/bash
#===============================================================================
#          FILE: kaltura-async-uploader-configure.sh
#         USAGE: ./kaltura-async-uploader-configure.sh
#   DESCRIPTION: post install configure kaltura-async-uploader
#       OPTIONS: ---
#       LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Igor Shevach <igor.shevach@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 22/02/15 09:23:34 EST
#      REVISION:  ---
#===============================================================================

if[ ! -r $1 ]; then
    echo "no ini file path provided! exiting"
    exit 1

 fi

. $1

cd $ASYNC_CLIENT_APP_DIR
ant -Dproperties_file_path=/opt/kaltura/app/configurations/ecdn.ini
/etc/init.d/WowzaStreamingEngine stop >> /dev/null 2>&1
/etc/init.d/WowzaStreamingEngine start

