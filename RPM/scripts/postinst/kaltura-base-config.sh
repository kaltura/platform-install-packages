#!/bin/bash  
#===============================================================================
#          FILE: kaltura-base-config.sh
#         USAGE: ./kaltura-base-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy, <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/06/14 11:27:00 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
verify_user_input()
{
        ANSFILE=$1
        . $ANSFILE
        RC=0
        for VAL in TIME_ZONE KALTURA_FULL_VIRTUAL_HOST_NAME KALTURA_VIRTUAL_HOST_NAME DB1_HOST DB1_PORT DB1_NAME DB1_USER SERVICE_URL SPHINX_SERVER1 SPHINX_SERVER2 DWH_HOST DWH_PORT SPHINX_DB_HOST SPHINX_DB_PORT ADMIN_CONSOLE_ADMIN_MAIL ADMIN_CONSOLE_PASSWORD SUPER_USER SUPER_USER_PASSWD CDN_HOST KALTURA_VIRTUAL_HOST_PORT DB1_PASS DWH_PASS PROTOCOL RED5_HOST USER_CONSENT VOD_PACKAGER_HOST VOD_PACKAGER_PORT IP_RANGE IS_SSL; do
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
                send_install_becon kaltura-base $ZONE "install_fail"  "$OUT"
                exit $RC 
        fi
}

create_answer_file()
{
        POST_INST_MAIL_TMPL=$1
        ANSFILE=/tmp/kaltura_`date +%d_%m_%H_%M`.ans
        for VAL in TIME_ZONE KALTURA_FULL_VIRTUAL_HOST_NAME KALTURA_VIRTUAL_HOST_NAME DB1_HOST DB1_PORT DB1_PASS DB1_NAME DB1_USER SERVICE_URL SPHINX_SERVER1 SPHINX_SERVER2 DWH_HOST DWH_PORT SPHINX_DB_HOST SPHINX_DB_PORT ADMIN_CONSOLE_ADMIN_MAIL ADMIN_CONSOLE_PASSWORD CDN_HOST KALTURA_VIRTUAL_HOST_PORT SUPER_USER SUPER_USER_PASSWD ENVIRONMENT_NAME DWH_PASS PROTOCOL RED5_HOST USER_CONSENT SEND_NEWSLETTER CONTACT_MAIL VOD_PACKAGER_HOST VOD_PACKAGER_PORT IP_RANGE WWW_HOST; do
                if [ -n "${!VAL}" ];then
                        echo "$VAL=\"${!VAL}\"" >> $ANSFILE 
                fi
        done
        if [ -r "$POST_INST_MAIL_TMPL" ];then
                        sed -i "s#@ANSFILE@#$ANSFILE#g" $POST_INST_MAIL_TMPL 
        fi
	chmod 600 $ANSFILE
        echo -en "${CYAN}
========================================================================================================================
Kaltura install answer file written to $ANSFILE  -  Please save it!
This answers file can be used to silently-install re-install this machine or deploy other hosts in your cluster.
========================================================================================================================
${NORMAL}
"

}

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
        OUT="${BRIGHT_RED}ERROR:could not find $KALTURA_FUNCTIONS_RC so, exiting..${NORMAL}"
        echo -en $OUT
        exit 3
fi
. $KALTURA_FUNCTIONS_RC
if ! rpm -q kaltura-base;then
        echo -e "${BRIGHT_RED}Exiting as kaltura-base is not installed.
This MAY be because the installation of it was skipped do to SELinux being in 'Enforcing' mode.
Please review: https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#disable-selinux---required-currently-kaltura-cant-run-properly-with-selinux
And re-run:
# yum install kaltura-server

${NORMAL}"
        exit 0 
fi
trap 'my_trap_handler "${LINENO}" ${$?}' ERR
send_install_becon `basename $0` $ZONE install_start 0
BASE_DIR=/opt/kaltura
LOCALHOST=127.0.0.1
DISPLAY_NAME=`rpm -q kaltura-base --queryformat %{version}`
KALT_CONF_DIR=$BASE_DIR/app/configurations/
BEGINNERS_TUTORIAL_URL=http://bit.ly/KalturaUploadMenu
QUICK_START_GUIDE_URL=http://bit.ly/KalturaKmcManual
FORUMS_URLS=http://bit.ly/KalturaForums
echo -e "${CYAN}Welcome to Kaltura Server $DISPLAY_NAME post install setup.${NORMAL}"

if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
        . $ANSFILE
        export ANSFILE
else
        if [ -r $CONSENT_FILE ];then
                . $CONSENT_FILE
        elif [ -z "$USER_CONSENT" ];then
                get_tracking_consent
        fi
        . $CONSENT_FILE
	# get_newsletter_consent
       # echo "Welcome to Kaltura Server $DISPLAY_NAME post install setup.
echo -e "\n${CYAN}In order to finalize the system configuration, please input the following:


