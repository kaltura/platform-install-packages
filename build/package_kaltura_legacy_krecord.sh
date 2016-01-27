#!/bin/bash

SOURCES_FILE="./sources.rc"

if [ -r $SOURCES_FILE ];then
    . $SOURCES_FILE
fi

component="krecord"
SVN_EXPORT_COMMAND="svn+ssh://svnread@kelev.kaltura.com"
REMOTE_SVN_PATH="/usr/local/kalprod/flash/$component/"
REMOTE_GIT_PATH="https://github.com/kaltura/$component/archive/"
VERSION_DOWNLOAD_PATH="/tmp/"$component"_packing/kaltura-legacy-"$component/
VERSION="v1"

function clean_up () {
    echo -n "cleaning [$VERSION_DOWNLOAD_PATH] -> "
    rm -rf $VERSION_DOWNLOAD_PATH
    echo "done"
}


function svn_export() {
    for SVN_VERSION in $SVN_LEGACY_VERSIONS; 
    do 
        # svn export --force $SVN_EXPORT_COMMAND/$REMOTE_SVN_PATH/$SVN_VERSION $VERSION_DOWNLOAD_PATH/$SVN_VERSION
        svn export --force --quiet $SVN_EXPORT_COMMAND/$REMOTE_SVN_PATH/$SVN_VERSION $VERSION_DOWNLOAD_PATH/$SVN_VERSION
        if [ $? -ne 0 ]; then
            echo "There was a probblem exporting version $SVN_VERSION from SVN. Exiting."
            exit 1
        fi
    done
}

function git_zip_download() {
    for git_version in $GIT_LEGACY_VERSIONS;
    do
        wget $REMOTE_GIT_PATH/$git_version.zip -O $VERSION_DOWNLOAD_PATH/$git_version.zip
        if [ $? -ne 0 ]; then
            echo "There was a probblem exporting version $git_version from Github. Exiting."
            exit 1
        fi
        unzip -q "$VERSION_DOWNLOAD_PATH/$git_version.zip" -d "$VERSION_DOWNLOAD_PATH/"
        clean_git_version=`echo $git_version | awk -F'v' '{print $2}'`
        mv "$VERSION_DOWNLOAD_PATH/$component-$clean_git_version" "$VERSION_DOWNLOAD_PATH/$git_version"
        rm -f $VERSION_DOWNLOAD_PATH/$git_version.zip
    done
}

function zip_for_rpm_source() {
    pushd $VERSION_DOWNLOAD_PATH/../
    zip -qr $RPM_SOURCES_DIR/"kaltura-legacy-"$component"-$VERSION.zip" ./
    popd
}

function build_rpm() {
    if [ -x "`which rpmbuild 2>/dev/null`" ];then
        rpmbuild -ba $RPM_SPECS_DIR/$LEGACY_KRECORD_RPM_NAME.spec
    else
        echo "rpmbuild was not found on this machine. Exiting"
    fi
}

set -o nounset

clean_up
[ ! -d $VERSION_DOWNLOAD_PATH ] && mkdir $VERSION_DOWNLOAD_PATH
svn_export
git_zip_download
zip_for_rpm_source
echo "packed legacy_$component.zip at $RPM_SOURCES_DIR"
build_rpm
