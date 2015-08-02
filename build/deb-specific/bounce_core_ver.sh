#!/bin/sh

if [ $# -lt 2 ];then
	echo "Usage: $0 CORE_VERSION DIST"
	exit 1
fi
VER=$1
DIST=$2
BASE_CHECKOUT=/home/jess/sources/platform-install-packages/deb/
cd $BASE_CHECKOUT
for COMP in kaltura-base kaltura-front kaltura-batch ;do  
	CHLOG_FILE=$COMP/debian/changelog
	if [ -f $CHLOG_FILE ];then
		dch -v $VER-1 "Switching to $VER" -D $DIST -c $CHLOG_FILE 
		rm -f $BASE_CHECKOUT/$COMP/debian/br.* $BASE_CHECKOUT/$COMP/rev.*
	fi
done
