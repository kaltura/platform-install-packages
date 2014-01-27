#!/bin/sh

BASE_DIR=/opt/kaltura/
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
	. $ANSFILE
	export ANSFILE
fi

echo "Running base config...

"
$BASE_DIR/bin/kaltura-base-config.sh "$ANSFILE" 
if [ $? -ne 0 ];then
	echo "$BASE_DIR/bin/kaltura-base-config.sh failed:( You can re-run it when the issue is fixed"
	exit 1
fi

RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo "Could not find $RC_FILE so, exiting.."
	exit 2
fi
. $RC_FILE
echo "Running Sphinx config...

"
bash -e $BASE_DIR/bin/kaltura-sphinx-config.sh "$ANSFILE" 
if [ $? -ne 0 ];then
	echo "$BASE_DIR/bin/kaltura-sphinx-config.sh failed:( You can re-run it when the issue is fixed"
	exit 3 
fi
echo "Running FrontEnd config...

"

$BASE_DIR/bin/kaltura-front-config.sh "$ANSFILE" 
if [ $? -ne 0 ];then
	echo "$BASE_DIR/bin/kaltura-front-config.sh failed:( You can re-run it when the issue is fixed"
	exit 2 
fi
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
rm -rf $APP_DIR/cache/*
rm -f $APP_DIR/log/kaltura-*.log


echo "Setup is done. To login please access:
$SERVICE_URL

"
