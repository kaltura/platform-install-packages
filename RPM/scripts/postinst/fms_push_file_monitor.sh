#!/bin/bash - 
#===============================================================================
#          FILE: fms_push_file.sh
#         USAGE: ./fms_push_file.sh 
#   DESCRIPTION:
#       OPTIONS: </path/to/local/file> <fms_host> [--debug]---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), jess.portnoy@kaltura.com
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 11/29/2013 03:26:51 PM IST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ $# -lt 2 ];then
    echo "Usage: $0 </path/to/local/file> <fms_url> [--debug]"
    echo "Example for <fms_url> rtmp://FMS_HOSTNAME/oflaDemo/"
    exit 1
fi
ASSET=$1
FMS_HOSTNAME=$2
if [ "$3" = '--debug' ];then
    DEBUG=1
fi
FILENAME=`basename $ASSET`
if which avconv 2>/dev/null;then
    ENCODER=avconv
else
    ENCODER=ffmpeg
fi
OUT=`$ENCODER -re -i $ASSET -c copy -f flv "$FMS_HOSTNAME/$FILENAME" 2>&1`
RC=$?
if [ $RC -ne 0 ];then
    echo "FAILED: $OUT"
    NAGIOS_RC=2
else
    echo "OK:) $FILENAME successfully uploaded."
    if [ -n "$DEBUG" ]; then
	echo $OUT
    fi
fi
if [ $RC -gt 2 ] ;then
    echo "UNKNOWN issue, we got $RC from $ENCODER"
    echo $OUT
    NAGIOS_RC=3
fi
exit $NAGIOS_RC
