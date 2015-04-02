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

if [ ! -r $KALTURA_ECDN_CONFIG_FILE_PATH ]; then
    echo "no ini file path provided! exiting"
    exit 1
 fi

. $KALTURA_ECDN_CONFIG_FILE_PATH

if [  -r $BIN_DIR/kaltura_media_server_async_processi.template.sh ]; then
  sed -e "s#@KALTURA_ECDN_CONFIG_FILE_PATH@#$KALTURA_ECDN_CONFIG_FILE_PATH#g" $BIN_DIR/kaltura_media_server_async_process.template.sh > $BIN_DIR/kaltura_media_server_async_process.sh
   ln -sf  $BIN_DIR/kaltura_media_server_async_process.sh /etc/profile.d/
fi

cd $ASYNC_CLIENT_APP_DIR
ant
/etc/init.d/WowzaStreamingEngine stop >> /dev/null 2>&1
/etc/init.d/WowzaStreamingEngine start >> /dev/null 2>&1

