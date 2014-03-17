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
PREFIX=/opt/kaltura
MOUNT_DIR=$PREFIX/web
# create user/group, and update permissions
groupadd -r kaltura -g7373 2>/dev/null || true
useradd -M -r -u7373 -d $PREFIX -s /bin/bash -c "Kaltura server" -g kaltura kaltura 2>/dev/null || true
getent group apache >/dev/null || groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d /var/www -c "Apache" apache
usermod -g kaltura kaltura 2>/dev/null || true

if grep -q "^Domain" $IDMAPD_CONFFILE;then
        sed -i "s@^Domain\s*=\s*.*@Domain = $DOMAIN@g" $IDMAPD_CONFFILE
else
        echo "Domain = $DOMAIN" >> $IDMAPD_CONFFILE
fi
if grep -q "^Nobody-User" $IDMAPD_CONFFILE;then
        sed -i "s@^Nobody-User\s*=\s*.*@Nobody-User = $NOBODY_USER@g" $IDMAPD_CONFFILE
        sed -i "s@^Nobody-Group\s*=\s*.*@Nobody-Group = $NOBODY_GROUP@g" $IDMAPD_CONFFILE
else
        echo "Nobody-User = $NOBODY_USER" >>$IDMAPD_CONFFILE
        echo "Nobody-User = $NOBODY_GROUP" >>$IDMAPD_CONFFILE
fi
echo "$NFS_HOST:$MOUNT_DIR $MOUNT_DIR nfs4" >> /etc/fstab
for DAEMON in rpcbind rpcidmapd ;do
	service $DAEMON restart
done
nfsidmap -c
mount $MOUNT_DIR
