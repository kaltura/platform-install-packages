#!/bin/bash -e 
#===============================================================================
#          FILE: prerequisites.centos.6.6.sh
#         USAGE: ./prerequisites.centos.6.6.sh 
#   DESCRIPTION: Install all prerequisites for CentOS 6.6
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/25/14
#      REVISION:  ---
#===============================================================================

sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
sudo rpm -Uvh http://dl.atrpms.net/el6-x86_64/atrpms/stable/atrpms-repo-6-7.el6.x86_64.rpm
sudo rpm -Uvh http://apt.sw.be/redhat/el6/en/x86_64/rpmforge/RPMS/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm

# red5 - java
JDK_VERSION=jdk-7u71
wget -c -O "$JDK_VERSION-linux-x64.tar.gz" --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/7u71-b14/$JDK_VERSION-linux-x64.tar.gz"
tar zxf $JDK_VERSION-linux-x64.tar.gz
rm -f $JDK_VERSION-linux-x64.tar.gz
JDK_VERSION=1.7.0_71
sudo mv jdk$JDK_VERSION /opt/
sudo chown -R root.root /opt/jdk$JDK_VERSION
sudo rm -f /usr/bin/java /usr/bin/javac /usr/bin/javah /usr/bin/javap /usr/bin/javadoc
sudo ln -s /opt/jdk$JDK_VERSION/bin/java /usr/bin/java
sudo ln -s /opt/jdk$JDK_VERSION/bin/javac /usr/bin/javac
sudo ln -s /opt/jdk$JDK_VERSION/bin/javah /usr/bin/javah
sudo ln -s /opt/jdk$JDK_VERSION/bin/javap /usr/bin/javap
sudo ln -s /opt/jdk$JDK_VERSION/bin/javadoc /usr/bin/javadoc
JAVA_HOME=/opt/jdk$JDK_VERSION
export JAVA_HOME

# red5 - maven
wget http://apache.mivzakim.net/maven/maven-3/3.2.5/binaries/apache-maven-3.2.5-bin.tar.gz
tar zxf apache-maven-3.2.5-bin.tar.gz
rm -f apache-maven-3.2.5-bin.tar.gz
sudo mv apache-maven-3.2.5 /opt/
sudo chown -R root.root /opt/apache-maven-3.2.5
sudo ln -s /opt/apache-maven-3.2.5/bin/mvn /usr/bin/mvn

# PECL
sudo yum install -y php-devel php-pear libxml2-devel cyrus-sasl-devel flex bison python-sphinx memcached systemtap-sdt-devel libevent-devel libssh2-devel

# x264
sudo yum install -y nasm yasm

# lame
sudo yum install -y gtk2-devel libvorbis-devel ncurses-devel
QA_RPATHS=0x0002
export QA_RPATHS

# faac
sudo yum install -y libmp4v2-devel dos2unix

# ffmpeg
sudo yum install -y SDL-devel imlib2-devel schroedinger-devel libtheora-devel xvidcore-devel openjpeg-devel librtmp-devel texi2html yasm-devel gsm-devel speex-devel libvpx-devel faac faac-devel libass-devel

# sphinx
sudo yum install -y mysql-devel expat-devel



