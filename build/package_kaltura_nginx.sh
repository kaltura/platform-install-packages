#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_core.sh
#         USAGE: ./package_kaltura_core.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/10/14 08:46:43 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi
wget $KALTURA_NGINX_SECURE_TOKEN_URI -O$RPM_SOURCES_DIR/nginx-secure-token-module-$KALTURA_NGINX_SECURE_TOKEN_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-secure-token-module-$KALTURA_NGINX_SECURE_TOKEN_VERSION.zip"
wget $KALTURA_NGINX_AKAMAI_TOKEN_VALIDATE_URI -O$RPM_SOURCES_DIR/nginx-akamai-token-validate-module-$KALTURA_NGINX_AKAMAI_TOKEN_VALIDATE_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-akamai-token-validate-module-$KALTURA_NGINX_AKAMAI_TOKEN_VALIDATE_VERSION.zip"
wget $KALTURA_NGINX_VOD_URI -O$RPM_SOURCES_DIR/nginx-vod-module-$KALTURA_NGINX_VOD_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-vod-module-$KALTURA_NGINX_VOD_VERSION.zip"
wget $NGINX_VTS_URI -O$RPM_SOURCES_DIR/nginx-module-vts-$NGINX_VTS_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-module-vts-$NGINX_VTS_VERSION.zip"
wget $NGINX_URI -O$RPM_SOURCES_DIR/kaltura-nginx-$NGINX_VERSION.tar.gz
echo "Packaged into $RPM_SOURCES_DIR/kaltura-nginx-$NGINX_VERSION.tar.gz"
wget $NGX_AWS_AUTH_URI -O$RPM_SOURCES_DIR/ngx_aws_auth-$NGX_AWS_AUTH_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/ngx_aws_auth-$NGX_AWS_AUTH_VERSION.zip"

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-nginx.spec
fi
