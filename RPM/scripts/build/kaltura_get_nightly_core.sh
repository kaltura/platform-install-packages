#!/bin/bash - 
#===============================================================================
#          FILE: get_nightly.sh
#         USAGE: ./get_nightly.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 08/17/14 09:08:08 EDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 

for i in unzip wget;do
	EX_PATH=`which $i 2>/dev/null`
	if [ -z "$EX_PATH" -o ! -x "$EX_PATH" ];then
		echo "Need to install $i."
		exit 2
	fi
done

GITHUB_API=https://api.github.com
NIGHTLY_BRANCH=`curl $GITHUB_API/repos/kaltura/server -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/'| sed 's@\s*@@g'`
TMPDIR=/tmp/nightly-core-$NIGHTLY_BRANCH
wget https://github.com/kaltura/server/archive/$NIGHTLY_BRANCH.zip -O$RPM_SOURCES_DIR/$NIGHTLY_BRANCH.zip
mkdir -p $TMPDIR 
unzip -o -j $RPM_SOURCES_DIR/$NIGHTLY_BRANCH.zip server-$NIGHTLY_BRANCH/configurations/base.ini -d "$TMPDIR"
#      - parse the base.ini and kmc_config.ini to locate versions for
#        - HTML5
#        - KMC
#        - KDP3 
#        - Studio

for i in kmc_login_version kdp_wrapper_version kdp3_wrapper_version html5_version clipapp_version studio_version kmc_version;do
	grep "$i\s*=\s*v" /tmp/nightly-core/base.ini|awk -F "=" '{print $2}'
done

#-------    - if kmc_version -ne version in sources.rc
KMC_BRANCH=`curl $GITHUB_API/repos/kaltura/kmc -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/'|sed 's@\s*@@g'`
wget --no-check-certificate https://github.com/kaltura/kmc/raw/master/KMC/config/config.ini -O$TMPDIR/config.ini
#extrace kmc_version.ini from archive and check versions of stuff
#- set versions in acrrodence in:
#       - spec files
#       - .rmpmacros
#       - sources.rc


