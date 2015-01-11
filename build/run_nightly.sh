#!/bin/bash -e 
#===============================================================================
#          FILE: run.sh
#         USAGE: ./run.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/01/14 10:17:05 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ ! -x `which wget 2>/dev/null` ];then
	echo "Need to install wget."
	exit 2
fi
if [ ! -x `which svn 2>/dev/null` ];then
	echo "Need to install svn."
	exit 2
fi
rm -f /tmp/nightly.log

mkdir -p tmp
RPMS_BASE_DIR=/home/jess/rpmbuild/RPMS
KALTURA_SERVER_VERSION=`curl https://api.github.com/repos/kaltura/server -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`
KALTURA_SHORT_SERVER_VERSION=`echo $KALTURA_SERVER_VERSION|awk -F "-" '{print $2}'`

# set release [revision] to 1, if the new ver to push is the same as the one we currenly have on the nightly repo, however, then change to current revision + 1 instead.
KALTURA_SERVER_NEXT_REVISION=1
sudo yum clean all
KALTURA_SERVER_REMOTE_VERSION=`yum info kaltura-base | grep Version|awk -F ": " '{print $2}'`
if [ "$KALTURA_SHORT_SERVER_VERSION" = "$KALTURA_SERVER_REMOTE_VERSION" ];then
	KALTURA_SERVER_REMOTE_REVISION=`yum info kaltura-base | grep Release|awk -F ": " '{print $2}'`
	KALTURA_SERVER_NEXT_REVISION=`expr $KALTURA_SERVER_REMOTE_REVISION + 1`
fi
wget https://github.com/kaltura/server/archive/$KALTURA_SERVER_VERSION.zip -O /home/jess/rpmbuild/SOURCES/$KALTURA_SERVER_VERSION.zip 
unzip -qo -j /home/jess/rpmbuild/SOURCES/$KALTURA_SERVER_VERSION.zip server-$KALTURA_SERVER_VERSION/configurations/base.ini -d "tmp/"
KMC_LOGIN_VERSION=`grep ^kmc_login_version tmp/base.ini |awk -F "=" '{print $2}'|sed 's@\s*@@g'`
KMC_VERSION=`grep ^kmc_version tmp/base.ini |awk -F "=" '{print $2}'|sed 's@\s*@@g'`
KMC_NEXT_REVISION=1
KMC_REMOTE_VERSION=`yum info kaltura-kmc | grep Version|awk -F ": " '{print $2}'`
if [ "$KMC_VERSION" = "$KMC_REMOTE_VERSION" ];then
	KMC_REMOTE_REVISION=`yum info kaltura-kmc | grep Release|awk -F ": " '{print $2}'`
	KMC_NEXT_REVISION=`expr $KMC_REMOTE_REVISION + 1`
fi

HTML5_APP_STUDIO_VERSION=`grep ^studio_version tmp/base.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
HTML5_APP_STUDIO_NEXT_REVISION=1
HTML5_APP_STUDIO_REMOTE_VERSION=`yum info kaltura-html5-studio | grep Version|awk -F ": " '{print $2}'`
if [ "$HTML5_APP_STUDIO_VERSION" = "$HTML5_APP_STUDIO_REMOTE_VERSION" ];then
	HTML5_APP_STUDIO_REMOTE_REVISION=`yum info kaltura-html5-studio | grep Release|awk -F ": " '{print $2}'`
	HTML5_APP_STUDIO_NEXT_REVISION=`expr $HTML5_APP_STUDIO_REMOTE_REVISION + 1`
fi
HTML5LIB_DEFAULT_BRANCH=`curl https://api.github.com/repos/kaltura/mwembed -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`
wget --no-check-certificate https://github.com/kaltura/mwEmbed/raw/$HTML5LIB_DEFAULT_BRANCH/includes/DefaultSettings.php -O tmp/DefaultSettings.php; 
dos2unix tmp/DefaultSettings.php
HTML5LIB_VERSION="v`grep wgMwEmbedVersion tmp/DefaultSettings.php |sed 's@^\s*$wgMwEmbedVersion\s*=\s*.\([0-9.]*\)..@\1@'`"
HTML5LIB_NEXT_REVISION=1
HTML5LIB_REMOTE_VERSION=`yum info kaltura-html5lib | grep Version|awk -F ": " '{print $2}'`
if [ "$HTML5LIB_VERSION" = "$HTML5LIB_REMOTE_VERSION" ];then
	HTML5LIB_REMOTE_REVISION=`yum info kaltura-html5lib | grep Release|awk -F ": " '{print $2}'`
	HTML5LIB_NEXT_REVISION=`expr $HTML5LIB_REMOTE_REVISION + 1`
fi
cp ~/rpmbuild/SOURCES/kmc_config.ini ~/rpmbuild/SOURCES/kmc_config.ini.stable
sed -i "s@\(.*html5_version.*\)\s*=.*@\1= $HTML5LIB_VERSION@g" ~/rpmbuild/SOURCES/kmc_config.ini
mv ~/.rpmmacros ~/.rpmmacros.stable
sed -e "s#@KMC_VERSION@#$KMC_VERSION#" -e "s#@KMC_LOGIN_VERSION@#$KMC_LOGIN_VERSION#" -e "s#@HTML5LIB_VERSION@#$HTML5LIB_VERSION#" `dirname $0`/.rpmmacros.tmplt > ~/.rpmmacros  

