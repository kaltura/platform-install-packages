#!/bin/sh

BASE_DIR=/opt/kaltura/
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
	. $ANSFILE
	export ANSFILE
fi

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	echo "Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
echo "Running base config...

"
$BASE_DIR/bin/kaltura-base-config.sh "$ANSFILE" 
if [ $? -ne 0 ];then
	echo "$BASE_DIR/bin/kaltura-base-config.sh failed:( You can re-run it when the issue is fixed."
	exit 1
fi

RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo "Could not find $RC_FILE so, exiting.."
	exit 2
fi
. $RC_FILE
if [ $? -ne 0 ];then
	echo "$BASE_DIR/bin/kaltura-sphinx-config.sh failed:( You can re-run it when the issue is fixed."
	exit 3 
fi
echo "Running FrontEnd config...

"

$BASE_DIR/bin/kaltura-front-config.sh "$ANSFILE" 
if [ $? -ne 0 ];then
	echo "$BASE_DIR/bin/kaltura-front-config.sh failed:( You can re-run it when the issue is fixed."
	exit 2 
fi
echo "Running Sphinx config...

"
bash -e $BASE_DIR/bin/kaltura-sphinx-config.sh "$ANSFILE" 
echo "use kaltura" | mysql -h$DB1_HOST -P$DB1_PORT -u$SUPER_USER -p$SUPER_USER_PASSWD mysql 2> /dev/null
if [ $? -ne 0 ];then
	echo "

Configuring your Kaltura DB...

"
$BASE_DIR/bin/kaltura-db-config.sh $DB1_HOST $SUPER_USER $SUPER_USER_PASSWD $DB1_PORT $SPHINX_HOST
	RC=$?
	if [ $RC -ne 0 ];then
		if [ $RC = 111 ];then
			echo "$BASE_DIR/bin/kaltura-db-config.sh $DB1_HOST $SUPER_USER $SUPER_USER_PASSWD $DB1_PORT failed when trying to populate the DB.
It tried reaching $SERVICE_URL/api_v3/index.php?service=system&action=ping and couldn't.
This probably means you have either inputted and bad service URL or have yet to configure your Apache.
To configure your Apache, please use $BASE_DIR/bin/kaltura-front-config.sh.
Since the schema creation succeeded, you can skip that part by running:
# POPULATE_ONLY=1 $BASE_DIR/bin/kaltura-db-config.sh $DB1_HOST $SUPER_USER $SUPER_USER_PASSWD $DB1_PORT 

Please run it manually to debug the issue.
You may run $0 again once done."
			exit 111
		else
			echo "We failed on something else.."
			exit 112
		fi
	fi
fi


echo "Running Batch config...

"
$BASE_DIR/bin/kaltura-batch-config.sh "$ANSFILE" 

$BASE_DIR/bin/kaltura-dwh-config.sh "$ANSFILE" 

rm -rf $APP_DIR/cache/*
rm -f $APP_DIR/log/kaltura-*.log

echo "
====================================================================================================================

Setup completed successfully! 

To access your Kaltura tools visit:
$SERVICE_URL

To begin, access the Admin Console using the Admin email and password you've entered while installing.
When logged in to the KAC, create a new publisher account to being using Kaltura.
Visit http://www.kaltura.org to join the community and get help!
Visit http://knowledge.kaltura.com to read documentation and learn more.
=====================================================================================================================
"

find $BASE_DIR/app/cache/ $BASE_DIR/log -type d -exec chmod 775 {} \; 
find $BASE_DIR/app/cache/ $BASE_DIR/log -type f -exec chmod 664 {} \; 
chown -R kaltura.apache $BASE_DIR/app/cache/ $BASE_DIR/log
send_post_inst_msg $ADMIN_CONSOLE_ADMIN_MAIL 
