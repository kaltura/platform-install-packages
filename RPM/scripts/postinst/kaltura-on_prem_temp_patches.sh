#!/bin/bash

# Remove KMC's real time dashboard --------------------------------------------------------------------------------
FILE_NAME='/opt/kaltura/web/flash/kmc/v5.39.6/xml/permissions_uiconf.xml'
REPLACE_STR='FEATURE_LIVE_STREAM'
NEW_STR='FEATURE_LIVE_STREAM-DISABLED-UNTIL-RTA'
KMC_VER=`rpm -qa kaltura-kmc --queryformat %{version}`
LINE_NUM=`grep -n '<tab id="realTimeDashboard">' /opt/kaltura/web/flash/kmc/v5.39.6/xml/permissions_uiconf.xml | cut -d':' -f1`
LINE_NUM=$((LINE_NUM+1))
sed -i $((LINE_NUM))s/$REPLACE_STR/$NEW_STR/ /opt/kaltura/web/flash/kmc/$KMC_VER/xml/permissions_uiconf.xml
php /opt/kaltura/app/deployment/uiconf/deploy_v2.php --ini=/opt/kaltura/web/flash/kmc/$KMC_VER/config.ini
