#!/bin/bash -e 
#===============================================================================
#          FILE: kaltura-live-config.sh
#         USAGE: ./kaltura-live-config.sh 
#   DESCRIPTION: configure server as a batch node.
#       OPTIONS: ---
#       LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 29/11/16 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
verify_user_input()
{
        ANSFILE=$1
        . $ANSFILE
        RC=0
        for VAL in WOWZA_LIC_KEY WOWZA_SILENT_KEY WOWZA_PASSWD  ; do
                if [ -z "${!VAL}" ];then
                        VALS="$VALS\n$VAL"
                        RC=1
                fi
        done
        if [ $RC -eq 1 ];then
                OUT="ERROR: Missing the following params in $ANSFILE
                $VALS
                "
                echo -en "${BRIGHT_RED}$OUT${NORMAL}\n"
                send_install_becon "`basename $0`" "install_fail"  "$OUT"
                exit $RC 
        fi
}
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
        OUT="ERROR: Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
        echo -e $OUT
        exit 3
fi
. $KALTURA_FUNCTIONS_RC
if ! rpm -q kaltura-live;then
        echo -e "${BRIGHT_BLUE}Skipping as kaltura-live is not installed.${NORMAL}"
        exit 0 
fi
CONFIG_DIR=/opt/kaltura/app/configurations
if [ -r $CONFIG_DIR/system.ini ];then
 . $CONFIG_DIR/system.ini
else
 echo -e "${BRIGHT_RED}ERROR: Missing $CONFIG_DIR/system.ini. Exiting..${NORMAL}"
 exit 1
fi

WOWZA_VER=4.7.3
WOWZA_VER_DASHES=`echo $WOWZA_VER|sed 's/\./-/g'`

echo -e "${CYAN}Welcome to Kaltura Live post install setup.${NORMAL}"
trap 'my_trap_handler "${LINENO}" $?' ERR
send_install_becon "`basename $0" "install_start" 0 
RELEASE=`lsb_release -r -s|awk -F . '{print $1}'`
if [ $RELEASE = 6 ];then
        yum install -y ant-trax
fi

if [ -r $CONSENT_FILE ];then
        . $CONSENT_FILE
fi
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        . $ANSFILE
else
        echo -e "${CYAN}Wowza license key:${NORMAL} "
        read -e WOWZA_LIC_KEY
        echo -e "${CYAN}Wowza silent key:${NORMAL} "
        read -e WOWZA_SILENT_KEY
        echo -e "${CYAN}Wowza admin password [only letters, numbers and '@', '.', '_' and '-' are acceptible]:${NORMAL} "
        read -s WOWZA_PASSWD
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


echo -e "${BRIGHT_BLUE}Fetching the Wowza archive...${NORMAL}"
wget --quiet https://www.wowza.com/downloads/WowzaStreamingEngine-$WOWZA_VER_DASHES/WowzaStreamingEngine-$WOWZA_VER-linux-x64-installer.run -O /tmp/WowzaStreamingEngine-$WOWZA_VER-linux-x64-installer.run
chmod +x /tmp/WowzaStreamingEngine-$WOWZA_VER-linux-x64-installer.run
echo -e "${BRIGHT_BLUE}Deploying Wowza, this may take a while...${NORMAL}"
if [ -n "$WOWZA_SILENT_KEY" ];then
       # this is incredibly moronic --prefix is a mandatory arg but no matter what you'll pass the prefix is always /usr/local
 /tmp/WowzaStreamingEngine-$WOWZA_VER-linux-x64-installer.run  --mode unattended --licensekey $WOWZA_LIC_KEY --silentInstallKey $WOWZA_SILENT_KEY --username kadmin --password $WOWZA_PASSWD --prefix /usr/local/
else
       # install interactively
 /tmp/WowzaStreamingEngine-$WOWZA_VER-linux-x64-installer.run  
fi

BASE_DIR=/opt/kaltura
WOWZA_PREFIX=/usr/local/WowzaStreamingEngine
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/wowza.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.wowza.rc

MINUS_FIVE_ADMIN_SECRET=`echo "select admin_secret from partner where id=-5"|mysql -N -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME -P$DB1_PORT`

CONF_FILE_TEMPLATES=`find /usr/local/WowzaStreamingEngine/conf -type f -name "*template*"`
for CONF_FILE_TEMPLATE in $CONF_FILE_TEMPLATES;do
    CONF_FILE=`echo $CONF_FILE_TEMPLATE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
    sed -e "s#@KALTURA_SERVICE_URL@#$SERVICE_URL#g" -e "s#@KALTURA_PARTNER_ID@#-5#g" -e "s#@KALTURA_PARTNER_ADMIN_SECRET@#$MINUS_FIVE_ADMIN_SECRET#g" $CONF_FILE_TEMPLATE > $CONF_FILE
done


# remove default unneeded Wowza apps:
rm -rf $WOWZA_PREFIX/conf/live/
rm -rf $WOWZA_PREFIX/conf/vod/
rm -rf $WOWZA_PREFIX/applications/live/
rm -rf $WOWZA_PREFIX/applications/vod/

sed 's@${com.wowza.wms.TuningHeapSizeDevelopment}@${com.wowza.wms.TuningHeapSizeProduction}@g' -i $WOWZA_PREFIX/conf/Tune.xml
#ant -Dbasedir=$WOWZA_PREFIX -f $WOWZA_PREFIX/build.xml
php $BASE_DIR/bin/register_media_server.php `hostname -f`
service WowzaStreamingEngine restart
service kaltura-monit stop >> /dev/null 2>&1
service kaltura-monit start

send_install_becon `basename $0` install_success 0
