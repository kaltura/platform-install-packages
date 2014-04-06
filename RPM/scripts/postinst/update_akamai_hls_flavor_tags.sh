#!/bin/sh
# here is our problem:
#   the ip{hone,ad}new tags are only good for Akamai HLS, on any other serve method, it makes ip{hone,ad} serves not to work.
#   If a user DOES wish to use Akamai HLS, we have the kaltura-remote-storage-config.sh for them to run and that script calls this one.

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	echo $OUT
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 1 
fi
. $RC_FILE
for i in `echo "select id from flavor_params where tags not like '%ipadnew%' and tags not like '%iphonenew%' and tags like '%ipad' or tags like '%iphone';"| mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME -N` ;do
	TAGS=`echo "select tags from flavor_params where id=$i" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME -N`
	if echo $TAGS|grep -q ipad;then
		echo "update flavor_params set tags='$TAGS,ipadnew' where id=$i" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME -N
	elif echo $TAGS|grep -q iphone;then
		echo "update flavor_params set tags='$TAGS,iphonenew' where id=$i" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME -N
	fi
done
