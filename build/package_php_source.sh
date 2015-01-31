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

wget $LIBMCRYPT_URI -O $RPM_SOURCES_DIR/libmcrypt-$LIBMCRYPT_VERSION.tar.gz
if [ $? -eq 0 ];then
	echo "Packaged to libmcrypt-$LIBMCRYPT_VERSION.tar.gz"
else
	echo "Unable to download $LIBMCRYPT_URI" >&2
	exit 1
fi

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-libmcrypt.spec
	kaltura_install kaltura-libmcrypt $LIBMCRYPT_VERSION
	kaltura_install kaltura-libmcrypt-devel $LIBMCRYPT_VERSION
	rpmbuild -ba $RPM_SPECS_DIR/php-mcrypt.spec
fi


wget $LIBMEMCACHED_URI -O $RPM_SOURCES_DIR/libmemcached-$LIBMEMCACHED_VERSION.tar.gz
if [ $? -eq 0 ];then
	echo "Packaged to libmemcached-$LIBMEMCACHED_VERSION.tar.gz"
else
	echo "Unable to download $LIBMEMCACHED_URI" >&2
	exit 1
fi
cd $RPM_SOURCES_DIR
tar xzf $RPM_SOURCES_DIR/libmemcached-$LIBMEMCACHED_VERSION.tar.gz
rm libmemcached-$LIBMEMCACHED_VERSION/libhashkit/hsieh.cc
rm -f libmemcached-$LIBMEMCACHED_VERSION-exhsieh.tar.gz
tar czf libmemcached-$LIBMEMCACHED_VERSION-exhsieh.tar.gz libmemcached-$LIBMEMCACHED_VERSION
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-libmemcached.spec
	kaltura_install kaltura-libmemcached $LIBMEMCACHED_VERSION
	kaltura_install kaltura-libmemcached-devel $LIBMEMCACHED_VERSION
fi


wget $MEMCACHED_URI -O $RPM_SOURCES_DIR/memcached-$MEMCACHED_VERSION.tgz
if [ $? -eq 0 ];then
	echo "Packaged to memcached-$MEMCACHED_VERSION.tgz"
else
	echo "Unable to download $MEMCACHED_URI" >&2
	exit 1
fi
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/php-pecl-memcached.spec
fi



wget $LIBSSH_URI -O $RPM_SOURCES_DIR/ssh2-$LIBSSH_VERSION.tgz
if [ $? -eq 0 ];then
	echo "Packaged to ssh2-$LIBSSH_VERSION.tgz"
else
	echo "Unable to download $LIBSSH_URI" >&2
	exit 1
fi
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/php-pecl-ssh2.spec
fi