. `dirname $0`/sources.rc 
`dirname $0`/rpm-specific/bounce_rpm_ver.sh kaltura-kmc.spec $KMC_VERSION $KMC_NEXT_REVISION "Kaltura night build"
`dirname $0`/rpm-specific/bounce_rpm_ver.sh kaltura-html5lib.spec $HTML5LIB_VERSION $HTML5LIB_NEXT_REVISION "Kaltura night build"
`dirname $0`/rpm-specific/bounce_rpm_ver.sh kaltura-html5-studio.spec $HTML5_APP_STUDIO_VERSION $HTML5_APP_STUDIO_NEXT_REVISION "Kaltura night build"
`dirname $0`/rpm-specific/bounce_rpm_ver.sh kaltura-base.spec $KALTURA_SHORT_SERVER_VERSION $KALTURA_SERVER_NEXT_REVISION "Kaltura night build"

rpmbuild -ba $RPM_SPECS_DIR/kaltura-base.spec
`dirname $0`/rpm-specific/push_rpm.sh $RPMS_BASE_DIR/noarch/kaltura-base-$KALTURA_SHORT_SERVER_VERSION-$KALTURA_SERVER_NEXT_REVISION.noarch.rpm $KALTURA_SHORT_SERVER_VERSION 
echo "Pushed kaltura-base-$KALTURA_SHORT_SERVER_VERSION-$KALTURA_SERVER_NEXT_REVISION.noarch.rpm to $KALTURA_SHORT_SERVER_VERSION" >> /tmp/nightly.log
`dirname $0`/package_kaltura_kmc.sh
rpmbuild -ba $RPM_SPECS_DIR/$KMC_RPM_NAME.spec
`dirname $0`/rpm-specific/push_rpm.sh $RPMS_BASE_DIR/noarch/$KMC_RPM_NAME-$KMC_VERSION-$KMC_NEXT_REVISION.noarch.rpm $KALTURA_SHORT_SERVER_VERSION
echo "Pushed $RPMS_BASE_DIR/noarch/$KMC_RPM_NAME-$KMC_VERSION-$KMC_NEXT_REVISION.noarch.rpm to $KALTURA_SHORT_SERVER_VERSION" >> /tmp/nightly.log

mkdir -p $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION
rm -rf $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION/*
wget -q $HTML5_APP_STUDIO_URI -O$SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION/$HTML5_APP_STUDIO_NORMALIZED_ARCHIVE_NAME
cd $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION
unzip -qq $HTML5_APP_STUDIO_NORMALIZED_ARCHIVE_NAME
rm $HTML5_APP_STUDIO_NORMALIZED_ARCHIVE_NAME
cd ../
tar jcf  $RPM_SOURCES_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION.tar.bz2 $HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION
echo "Packaged into $RPM_SOURCES_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$HTML5_APP_STUDIO_RPM_NAME.spec
`dirname $0`/rpm-specific/push_rpm.sh $RPMS_BASE_DIR/noarch/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION-$HTML5_APP_STUDIO_NEXT_REVISION.noarch.rpm $KALTURA_SHORT_SERVER_VERSION
echo "Pushed $HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION-$HTML5_APP_STUDIO_NEXT_REVISION.noarch.rpm to $KALTURA_SHORT_SERVER_VERSION" >> /tmp/nightly.log

HTML5LIB_VERSIONS="$HTML5LIB_VERSIONS $HTML5LIB_VERSION"
#cd $SOURCE_PACKAGING_DIR
#for HTML5LIB_VERSION in $HTML5LIB_VERSIONS;do
#	if ! tar ztf  $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz ;then
#		wget $HTML5LIB_BASE_URI/$HTML5LIB_VERSION -O $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz
#		tar zxf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz 
#		rm -rf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
#		mv `ls -rtd kaltura-mwEmbed-* | tail -1` $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
#		tar zcf $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
#		echo "Packaged into $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz"
#	fi
#done
#rpmbuild -ba $RPM_SPECS_DIR/$HTML5LIB_RPM_NAME.spec
#~/scripts/push_rpm.sh $RPMS_BASE_DIR/noarch/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION-$HTML5LIB_NEXT_REVISION.noarch.rpm nightly1

if [ "$1" = 'launch-ec2' ];then
	. ~/csi/csi-functions.rc
	INSTANCE_ID=`start_instances $NFS_IMG 1 $SECURITY_GROUP` 
	while ! get_instance_status $ID ;do 
		echo "Waiting for instance to init.."
		sleep 10 
	done

	IP=`get_instance_ip $INSTANCE_ID`
	while ! nc $IP 22 -w1 ;do 
		echo "Waiting for instance to init.."
		sleep 10 
	done
	ec2-create-tags $INSTANCE_ID --tag Name="Kaltura-Sanity-`date`"
	scp $SSH_QUIET_OPTS -i ~/csi.pem ~/nightly/kaltura-install.sh ec2-user@$IP:/tmp
	ssh $SSH_QUIET_OPTS -t -i ~/csi.pem ec2-user@$IP sudo bash /tmp/kaltura-install.sh
	INSTANCE_HOSTNAME=`ssh $SSH_QUIET_OPTS -i ~/csi.pem ec2-user@$IP hostname 2>/dev/null`
	SQL_FILE=/tmp/$INSTANCE_HOSTNAME-reportme.`date +%d_%m_%Y`.sql
	scp $SSH_QUIET_OPTS -i ~/csi.pem ec2-user@$IP:$SQL_FILE /tmp
	#ec2-terminate-instances $INSTANCE_ID
	CSI_MACHINE=ce-csi.dev.kaltura.com
	scp $SSH_QUIET_OPTS $SQL_FILE root@$CSI_MACHINE:/tmp 
	ssh $SSH_QUIET_OPTS root@$CSI_MACHINE /opt/vhosts/csi/update_csi_db.sh $SQL_FILE $KALTURA_SHORT_SERVER_VERSION
fi
ssh root@192.168.70.100 mail -s \'Nightly Core build ready\' jess.portnoy@kaltura.com,Jonathan.Kanarek@kaltura.com < /etc/issue 
