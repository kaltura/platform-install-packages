#!/bin/sh -e
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
        OUT="ERROR: Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
        echo -e $OUT
        exit 3
fi
. $KALTURA_FUNCTIONS_RC

cat <<EOF > /etc/yum.repos.d/datastax.repo
[datastax]
name = DataStax Repo for Apache Cassandra
baseurl = https://rpm.datastax.com/community
enabled = 1
gpgcheck = 0
EOF

RELEASE=`lsb_release -r -s|awk -F . '{print $1}'`
rpm -Uhv https://dl.fedoraproject.org/pub/epel/epel-release-latest-$RELEASE.noarch.rpm || true
yum install -y dsc22 cassandra22 nginx
yum install -y kaltura-live-analytics
if [ $RELEASE = 6 ];then
        # we need to enable to SCLO repos and install python27 for cqlsh
        rpm -ihv http://mirror.centos.org/centos/6/extras/x86_64/Packages/centos-release-scl-rh-2-3.el6.centos.noarch.rpm
        yum install python27 -y
        . /opt/rh/python27/enable
fi

KALTURA_BASE_DIR=/opt/kaltura
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        . $ANSFILE
else
        echo -e "${CYAN}Cassandra host [127.0.0.1]:${NORMAL} "
        read -e CASSANDRA_HOST
        if [ -z "$CASSANDRA_HOST" ];then
                CASSANDRA_HOST=127.0.0.1
        fi
        echo -e "${CYAN}Live Stats port [8888]:${NORMAL} "
        read -e LIVE_ANALYTICS_STATS_PORT
        if [ -z "$LIVE_ANALYTICS_STATS_PORT" ];then
                LIVE_ANALYTICS_STATS_PORT=8888
        fi
        echo -e "${CYAN}IP2Location username:${NORMAL} "
        read -e IP2LOC_USER
        echo -e "${CYAN}IP2Location password:${NORMAL} "
        read -s IP2LOC_PASS
fi
IP2LOC_TMPDIR=/tmp/ip2loc/
mkdir -p $IP2LOC_TMPDIR
cd $IP2LOC_TMPDIR
wget "http://www.ip2location.com/download?productcode=DB3LITEBIN&login=$IP2LOC_USER&password=$IP2LOC_PASS" -O $IP2LOC_TMPDIR/DB3LITE.zip
unzip $IP2LOC_TMPDIR/DB3LITE.zip
mv IP2LOCATION-LITE-DB3.BIN /opt/kaltura/data/geoip/
cd -
rm -rf $IP2LOC_TMPDIR

LIVE_ANALYTICS_CONFIG_BASE_DIR=$KALTURA_BASE_DIR/app/configurations/live_analytics/
cqlsh < $LIVE_ANALYTICS_CONFIG_BASE_DIR/cassandra/create_cassandra_tables.cql
sed "s#@CASSANDRA_HOST@#$CASSANDRA_HOST#g"  $LIVE_ANALYTICS_CONFIG_BASE_DIR/logrotate/live_stats.template > $LIVE_ANALYTICS_CONFIG_BASE_DIR/logrotate/live_stats
sed "s#@CASSANDRA_HOST@#$CASSANDRA_HOST#g" $LIVE_ANALYTICS_CONFIG_BASE_DIR/config.template.properties > /opt/kaltura/lib/config.properties
ln -sf $LIVE_ANALYTICS_CONFIG_BASE_DIR/logrotate/live_stats /etc/logrotate.d/kaltura_live_stats
ln -sf $LIVE_ANALYTICS_CONFIG_BASE_DIR/cron/live_stats /etc/cron.d/kaltura_live_stats
sed "s#@LIVE_ANALYTICS_STATS_PORT@#$LIVE_ANALYTICS_STATS_PORT#g" $LIVE_ANALYTICS_CONFIG_BASE_DIR/nginx/live.template.conf > $LIVE_ANALYTICS_CONFIG_BASE_DIR/nginx/live.conf
ln -sf $LIVE_ANALYTICS_CONFIG_BASE_DIR/nginx/live.conf /etc/nginx/conf.d/
service nginx restart
service live-analytics-driver restart
