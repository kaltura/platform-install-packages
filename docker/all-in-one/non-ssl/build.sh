#!/bin/bash

IMAGE=kaltura/server
VERSION=Kajam-11.8.0

# java
JDK_VERSION=jdk-7u71

if [ ! -e tmp ]; then
    mkdir tmp
fi

if [ ! -e tmp/jdk-linux-x64.tar.gz ]; then
	wget -c -O "tmp/jdk-linux-x64.tar.gz" --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/7u71-b14/$JDK_VERSION-linux-x64.tar.gz"
fi


# create link in build context
ln -s ../../utils/mysql_secure_installation.sh mysql_secure_installation.sh

# building
docker build -t $IMAGE:$VERSION .
docker tag -f $IMAGE:$VERSION $IMAGE:latest

# delete link
rm -f mysql_secure_installation.sh


#running
docker run -d --name=kaltura -p 80:80 kaltura/server


# installing 
docker exec -i -t kaltura /root/install/install.sh
