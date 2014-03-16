#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-sphinx-config.sh
#         USAGE: ./kaltura-sphinx-config.sh 
#   DESCRIPTION: configure server as a Sphinx node.
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:25:30 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	echo $OUT
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
if ! rpm -q kaltura-sphinx;then
	echo -e "${BRIGHT_RED}ERROR: first install kaltura-sphinx.${NORMAL}"
	exit 11
fi
if [ -n "$1" -a -r "$1" ];then
	ANSFILE=$1
	. $ANSFILE
fi
if [ ! -r /opt/kaltura/app/base-config.lock ];then
	`dirname $0`/kaltura-base-config.sh "$ANSFILE"
else
	echo -e "${BRIGHT_BLUE}base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
${NORMAL}
"
fi
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2
fi
. $RC_FILE
trap 'my_trap_handler ${LINENO} ${$?}' ERR
send_install_becon `basename $0` $ZONE install_start 
mkdir -p $LOG_DIR/sphinx/data $APP_DIR/cache//sphinx
chown $OS_KALTURA_USER.$OS_KALTURA_USER $APP_DIR/cache/sphinx $LOG_DIR/sphinx/data
echo "sphinxServer = $SPHINX_HOST" > /opt/kaltura/app/configurations/sphinx/populate/`hostname`.ini
/etc/init.d/kaltura-sphinx restart >/dev/null 2>&1
/etc/init.d/kaltura-populate restart >/dev/null 2>&1
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/sphinx.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.sphinx.rc
/etc/init.d/kaltura-monit stop >> /dev/null 2>&1
/etc/init.d/kaltura-monit start
send_install_becon `basename $0` $ZONE install_success