CDN hostname [${YELLOW}`hostname`${CYAN}]:${NORMAL}"
	echo -e "\n${CYAN}The host will be accessed over http(s). In case your CDN operates on a non-default port, please input CDNHOST:PORT.  ${NORMAL}"
        read -e CDN_HOST
        if [ -z "$CDN_HOST" ];then
                CDN_HOST=`hostname`

        fi

        echo -e "${CYAN}Apache virtual hostname [${YELLOW}`hostname`${CYAN}]
(Must be accessible from both inside the machine and from any clients / browsers that will use Kaltura):
${NORMAL} "
        read -e KALTURA_VIRTUAL_HOST_NAME
        if [ -z "$KALTURA_VIRTUAL_HOST_NAME" ];then
                KALTURA_VIRTUAL_HOST_NAME=`hostname`
                #echo $KALTURA_VIRTUAL_HOST_NAME
        fi
	WWW_HOST=$KALTURA_VIRTUAL_HOST_NAME
        echo -en "${CYAN}Vhost port to listen on [${YELLOW}80${CYAN}]:${NORMAL} "
        read -e KALTURA_VIRTUAL_HOST_PORT
        if [ -z "$KALTURA_VIRTUAL_HOST_PORT" ];then
                KALTURA_VIRTUAL_HOST_PORT=80
        fi

	if [ "$KALTURA_VIRTUAL_HOST_PORT" -eq 80 -o "$KALTURA_VIRTUAL_HOST_PORT" -eq 443 ];then
		KALTURA_FULL_VIRTUAL_HOST_NAME=$KALTURA_VIRTUAL_HOST_NAME
	else
		KALTURA_FULL_VIRTUAL_HOST_NAME="$KALTURA_VIRTUAL_HOST_NAME:$KALTURA_VIRTUAL_HOST_PORT"
	fi


        if [ -z "$DB1_HOST" ];then
                echo -en "${CYAN}DB hostname [${YELLOW}$LOCALHOST${CYAN}]:${NORMAL} "
                read -e DB1_HOST
                if [ -z "$DB1_HOST" ];then
                        DB1_HOST=$LOCALHOST
                fi
        fi


        echo -en "${CYAN}range of ip addresses belonging to internal kaltura servers [${YELLOW}0.0.0.0-255.255.255.255${CYAN}]:${NORMAL} 
The range is used when checking service actions permissions and allowing to access certain services without KS from the internal servers.
The default is only good for testing, on a production ENV you should adjust according to your network.
"
	read IP_RANGE
	if [ -z "$IP_RANGE" ];then
		IP_RANGE="0.0.0.0-255.255.255.255"
	fi


        echo -en "${CYAN}DB port [${YELLOW}3306${CYAN}]:${NORMAL} "
        read -e DB1_PORT
        if [ -z "$DB1_PORT" ];then
                DB1_PORT=3306
        fi

	echo -en "${CYAN}MySQL super user [only for install, default root]:${NORMAL} "
	read -e SUPER_USER
	if [ -z "$SUPER_USER" ];then
		SUPER_USER=root
	fi
        while [ -z "$SUPER_USER_PASSWD" ];do
                echo -en "${CYAN}MySQL super user passwd [only for install]:${NORMAL}\n "
                read -s SUPER_USER_PASSWD
        done

        echo -en "${CYAN}Analytics DB hostname [${YELLOW}$DB1_HOST${CYAN}]:${NORMAL}"
        read -e DWH_HOST
        if [ -z "$DWH_HOST" ];then
                DWH_HOST=$DB1_HOST
        fi

        echo -en "${CYAN}Analytics DB port [${YELLOW}$DB1_PORT${CYAN}]:${NORMAL}"
        read -e DWH_PORT
        if [ -z "$DWH_PORT" ];then
                DWH_PORT=$DB1_PORT
        fi

        if [ -z "$SPHINX_SERVER1" ];then
                echo -en "${CYAN}Sphinx hostname [${YELLOW}$LOCALHOST${CYAN}]:${NORMAL} "
                read -e SPHINX_SERVER1
                if [ -z $SPHINX_SERVER1 ];then
                        SPHINX_SERVER1="$LOCALHOST"
                fi
        fi

        if [ -z "$RED5_HOST" ];then
                echo -en "${CYAN}Media Streaming Server host [${YELLOW}`hostname`${CYAN}]:${NORMAL} "
                read -e RED5_HOST
                if [ -z $RED5_HOST ];then
                        RED5_HOST=`hostname`
                fi
        fi
        echo -en "${CYAN}Secondary Sphinx hostname [leave empty if none]: ${NORMAL} "
        read -e SPHINX_SERVER2
        if [ -z $SPHINX_SERVER2 ];then
                SPHINX_SERVER2=" "
        fi

        while [ -z "$SERVICE_URL" ];do
                if [ "$KALTURA_VIRTUAL_HOST_PORT" -eq 443 ];then
                        PROTOCOL="https"
                else
                        PROTOCOL="http"
                fi
                echo -e "${CYAN}Your Kaltura Service URL [${YELLOW}$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME${CYAN}]
