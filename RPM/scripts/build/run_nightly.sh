#!/bin/bash - 
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
mkdir -p tmp
RPMS_BASE_DIR=/home/jess/rpmbuild/RPMS
KALTURA_SERVER_VERSION=`curl https://api.github.com/repos/kaltura/server -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`

# set release [revision] to 1, if the new ver to push is the same as the one we currenly have on the nightly repo, however, then change to current revision + 1 instead.
KALTURA_SERVER_NEXT_REVISION=1
sudo yum clean all
KALTURA_SERVER_REMOTE_VERSION=`yum info kaltura-base | grep Version|awk -F ": " '{print $2}'`
if [ "$KALTURA_SERVER_VERSION" = "$KALTURA_SERVER_REMOTE_VERSION" ];then
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
HTML5LIB_VERSION=`curl https://api.github.com/repos/kaltura/mwembed -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`
HTML5LIB_VERSION=v2.22
HTML5LIB_NEXT_REVISION=1
HTML5LIB_REMOTE_VERSION=`yum info kaltura-html5lib | grep Version|awk -F ": " '{print $2}'`
if [ "$HTML5LIB_VERSION" = "$HTML5LIB_REMOTE_VERSION" ];then
	HTML5LIB_REMOTE_REVISION=`yum info kaltura-html5lib | grep Release|awk -F ": " '{print $2}'`
	HTML5LIB_NEXT_REVISION=`expr $HTML5LIB_REMOTE_REVISION + 1`
fi

mv ~/.rpmmacros ~/.rpmmacros.stable
sed -e "s#@KMC_VERSION@#$KMC_VERSION#" -e "s#@KMC_LOGIN_VERSION@#$KMC_LOGIN_VERSION#" -e "s#@HTML5LIB_VERSION@#$HTML5LIB_VERSION#" `dirname $0`/.rpmmacros.tmplt > ~/.rpmmacros  

. `dirname $0`/sources.rc 
`dirname $0`/bounce_rpm_ver.sh kaltura-kmc.spec $KMC_VERSION $KMC_NEXT_REVISION
`dirname $0`/bounce_rpm_ver.sh kaltura-html5lib.spec $HTML5LIB_VERSION $HTML5LIB_NEXT_REVISION
`dirname $0`/bounce_rpm_ver.sh kaltura-html5-studio.spec $HTML5_APP_STUDIO_VERSION $HTML5_APP_STUDIO_NEXT_REVISION
`dirname $0`/bounce_rpm_ver.sh kaltura-base.spec `echo $KALTURA_SERVER_VERSION|awk -F "-" '{print $2}'` $KALTURA_SERVER_NEXT_REVISION

rpmbuild -ba $RPM_SPECS_DIR/kaltura-base.spec
~/scripts/push_rpm.sh $RPMS_BASE_DIR/noarch/kaltura-base-$KALTURA_SERVER_VERSION-1.noarch.rpm nightly1

svn export --force --quiet $KMC_UICONF_URI $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/uiconf/kaltura/kmc
cd $SOURCE_PACKAGING_DIR
wget $KMC_URI -O $KMC_RPM_NAME-$KMC_VERSION.zip
unzip -qo $KMC_RPM_NAME-$KMC_VERSION.zip
wget $KMC_LOGIN_URI -O $KMC_RPM_NAME-$KMC_LOGIN_VERSION.zip
unzip -oq $KMC_RPM_NAME-$KMC_LOGIN_VERSION.zip
rm -rf $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/login
mkdir -p $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/login
mv $KMC_LOGIN_VERSION $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/login
mv $KMC_VERSION $KMC_RPM_NAME-$KMC_VERSION
find $KMC_RPM_NAME-$KMC_VERSION -type f -exec chmod -x {} \;
tar jcf $RPM_SOURCES_DIR/$KMC_RPM_NAME-$KMC_VERSION.tar.bz2 $KMC_RPM_NAME-$KMC_VERSION
# flash things DO NOT need exec perms.
echo "Packaged into $RPM_SOURCES_DIR/$KMC_RPM_NAME-$KMC_VERSION.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$KMC_RPM_NAME.spec
~/scripts/push_rpm.sh $RPMS_BASE_DIR/noarch/$KMC_RPM_NAME-$KMC_VERSION-1.noarch.rpm nightly1

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
~/scripts/push_rpm.sh $RPMS_BASE_DIR/noarch/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION-1.noarch.rpm nightly1


HTML5LIB_VERSIONS="$HTML5LIB_VERSIONS $HTML5LIB_VERSION"
cd $SOURCE_PACKAGING_DIR
for HTML5LIB_VERSION in $HTML5LIB_VERSIONS;do
	if ! tar ztf  $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz ;then
		wget $HTML5LIB_BASE_URI/$HTML5LIB_VERSION -O $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz
		tar zxf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz 
		rm -rf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
		mv `ls -rtd kaltura-mwEmbed-* | tail -1` $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
		tar zcf $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
		echo "Packaged into $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz"
	fi
done
rpmbuild -ba $RPM_SPECS_DIR/$HTML5LIB_RPM_NAME.spec
~/scripts/push_rpm.sh $RPMS_BASE_DIR/noarch/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION-1.noarch.rpm nightly1
