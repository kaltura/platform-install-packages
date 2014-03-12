#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-nfs-client-config.sh
#         USAGE: ./kaltura-nfs-client-config.sh 
#   DESCRIPTION: NFS client side preps. 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 03/12/14 13:06:13 EDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ $# -ne 4 ];then
        echo "Usage: $0 <NFS host> <domain> <nobody-user> <nobody-group>"
        exit 1
fi
NFS_HOST=$1
DOMAIN=$2
NOBODY_USER=$3
NOBODY_GROUP=$4
IDMAPD_CONFFILE=/etc/idmapd.conf
MOUNT_DIR=/opt/kaltura/web
if grep -q "^Domain" $IDMAPD_CONFFILE;then
        sed -i "s@^Domain\s*=\s*.*@Domain = $DOMAIN@g" $IDMAPD_CONFFILE
else
        echo "Domain = $DOMAIN" >> $IDMAPD_CONFFILE
fi
if grep -q "^Nobody-User" $IDMAPD_CONFFILE;then
        sed -i "s@^Nobody-User\s*=\s*.*@Nobody-User = $NOBODY_USER@g" /etc/idmapd.conf
        sed -i "s@^Nobody-Group\s*=\s*.*@Nobody-Group = $NOBODY_GROUP@g" /etc/idmapd.conf
else
        echo "Nobody-User = $NOBODY_USER" >>$IDMAPD_CONFFILE
        echo "Nobody-User = $NOBODY_GROUP" >>$IDMAPD_CONFFILE
fi
echo "$NFS_HOST:$MOUNT_DIR $MOUNT_DIR nfs4" >> /etc/fstab
service rpcidmapd restart
nfsidmap -c
mount $MOUNT_DIR