(Base URL where the Kaltura API and Apps will be accessed from - this would be your Load Balancer URL on a cluster or same as your virtual host in an all-in-one Kaltura server - Must be accessible from both inside the machine and from any clients / browsers that will use Kaltura):
${NORMAL} "
                read -e SERVICE_URL
                if [ -z "$SERVICE_URL" ];then
                        SERVICE_URL=$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME
                fi
        done
        echo -en "${CYAN}VOD packager hostname [${YELLOW}`hostname`${CYAN}]:${NORMAL} "
        read -e VOD_PACKAGER_HOST
        if [ -z "$VOD_PACKAGER_HOST" ];then
                VOD_PACKAGER_HOST=`hostname`
        fi

        echo -en "${CYAN}VOD packager port to listen on [${YELLOW}88${CYAN}]:${NORMAL} "
        read -e VOD_PACKAGER_PORT
        if [ -z "$VOD_PACKAGER_PORT" ];then
                VOD_PACKAGER_PORT=88
        fi
        while [ -z "$ADMIN_CONSOLE_ADMIN_MAIL" ];do
                echo -en "${CYAN}Kaltura Admin user (email address):${NORMAL} "
                read -e ADMIN_CONSOLE_ADMIN_MAIL
        done
        while [ -z "$ADMIN_CONSOLE_PASSWORD" ];do
                echo -en "${CYAN}Admin user login password (must be minimum 8 chars and include at least one of each: upper-case, lower-case, number and a special character):${NORMAL}"
                read -s ADMIN_CONSOLE_PASSWORD
                if echo $ADMIN_CONSOLE_PASSWORD | grep -q "/" ;then
                        echo -en "${BRIGHT_RED}ERROR: Passwd can't have the '/' char in it. Please re-input.${NORMAL}"
                        unset ADMIN_CONSOLE_PASSWORD
                fi
        done

        while [ -z "$ANSFILE" -a -z "$AGAIN_ADMIN_CONSOLE_PASSWORD" ];do
                echo -en "\n${CYAN}Confirm passwd:${NORMAL} \n"
                read -s AGAIN_ADMIN_CONSOLE_PASSWORD
                if [ "$ADMIN_CONSOLE_PASSWORD" != "$AGAIN_ADMIN_CONSOLE_PASSWORD" ];then
                        echo -en "${BRIGHT_RED}ERROR: Passwds do not match, again please.${NORMAL}" 
                        unset AGAIN_ADMIN_CONSOLE_PASSWORD
                        echo -en "${BRIGHT_RED}ERROR: Admin user login password (must be minimum 8 chars and include at least one of each: upper-case, lower-case, number and a special character): ${NORMAL}"
                        read -s ADMIN_CONSOLE_PASSWORD
                fi
        done
        if [ -r /etc/sysconfig/clock ];then
                . /etc/sysconfig/clock
        fi
        while [ -z "$TIME_ZONE" ];do
                if [ -n "$ZONE" ];then
                        echo -en "${CYAN}Your time zone [see http://php.net/date.timezone], or press enter for [${YELLOW}$ZONE${CYAN}]: ${NORMAL}"
                else
                        echo -en "${CYAN}Your time zone [see http://php.net/date.timezone]: ${NORMAL}"
                fi
                read -e TIME_ZONE
                if [ -z "$TIME_ZONE" -a -n "$ZONE" ];then
                        TIME_ZONE="$ZONE"
                fi
		trap - ERR
		php -r "if (timezone_open('$TIME_ZONE') === false){exit(1);}" 2>/dev/null
		RC=$?
		trap 'my_trap_handler "${LINENO}" ${$?}' ERR
		if [ $RC -ne 0 ];then
			echo -e "${BRIGHT_RED}Bad Timezone value, please check valid options at http://php.net/date.timezone${NORMAL}"
			unset TIME_ZONE
		fi
        done


        if [ -z "$ENVIRONMENT_NAME" ];then
                echo -en "${CYAN}Your Kaltura install name (this name will show as the From field in emails sent by the system) [${YELLOW}Kaltura Video Platform${CYAN}]:${NORMAL}"
                read ENVIRONMENT_NAME
                if [ -z "$ENVIRONMENT_NAME" ];then
                        ENVIRONMENT_NAME="Kaltura Video Platform"
                fi
        fi

        if [ -z "$CONTACT_URL" ];then
                echo -en "${CYAN}Your website Contact Us URL [${YELLOW}http://corp.kaltura.com/company/contact-us${CYAN}]:${NORMAL} "
                read CONTACT_URL
                if [ -z "$CONTACT_URL" ];then
                        CONTACT_URL="http://corp.kaltura.com/company/contact-us"
                fi
        fi
        if [ -z "$CONTACT_PHONE_NUMBER" ];then
                echo -en "${CYAN}Your 'Contact us' phone number [${YELLOW}+1 800 871 5224${CYAN}]:${NORMAL}"
                read CONTACT_PHONE_NUMBER
                if [ -z "$CONTACT_PHONE_NUMBER" ];then
                        CONTACT_PHONE_NUMBER="+1 800 871 5224"
                fi
        fi







