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
# unfortunately, we need Python >= 2.7 for this to work, thus, in RHEL/CentOS 6, we need to rely on the SCO repo. Since we're also using RPM packages for the Python modules becasue we cannot rely on connectivity to the PIP repo on the target ENVs and our RPM packages are built against the SCO version of python27, we install python27 regardless of whether we're on el6 or 7.

if ! rpm -q centos-release-scl-rh;then
	rpm -ihv http://mirror.centos.org/centos/$RELEASE/extras/x86_64/Packages/centos-release-scl-rh-2-2.el${RELEASE}.centos.noarch.rpm
fi
yum install python27 -y
echo '. /opt/rh/python27/enable' >> /etc/profile.d/python.sh
. /etc/profile.d/python.sh

yum install -y kaltura-live kaltura-livedvr 
/opt/kaltura/bin/kaltura-live-config.sh

