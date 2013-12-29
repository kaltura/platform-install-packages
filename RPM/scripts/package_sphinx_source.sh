#!/bin/bash -e 
#===============================================================================
#          FILE: package_sphinx_source.sh
#         USAGE: ./package_sphinx_source.sh 
#   DESCRIPTION: Retrieve new Sphinx source and package as a tar ball 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy, <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/29/13 03:15:11 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ ! -x `which svn 2>/dev/null` ];then
	echo "Need to install subversion."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
svn export -q --force $SPHINX_URI -r$SPHINX_REVISION $SOURCE_PACKAGING_DIR/$SPHINX_RPM_PACKAGE_NAME-$SPHINX_VERSION
cd $SOURCE_PACKAGING_DIR 
tar zcf $RPM_SOURCES_DIR/$SPHINX_RPM_PACKAGE_NAME-$SPHINX_VERSION.tar.gz $SPHINX_RPM_PACKAGE_NAME-$SPHINX_VERSION
echo "Packaged rev $SPHINX_REVISION written to: $RPM_SOURCES_DIR/$SPHINX_RPM_PACKAGE_NAME-$SPHINX_VERSION.tar.gz."
rpmbuild -ba $RPM_SPECS_DIR/$SPHINX_RPM_PACKAGE_NAME.spec

