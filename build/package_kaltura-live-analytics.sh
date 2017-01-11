#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura-live-analytics.sh
#         USAGE: ./package_kaltura-live-analytics.sh
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/14/14 11:46:43 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi
wget $LIVE_ANALYTICS_WAR_URI -O $RPM_SOURCES_DIR/KalturaLiveAnalytics.war 
wget $LIVE_ANALYTICS_DRIVER_URI -O $RPM_SOURCES_DIR/live-analytics-driver.jar
wget $LIVE_ANALYTICS_REGISTER_FILE_URI -O $RPM_SOURCES_DIR/register-file.jar
wget $LIVE_ANALYTICS_SCHEMA_FILE -O $RPM_SOURCES_DIR/create_cassandra_tables.cql


echo "Placed KalturaLiveAnalytics.war in $RPM_SOURCES_DIR/KalturaLiveAnalytics.war"
echo "Placed live-analytics-driver.jar in $RPM_SOURCES_DIR/live-analytics-driver.jar"
echo "Placed register-file.jar in $RPM_SOURCES_DIR/register-file.jar"
echo "Placed create_cassandra_tables.cql in $RPM_SOURCES_DIR/create_cassandra_tables.cql"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$LIVE_ANALYTICS_PACKAGE_NAME.spec
fi
