FROM centos:6


RUN echo "NETWORKING=yes" > /etc/sysconfig/network


# JDK7
RUN yum -y install java-1.7.0-openjdk


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


# kaltura
RUN rpm -ihv http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
RUN yum install -y kaltura-server

ADD docker/install/* /root/install/
RUN chmod +x /root/install/install.sh

EXPOSE 80 443 1935


# start services
CMD ["/sbin/init"]
