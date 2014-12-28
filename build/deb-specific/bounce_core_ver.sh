#!/bin/sh

if [ $# -lt 1 ];then
	echo "Usage: $0 CORE_VERSION"
	exit 1
fi
VER=$1
DIST=ce
BASE_CHECKOUT=/home/jess/sources/platform-install-packages/deb/
cd $BASE_CHECKOUT
for COMP in kaltura-base kaltura-front kaltura-batch kaltura-release kaltura-server ;do  
	CHLOG_FILE=$COMP/debian/changelog
	if [ -f $CHLOG_FILE ];then
		dch -v $VER "Switching to $VER" -D $DIST -c $CHLOG_FILE 
		rm -f $BASE_CHECKOUT/$COMP/debian/br.* $BASE_CHECKOUT/$COMP/rev.*
	fi
done
