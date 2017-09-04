#!/bin/sh -e
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
        OUT="ERROR: Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
        echo -e $OUT
        exit 3
fi
. $KALTURA_FUNCTIONS_RC

RELEASE=`lsb_release -r -s|awk -F . '{print $1}'`
if ! rpm -q epel-release;then
        rpm -ihv https://dl.fedoraproject.org/pub/epel/epel-release-latest-$RELEASE.noarch.rpm
fi
if [ $RELEASE = 6 ];then
# unfortunately, we need Python >= 2.7 for this to work, thus, in RHEL/CentOS 6, we need to rely on the SCO repo
# therefore, we also cannot install the PIP modules in the kaltura-live-dvr %pre phase, we need to do it here instead
        if ! rpm -q centos-release-scl-rh;then
                rpm -ihv http://mirror.centos.org/centos/6/extras/x86_64/Packages/centos-release-scl-rh-2-3.el6.centos.noarch.rpm
        fi
        yum install python27 -y
        echo '. /opt/rh/python27/enable' >> /etc/profile.d/python.sh
        . /etc/profile.d/python.sh
        yum install python27-python-pip python27-python-devel  -y
else
        yum install -y python2-pip python-devel
fi
yum install -y gcc
for MOD in poster psutil m3u8 schedule pycrypto;do
        pip install $MOD
done
yum install -y kaltura-livedvr
