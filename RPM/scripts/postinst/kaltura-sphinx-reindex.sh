#!/bin/bash - 
#===============================================================================
#          FILE: sphinx_update.sh
#         USAGE: ./sphinx_update.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 11/10/14 12:37:31 EST
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
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 1 
fi
. $RC_FILE
. /etc/kaltura.d/system.ini
        if /etc/init.d/kaltura-sphinx status;then
                # disable Sphinx's monit monitoring
                rm $APP_DIR/configurations/monit/monit.d/enabled.sphinx.rc
                /etc/init.d/kaltura-sphinx stop
                service kaltura-monit restart 2>/dev/null || service monit restart 2>/dev/null
        fi
        STMP=`date +%s`
        mkdir -p $BASE_DIR/sphinx.bck.$STMP
        echo "Backing up files to $BASE_DIR/sphinx.bck.$STMP. Once the upgrade is done and tested, please remove this directory to save space"
        mv $BASE_DIR/sphinx/kaltura_*  $LOG_DIR/sphinx/data/binlog.* $BASE_DIR/sphinx.bck.$STMP
        /etc/init.d/kaltura-sphinx start
        ln -sf $APP_DIR/configurations/monit/monit.avail/sphinx.rc $APP_DIR/configurations/monit/monit.d/enabled.sphinx.rc
        service kaltura-monit restart 2>/dev/null || service monit restart 2>/dev/null
        for SCRIPT in $APP_DIR/deployment/base/scripts/populateSphinx*.php;do php $SCRIPT
        RC=$?
        if [ $RC -ne 0 ];then

                echo "Failed to run $APP_DIR/deployment/base/scripts/populateSphinxEntries.php.
        Please try to run it manually and look at the logs"
                exit $RC
        fi
	done
/etc/init.d/kaltura-sphinx start
