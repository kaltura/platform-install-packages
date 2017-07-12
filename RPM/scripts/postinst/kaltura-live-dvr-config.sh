#!/bin/sh -e
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
        OUT="ERROR: Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
        echo -e $OUT
        exit 3
fi
. $KALTURA_FUNCTIONS_RC

RELEASE=`lsb_release -r -s|awk -F . '{print $1}'`
rpm -Uhv https://dl.fedoraproject.org/pub/epel/epel-release-latest-$RELEASE.noarch.rpm || true
if [ $RELEASE = 6 ];then
# unfortunately, we need Python >= 2.7 for this to work, thus, in RHEL/CentOS 6, we need to rely on the SCO repo
# therefore, we also cannot install the PIP modules in the kaltura-live-dvr %pre phase, we need to do it here instead
        rpm -ihv http://mirror.centos.org/centos/6/extras/x86_64/Packages/centos-release-scl-rh-2-3.el6.centos.noarch.rpm
        yum install python27 -y
        echo '. /opt/rh/python27/enable' >> /etc/profile.d/python.sh
	. /etc/profile.d/python.sh
fi

for MOD in poster psutil m3u8 schedule pycrypto;do
	pip install $MOD
done
yum install -y kaltura-live-dvr