fi

# need to check if we even have PHP as Sphinx and DWH can be installed without thank heavens.
# reported by David Bezemer:
 for INI in /etc/php.ini /etc/php.d/*kaltura*ini;do
        if [ -r "$INI" ];then
                sed -i "s#\(date.timezone\)\s*=.*#\1='$TIME_ZONE'#g" $INI
        fi
done
if [ -z "$DB1_PASS" ];then
        DB1_PASS=`< /dev/urandom tr -dc A-Za-z0-9 | head -c15`
        echo "update mysql.user set password=PASSWORD('$DB1_PASS') WHERE user='kaltura';flush PRIVILEGES" | mysql -h$DB1_HOST -P$DB1_PORT -u$SUPER_USER -p$SUPER_USER_PASSWD mysql
	if [ -z "$DWH_PASS" ];then
		DWH_PASS=$DB1_PASS
	fi
fi
DB1_NAME=kaltura
DB1_USER=kaltura

# no added value in putting this on a separate server..
SPHINX_DB_HOST=$DB1_HOST
SPHINX_DB_PORT=$DB1_PORT

CONF_FILES=`find $KALT_CONF_DIR  -type f -name "*template*"`
CONF_FILES="$CONF_FILES $BASE_DIR/app/batch/batches/Mailer/emails_en.template.ini $BASE_DIR/app/tests/monitoring/config.template.ini $BASE_DIR/bin/sanity_config.template.ini"
if rpm -q kaltura-html5-studio > /dev/null;then
        CONF_FILES="$CONF_FILES $BASE_DIR/apps/studio/`rpm -qa kaltura-html5-studio --queryformat %{version}`/studio.template.ini"
fi 
CONF_FILES="$CONF_FILES `find $BASE_DIR/app/plugins/monitor/nagios/config -type f -name "*template*"`"
 
if [ -d "$BASE_DIR/dwh" ];then
        CONF_FILES="$CONF_FILES `find $BASE_DIR/dwh  -type f -name "*template*"`"
fi

HTML5_VER="`rpm -qa kaltura-html5lib --queryformat %{version}`"
create_answer_file $POST_INST_MAIL_TMPL
APP_REMOTE_ADDR_HEADER_SALT=`echo $SERVICE_URL|base64 -w0`

if [ "$IS_SSL" == 'Y' ];then
        PROTOCOL="https"
else
        PROTOCOL="http"
fi
SERVICE_URL="$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME"
echo "service URL is: $SERVICE_URL"

# Now we will sed.

for TMPL_CONF_FILE in $CONF_FILES;do
        CONF_FILE=`echo $TMPL_CONF_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
        if [ -r $CONF_FILE ];then
                cp $CONF_FILE $CONF_FILE.backup
        fi
        if `echo $TMPL_CONF_FILE|grep -q template`;then
                cp  $TMPL_CONF_FILE $CONF_FILE
        fi
	sed  -e "s#@ENVIRONMENT_PROTOCOL@#$PROTOCOL#g" -e "s#@CDN_HOST@#$CDN_HOST#g" -e "s#@DB[1-9]_HOST@#$DB1_HOST#g" -e "s#@DB[1-9]_NAME@#$DB1_NAME#g" -e "s#@DB[1-9]_USER@#$DB1_USER#g" -e "s#@DB[1-9]_PASS@#$DB1_PASS#g" -e "s#@DB[1-9]_PORT@#$DB1_PORT#g" -e "s#@TIME_ZONE@#$TIME_ZONE#g" -e "s#@KALTURA_FULL_VIRTUAL_HOST_NAME@#$KALTURA_FULL_VIRTUAL_HOST_NAME#g" -e "s#@KALTURA_VIRTUAL_HOST_NAME@#$KALTURA_VIRTUAL_HOST_NAME#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@WWW_HOST@#$KALTURA_FULL_VIRTUAL_HOST_NAME#g" -e "s#@SPHINX_DB_NAME@#kaltura_sphinx_log#g" -e "s#@SPHINX_DB_HOST@#$SPHINX_DB_HOST#g" -e "s#@SPHINX_DB_PORT@#$DB1_PORT#g" -e "s#@DWH_HOST@#$DWH_HOST#g" -e "s#@DWH_PORT@#$DWH_PORT#g" -e "s#@SPHINX_SERVER1@#$SPHINX_SERVER1#g" -e "s#@SPHINX_SERVER2@#$SPHINX_SERVER2#g" -e "s#@DWH_DATABASE_NAME@#kalturadw#g" -e "s#@DWH_USER@#etl#g" -e "s#@DWH_PASS@#$DWH_PASS#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@WEB_DIR@#$BASE_DIR/web#g" -e "s#@LOG_DIR@#$BASE_DIR/log#g" -e "s#$BASE_DIR/app#$BASE_DIR/app#g" -e "s#@PHP_BIN@#/usr/bin/php#g" -e "s#@OS_KALTURA_USER@#kaltura#g" -e "s#@BASE_DIR@#$BASE_DIR#" -e "s#@APP_DIR@#$BASE_DIR/app#g" -e "s#@DWH_DIR@#$BASE_DIR/dwh#g" -e "s#@KETTLE_SH@#/opt/kaltura/pentaho/pdi/kitchen.sh#g" -e "s#@EVENTS_LOGS_DIR@#$BASE_DIR/web/logs#g" -e "s#@TMP_DIR@#$BASE_DIR/tmp#g" -e "s#@APACHE_SERVICE@#httpd#g" -e "s#@KALTURA_VIRTUAL_HOST_PORT@#$KALTURA_VIRTUAL_HOST_PORT#g" -e "s#@BIN_DIR@#$BASE_DIR/bin#g" -e "s#@KALTURA_VERSION@#$DISPLAY_NAME#g" -e "s#@SPHINX_SERVER@#$SPHINX_SERVER#g" -e "s#@IMAGE_MAGICK_BIN_DIR@#/usr/bin#g" -e "s#@CURL_BIN_DIR@#/usr/bin#g" -e "s@^\(bin_path_mediainfo\).*@\1=/usr/bin/mediainfo@g" -e "s#@CONTACT_URL@#$CONTACT_URL#g" -e "s#@ENVIRONMENT_NAME@#$ENVIRONMENT_NAME#g" -e "s#@BEGINNERS_TUTORIAL_URL@#$BEGINNERS_TUTORIAL_URL#g" -e "s#@BEGINNERS_TUTORIAL_URL@#$BEGINNERS_TUTORIAL_URL#g" -e "s#@QUICK_START_GUIDE_URL@#$QUICK_START_GUIDE_URL#g" -e "s#@FORUMS_URLS@#$FORUMS_URLS#g" -e "s#@CONTACT_PHONE_NUMBER@#$CONTACT_PHONE_NUMBER#g" -e "s#@UNSUBSCRIBE_EMAIL_URL@#$SERVICE_URL/index.php/extwidget/blockMail?e=#g" -e "s#@UICONF_TAB_ACCESS@#SYSTEM_ADMIN_BATCH_CONTROL#g"  -e "s#@EVENTS_FETCH_METHOD@#local#g" -e "s#@HTML5_VER@#$HTML5_VER#g" -e "s#@MONIT_PASSWD@#$DB1_PASS#g" -e "s#@VOD_PACKAGER_HOST@#$VOD_PACKAGER_HOST#g" -e "s#@VOD_PACKAGER_PORT@#$VOD_PACKAGER_PORT#g" -e "s#@IP_RANGE@#$IP_RANGE#g" -e "s#@DB2_PORT@#$DWH_PORT#g" -e "s#@DB2_HOST@#$DWH_HOST#g" -e "s#@APP_REMOTE_ADDR_HEADER_SALT@#$APP_REMOTE_ADDR_HEADER_SALT#g" -i $CONF_FILE
done

sed -i "s#@MONIT_PASSWD@#$DB1_PASS#" -i $BASE_DIR/app/admin_console/views/scripts/index/monit.phtml
echo "
SERVICE_URL=$SERVICE_URL
SPHINX_HOST=$SPHINX_SERVER1
DB1_PORT=$DB1_PORT
SUPER_USER=$SUPER_USER
SUPER_USER_PASSWD=\"$SUPER_USER_PASSWD\"
KALTURA_VIRTUAL_HOST_NAME=$KALTURA_VIRTUAL_HOST_NAME
RED5_HOST=$RED5_HOST">> $BASE_DIR/app/configurations/system.ini
# these two have passwds in them.
chown kaltura.apache $BASE_DIR/app/configurations/system.ini $BASE_DIR/app/configurations/db.ini
chmod 640 $BASE_DIR/app/configurations/system.ini $BASE_DIR/app/configurations/db.ini
chown root.root $BASE_DIR/app/configurations/monit/monit.conf
chmod 600 $BASE_DIR/app/configurations/monit/monit.conf


# gen secrets
ADMIN_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@#$%^*()_+-=" | head -c20`
HASHED_ADMIN_SECRET=`echo $ADMIN_SECRET|md5sum`
ADMIN_SECRET=`echo $HASHED_ADMIN_SECRET|awk -F " " '{print $1}'`

ADMIN_CONSOLE_PARTNER_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@#$%^*()_+-=" | head -c20`
HASHED_ADMIN_CONSOLE_PARTNER_SECRET=`echo $ADMIN_CONSOLE_PARTNER_SECRET|md5sum`
ADMIN_CONSOLE_PARTNER_SECRET=`echo $HASHED_ADMIN_CONSOLE_PARTNER_SECRET|awk -F " " '{print $1}'`

MONITOR_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_MONITOR_PARTNER_ADMIN_SECRET=`echo $HASHED_MONITOR_PARTNER_ADMIN_SECRET | md5sum`
MONITOR_PARTNER_ADMIN_SECRET=`echo $HASHED_MONITOR_PARTNER_ADMIN_SECRET | awk -F " " '{print $1}'` 

MONITOR_PARTNER_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_MONITOR_PARTNER_SECRET=`echo $HASHED_MONITOR_PARTNER_SECRET | md5sum`
MONITOR_PARTNER_SECRET=`echo $HASHED_MONITOR_PARTNER_SECRET | awk -F " " '{print $1}'` 

PARTNER_ZERO_ADMIN_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_PARTNER_ZERO_ADMIN_SECRET=`echo $PARTNER_ZERO_ADMIN_SECRET|md5sum`
PARTNER_ZERO_ADMIN_SECRET=`echo $HASHED_PARTNER_ZERO_ADMIN_SECRET|awk -F " " '{print $1}'`

PARTNER_ZERO_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_PARTNER_ZERO_SECRET=`echo $PARTNER_ZERO_SECRET|md5sum`
PARTNER_ZERO_SECRET=`echo $HASHED_PARTNER_ZERO_SECRET|awk -F " " '{print $1}'`


BATCH_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_BATCH_PARTNER_ADMIN_SECRET=`echo $BATCH_PARTNER_ADMIN_SECRET|md5sum`
BATCH_PARTNER_ADMIN_SECRET=`echo $HASHED_BATCH_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`

BATCH_PARTNER_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_BATCH_PARTNER_SECRET=`echo $BATCH_PARTNER_SECRET|md5sum`
BATCH_PARTNER_SECRET=`echo $HASHED_BATCH_PARTNER_SECRET|awk -F " " '{print $1}'`

MEDIA_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_MEDIA_PARTNER_ADMIN_SECRET=`echo $MEDIA_PARTNER_ADMIN_SECRET|md5sum`
MEDIA_PARTNER_ADMIN_SECRET=`echo $HASHED_MEDIA_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`

MEDIA_PARTNER_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_MEDIA_PARTNER_SECRET=`echo $MEDIA_PARTNER_SECRET|md5sum`
MEDIA_PARTNER_SECRET=`echo $HASHED_MEDIA_PARTNER_SECRET|awk -F " " '{print $1}'`

TEMPLATE_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_TEMPLATE_PARTNER_ADMIN_SECRET=`echo $TEMPLATE_PARTNER_ADMIN_SECRET|md5sum`
TEMPLATE_PARTNER_ADMIN_SECRET=`echo $HASHED_TEMPLATE_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`
TEMPLATE_PARTNER_ADMIN_PASSWORD="0+`< /dev/urandom tr -dc "A-Za-z0-9_=@%$" | head -c8`=*1"

TEMPLATE_PARTNER_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_TEMPLATE_PARTNER_SECRET=`echo $TEMPLATE_PARTNER_SECRET|md5sum`
TEMPLATE_PARTNER_SECRET=`echo $HASHED_TEMPLATE_PARTNER_SECRET|awk -F " " '{print $1}'`

HOSTED_PAGES_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_HOSTED_PAGES_PARTNER_ADMIN_SECRET=`echo $HOSTED_PAGES_PARTNER_ADMIN_SECRET|md5sum`
HOSTED_PAGES_PARTNER_ADMIN_SECRET=`echo $HASHED_HOSTED_PAGES_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`

HOSTED_PAGES_PARTNER_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_HOSTED_PAGES_PARTNER_SECRET=`echo $HOSTED_PAGES_PARTNER_SECRET|md5sum`
HOSTED_PAGES_PARTNER_SECRET=`echo $HASHED_HOSTED_PAGES_PARTNER_SECRET|awk -F " " '{print $1}'`

PLAY_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_PLAY_PARTNER_ADMIN_SECRET=`echo $PLAY_PARTNER_ADMIN_SECRET|md5sum`
PLAY_PARTNER_ADMIN_SECRET=`echo $HASHED_PLAY_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`

PLAY_PARTNER_SECRET=`< /dev/urandom tr -dc "A-Za-z0-9_~@$%^*()_+-=" | head -c20`
HASHED_PLAY_PARTNER_SECRET=`echo $PLAY_PARTNER_SECRET|md5sum`
PLAY_PARTNER_SECRET=`echo $HASHED_PLAY_PARTNER_SECRET=|awk -F " " '{print $1}'`

# Dropping the port when it's a standard one
if [ "$KALTURA_VIRTUAL_HOST_PORT" -eq 443 -o "$KALTURA_VIRTUAL_HOST_PORT" -eq 80 ];then
        KALTURA_FULL_VIRTUAL_HOST_NAME="$KALTURA_VIRTUAL_HOST_NAME"
else
        KALTURA_FULL_VIRTUAL_HOST_NAME="$KALTURA_VIRTUAL_HOST_NAME:$KALTURA_VIRTUAL_HOST_PORT"
fi

SERVICE_URL=$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME

# SQL statement files tokens:
for TMPL in `find $BASE_DIR/app/deployment/base/scripts/init_content/ -name "*template*"`;do
        DEST_FILE=`echo $TMPL | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
        cp  $TMPL $DEST_FILE
        sed -e "s#@WEB_DIR@#$BASE_DIR/web#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@MONITOR_PARTNER_ADMIN_SECRET@#$MONITOR_PARTNER_ADMIN_SECRET#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@MONITOR_PARTNER_SECRET@#$MONITOR_PARTNER_SECRET#g" -e "s#@PARTNER_ZERO_ADMIN_SECRET@#$PARTNER_ZERO_ADMIN_SECRET#g" -e "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#g" -e "s#@MEDIA_PARTNER_ADMIN_SECRET@#$MEDIA_PARTNER_ADMIN_SECRET#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$TEMPLATE_PARTNER_ADMIN_SECRET#g" -e "s#@HOSTED_PAGES_PARTNER_ADMIN_SECRET@#$HOSTED_PAGES_PARTNER_ADMIN_SECRET#g" -e "s#@STORAGE_BASE_DIR@#$BASE_DIR/web#g" -e "s#@DELIVERY_HTTP_BASE_URL@#https://dontknow.com#g" -e "s#@DELIVERY_RTMP_BASE_URL@#rtmp://reallydontknow.com#g" -e "s#@DELIVERY_ISS_BASE_URL@#https://honesttogodihavenoidea.com#g" -e "s/@ADMIN_CONSOLE_PASSWORD@/$ADMIN_CONSOLE_PASSWORD/g"  -e "s#@WWW_HOST@#$KALTURA_FULL_VIRTUAL_HOST_NAME#g" -e "s/@PLAY_PARTNER_ADMIN_SECRET@/$PLAY_PARTNER_ADMIN_SECRET/g"   -e "s#@TEMPLATE_PARTNER_ADMIN_PASSWORD@#$TEMPLATE_PARTNER_ADMIN_PASSWORD#g" -e "s#@PARTNER_ZERO_SECRET@#$PARTNER_ZERO_SECRET#g" -e "s#@BATCH_PARTNER_SECRET@#$BATCH_PARTNER_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_SECRET@#$ADMIN_CONSOLE_PARTNER_SECRET#g" -e "s#@HOSTED_PAGES_PARTNER_SECRET@#$HOSTED_PAGES_PARTNER_SECRER#g" -e "s#@MEDIA_PARTNER_SECRET@#$MEDIA_PARTNER_SECRET#g" -e "s#@PLAY_PARTNER_SECRET@#$PLAY_PARTNER_SECRET#g" -e "s#@TEMPLATE_PARTNER_SECRET@#$TEMPLATE_PARTNER_SECRET#g" -e "s#@IP_RANGE@#$IP_RANGE#g" -i $DEST_FILE
done


CONFS=`find $BASE_DIR/app/deployment/base/scripts/init_data/ -name "*template*"`
CONFS="$CONFS $BASE_DIR/app/tests/monitoring/config.ini"
for TMPL in $CONFS;do
        DEST_FILE=`echo $TMPL | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
        if `echo $TMPL|grep -q template`;then
                cp $TMPL $DEST_FILE
        fi
        sed -e "s#@ENVIRONMENT_PROTOCOL@#$PROTOCOL#g" -e "s#@WEB_DIR@#$BASE_DIR/web#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@MONITOR_PARTNER_ADMIN_SECRET@#$MONITOR_PARTNER_ADMIN_SECRET#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@MONITOR_PARTNER_SECRET@#$MONITOR_PARTNER_SECRET#g" -e "s#@PARTNER_ZERO_ADMIN_SECRET@#$PARTNER_ZERO_ADMIN_SECRET#g" -e "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#g" -e "s#@MEDIA_PARTNER_ADMIN_SECRET@#$MEDIA_PARTNER_ADMIN_SECRET#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$TEMPLATE_PARTNER_ADMIN_SECRET#g" -e "s#@KALTURA_VERSION@#$DISPLAY_NAME#g" -e "s#@HOSTED_PAGES_PARTNER_ADMIN_SECRET@#$HOSTED_PAGES_PARTNER_ADMIN_SECRET#g" -e "s#@STORAGE_BASE_DIR@#$BASE_DIR/web#g" -e "s#@DELIVERY_HTTP_BASE_URL@#https://dontknow.com#g" -e "s#@DELIVERY_RTMP_BASE_URL@#rtmp://reallydontknow.com#g" -e "s#@DELIVERY_ISS_BASE_URL@#https://honesttogodihavenoidea.com#g"  -e "s/@ADMIN_CONSOLE_PASSWORD@/$ADMIN_CONSOLE_PASSWORD/g"  -e "s/@PLAY_PARTNER_ADMIN_SECRET@/$PLAY_PARTNER_ADMIN_SECRET/g" -e "s#@WWW_HOST@#$KALTURA_FULL_VIRTUAL_HOST_NAME#g" -e "s#@TEMPLATE_PARTNER_ADMIN_PASSWORD@#$TEMPLATE_PARTNER_ADMIN_PASSWORD#g" -e "s#@HOSTED_PAGES_PARTNER_SECRET@#$HOSTED_PAGES_PARTNER_SECRER#g" -e "s#@MEDIA_PARTNER_SECRET@#$MEDIA_PARTNER_SECRET#g" -e "s#@PLAY_PARTNER_SECRET@#$PLAY_PARTNER_SECRET#g" -e "s#@TEMPLATE_PARTNER_SECRET@#$TEMPLATE_PARTNER_SECRET#g" -e "s#@PARTNER_ZERO_SECRET@#$PARTNER_ZERO_SECRET#g" -e "s#@BATCH_PARTNER_SECRET@#$BATCH_PARTNER_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_SECRET@#$ADMIN_CONSOLE_PARTNER_SECRET#g" -e "s#@VOD_PACKAGER_HOST@#$VOD_PACKAGER_HOST#g" -e "s#@VOD_PACKAGER_PORT@#$VOD_PACKAGER_PORT#g" -e "s#@IP_RANGE@#$IP_RANGE#g"  -i $DEST_FILE 
done

if [ ! -r "$BASE_DIR/app/base-config-generator.lock" ];then
        echo -en "
${CYAN}Generating client libs...
This can take a few minutes to complete, see log at $BASE_DIR/log/generate.php.log.
${NORMAL}
        "
         php $BASE_DIR/app/generator/generate.php >> $BASE_DIR/log/generate.php.log 2>&1 && touch "$BASE_DIR/app/base-config-generator.lock"
fi

set +e

# in case we use Percona, change the motnit rc file
if rpm -qa "Percona-Server-server*" 2>/dev/null;then
    cp $BASE_DIR/app/configurations/monit/monit.avail/percona.rc $BASE_DIR/app/configurations/monit/monit.avail/percona.rc.backup
    sed -i s/@HOSTNAME@/`hostname`/ $BASE_DIR/app/configurations/monit/monit.avail/percona.rc
    if [ `ps -ef | grep monit | grep -v grep | wc -l` -ne 0 ]; then
        echo "Reloading monit"
        /opt/kaltura/bin/monit reload
    fi
fi

ln -sf $BASE_DIR/app/configurations/logrotate/kaltura_base /etc/logrotate.d/
ln -sf $BASE_DIR/app/configurations/logrotate/kaltura_api /etc/logrotate.d/
touch  "$BASE_DIR/app/base-config.lock"

find $BASE_DIR/app/cache/ $BASE_DIR/log -type d -exec chmod 775 {} \; 
find $BASE_DIR/app/cache/ $BASE_DIR/log -type f -exec chmod 664 {} \; 
chown -R kaltura.apache $BASE_DIR/app/cache/ $BASE_DIR/log
chmod 775 $BASE_DIR/web/content
if [ -d /usr/lib/red5/webapps/oflaDemo ];then
        ln -sf $BASE_DIR/web/content/webcam /usr/lib/red5/webapps/oflaDemo/streams
fi
KMC_PATH=`ls -ld $BASE_DIR/web/flash/kmc/v* 2>/dev/null|awk -F " " '{print $NF}' |tail -1`
KMC_LOGIN_PATH=`ls -ld $BASE_DIR/web/flash/kmc/login/v* 2>/dev/null|awk -F " " '{print $NF}' |tail -1`
if [ -d "$KMC_PATH" -a -d "$KMC_LOGIN_PATH" ];then
        KMC_VERSION=`basename $KMC_PATH`
        KMC_LOGIN_VERSION=`basename $KMC_LOGIN_PATH`
        sed -i "s#\(@KMC_VERSION@\)#$KMC_VERSION#g" $BASE_DIR/bin/sanity_config.ini
        sed -i "s#\(@KMC_LOGIN_VERSION@\)#$KMC_LOGIN_VERSION#g" $BASE_DIR/bin/sanity_config.ini
fi


echo -e "${BRIGHT_BLUE}Configuration of $DISPLAY_NAME finished successfully!${NORMAL}"
send_install_becon `basename $0` $ZONE install_success 0
write_last_base_version
#if [ -x /etc/init.d/httpd ];then
#	service httpd reload
#fi

