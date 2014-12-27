#!/bin/bash -e 
#===============================================================================
#          FILE: package_php_source.sh
#         USAGE: ./package_php_source.sh 
#   DESCRIPTION: Retrieve PHP source
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/17/14
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC

wget $PHP_URI -O $RPM_SOURCES_DIR/php-$PHP_VERSION.tar.bz2
if [ $? -eq 0 ];then
	echo "Packaged to php-$PHP_VERSION.tar.bz2"
else
	echo "Unable to download $PHP_URI" >&2
	exit 1
fi

wget $PHP_LIBMCRYPT_URI -O $RPM_SOURCES_DIR/libmcrypt-$PHP_LIBMCRYPT_VERSION.tar.gz
if [ $? -eq 0 ];then
	echo "Packaged to libmcrypt-$PHP_LIBMCRYPT_VERSION.tar.gz"
else
	echo "Unable to download $PHP_LIBMCRYPT_URI" >&2
	exit 1
fi
rpmbuild -ba $RPM_SPECS_DIR/kaltura-libmcrypt.spec


sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-libmcrypt-2.5.7-5.x86_64.rpm
sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-libmcrypt-devel-2.5.7-5.x86_64.rpm
rpmbuild -ba $RPM_SPECS_DIR/php-mcrypt.spec


wget $PHP_LIBMEMCACHED_URI -O $RPM_SOURCES_DIR/libmemcached-$PHP_LIBMEMCACHED_VERSION.tar.gz
if [ $? -eq 0 ];then
	echo "Packaged to libmemcached-$PHP_LIBMEMCACHED_VERSION.tar.gz"
else
	echo "Unable to download $PHP_LIBMEMCACHED_URI" >&2
	exit 1
fi
cd $RPM_SOURCES_DIR
tar -xzf $RPM_SOURCES_DIR/libmemcached-$PHP_LIBMEMCACHED_VERSION.tar.gz
rm libmemcached-$PHP_LIBMEMCACHED_VERSION/libhashkit/hsieh.cc
rm -f libmemcached-$PHP_LIBMEMCACHED_VERSION-exhsieh.tar.gz
tar -czf libmemcached-$PHP_LIBMEMCACHED_VERSION-exhsieh.tar.gz libmemcached-$PHP_LIBMEMCACHED_VERSION
rpmbuild -ba $RPM_SPECS_DIR/kaltura-libmemcached.spec


sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-libmemcached-1.0.16-2.x86_64.rpm
sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-libmemcached-devel-1.0.16-2.x86_64.rpm
wget $PHP_MEMCACHED_URI -O $RPM_SOURCES_DIR/memcached-$PHP_MEMCACHED_VERSION.tgz
if [ $? -eq 0 ];then
	echo "Packaged to memcached-$PHP_MEMCACHED_VERSION.tgz"
else
	echo "Unable to download $PHP_MEMCACHED_URI" >&2
	exit 1
fi
rpmbuild -ba $RPM_SPECS_DIR/php-pecl-memcached.spec



wget $PHP_SSH_URI -O $RPM_SOURCES_DIR/ssh2-$PHP_SSH_VERSION.tgz
if [ $? -eq 0 ];then
	echo "Packaged to ssh2-$PHP_SSH_VERSION.tgz"
else
	echo "Unable to download $PHP_SSH_URI" >&2
	exit 1
fi
rpmbuild -ba $RPM_SPECS_DIR/php-pecl-ssh2.spec

