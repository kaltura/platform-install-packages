FROM centos:6


RUN echo "NETWORKING=yes" > /etc/sysconfig/network
#RUN sed -i s/^SELINUX=enforcing/SELINUX=permissive/g /etc/selinux/config

# wget
RUN yum -y install wget


# JDK7
ADD tmp/jdk-linux-x64.tar.gz /opt
WORKDIR /opt/jdk1.7.0_71
RUN alternatives --install /usr/bin/java java /opt/jdk1.7.0_71/bin/java 1
RUN alternatives --install /usr/bin/jar jar /opt/jdk1.7.0_71/bin/jar 1
RUN alternatives --install /usr/bin/javac javac /opt/jdk1.7.0_71/bin/javac 1
RUN echo "JAVA_HOME=/opt/jdk1.7.0_71" >> /etc/environment


# apache
RUN yum -y install httpd
RUN /sbin/chkconfig httpd on


# mysql
RUN yum install -y mysql mysql-server
RUN mysql_install_db
RUN chkconfig mysqld on
RUN service mysqld start


# facilities
RUN yum install -y postfix memcached ntp
RUN chkconfig postfix on
RUN chkconfig memcached on
RUN chkconfig ntpd on
RUN service postfix start
RUN service memcached start
RUN service ntpd start



# php
RUN yum install -y php php-mysql php-gd php-pecl-memcache php-pspell php-snmp php-xmlrpc php-xml


# enabling the EPEL repo
RUN rpm -ihv http://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm


# kaltura
RUN rpm -ihv http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
RUN yum install -y kaltura-server

ADD install/* /root/install/
RUN chmod +x /root/install/install.sh

EXPOSE 80 443 1935 3306

# start services
CMD ["/sbin/init"]
