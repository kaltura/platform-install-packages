#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura.sh
#         USAGE: ./package_kaltura.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/23/14
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC

cd $BUILD_DIR

./package_kaltura_core.sh
./package_kaltura_clipapp.sh
./package_kaltura_dwh.sh
./package_kaltura_flex_wrapper.sh
./package_kaltura_html5lib.sh
./package_kaltura_html5-studio.sh
./package_kaltura_kclip.sh
./package_kaltura_kcw.sh
./package_kaltura_kdp.sh
./package_kaltura_kdp3.sh
./package_kaltura_kdp3wrapper.sh
./package_kaltura_kdpwrapper.sh
./package_kaltura_kmc_appstudio.sh
./package_kaltura_kmc.sh
./package_kaltura_krecord.sh
./package_kaltura_ksr.sh
./package_kaltura_kupload.sh
./package_kaltura_kvpm.sh
./package_kaltura_media-server.sh
./package_kaltura_monit.sh
./package_kaltura_nginx.sh
./package_kaltura_postinst.sh
./package_kaltura_studio.sh


if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-base.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-batch.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-front.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-mysql-config.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-opencore-amr.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-release.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-rtmpdump.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-segmenter.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-server.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-sshpass.spec
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-widgets.spec
fi


