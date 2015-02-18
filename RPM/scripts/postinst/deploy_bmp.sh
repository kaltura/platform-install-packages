#!/bin/sh
if [ -r /etc/kaltura.d/system.ini ];then
        . /etc/kaltura.d/system.ini
else
        echo "I need this file to get some information. Is Kaltura installed here?"
        exit 1;
fi
JAVA_VER=1.7.0
ACTIVITI_VER=5.17.0
MYSQL_JAVA_CONNECTOR_VER=5.0.8
XERCES_VER=2.8.1
rpm -ihv http://mirrors.coreix.net/fedora-epel/6/x86_64/epel-release-6-8.noarch.rpm
yum install -y ant tomcat java-$JAVA_VER-openjdk-devel
if [ -z "$CATALINA_HOME" ];then
        echo "Input path to CATALINA_HOME:"
        read -e CATALINA_HOME
fi
if [ -z "$JAVA_HOME" ];then
        echo "Input path to JAVA_HOME:"
        read -e JAVA_HOME
fi
echo "
CATALINA_HOME=$CATALINA_HOME
JAVA_HOME=$JAVA_HOME" >> /etc/kaltura.d/system.ini

if ! grep -q Integration $APP_DIR/configurations/plugins.ini;then
	echo "Integration" >> $APP_DIR/configurations/plugins.ini
fi

if ! grep -q ExampleIntegration $APP_DIR/configurations/plugins.ini;then
	echo "ExampleIntegration" >> $APP_DIR/configurations/plugins.ini
fi
if ! grep -q IntegrationEventNotifications $APP_DIR/configurations/plugins.ini;then
	echo "IntegrationEventNotifications" >> $APP_DIR/configurations/plugins.ini
fi
if ! grep -q BpmEventNotificationIntegration $APP_DIR/configurations/plugins.ini;then
	echo "BpmEventNotificationIntegration" >> $APP_DIR/configurations/plugins.ini
fi
if ! grep -q ActivitiBusinessProcessNotification $APP_DIR/configurations/plugins.ini;then
	echo "BpmEventNotificationIntegration" >> $APP_DIR/configurations/plugins.ini
fi
set -e
rm -rf $APP_DIR/cache/*
php $APP_DIR/deployment/base/scripts/installPlugins.php 
service httpd reload
#we basically only need pojo,bpmn,testsClient but there is some bug with testsClient not being generated explicitely so lets generate all
php $APP_DIR/generator/generate.php 
# gen additional needed clients
php /opt/kaltura/app/generator/generate.php pojo,bpmn

rm -rf $APP_DIR/cache/*
#vi $APP_DIR/configurations/batch/batch.ini
echo "[KAsyncIntegrate : JobHandlerWorker]
id                                                                                                      = 570
friendlyName                                                                            = Integrate
type                                                                                            = KAsyncIntegrate
maximumExecutionTime                                                            = 12000
scriptPath                                                                                      = ../plugins/integration/batch/Integrate/KAsyncIntegrateExe.php

[KAsyncIntegrateCloser : JobHandlerWorker]
id                                                                                                      = 580
friendlyName                                                                            = Integrate Closer
type                                                                                            = KAsyncIntegrateCloser
maximumExecutionTime                                                            = 12000
scriptPath                                                                                      = ../plugins/integration/batch/Integrate/KAsyncIntegrateCloserExe.php
params.maxTimeBeforeFail                                                        = 1000000
" >> $APP_DIR/configurations/batch/batch.ini
/etc/init.d/kaltura-batch restart
service httpd reload
mysql -u$DB1_USER -p$DB1_PASS $DB1_NAME <  $APP_DIR/deployment/updates/sql/2014_11_20_business_process_server.sql
cd $APP_DIR
php deployment/updates/scripts/add_permissions/2014_11_20_business_process_server_permissions.php
php deployment/updates/scripts/add_permissions/2015_01_20_dispatch_integration_job.php
php tests/standAloneClient/exec.php tests/standAloneClient/bpmNotificationsTemplates.xml
rm -rf $APP_DIR/cache/*
cd /tmp/
wget https://github.com/Activiti/Activiti/releases/download/activiti-$ACTIVITI_VER/activiti-$ACTIVITI_VER.zip -Oactiviti-$ACTIVITI_VER/activiti-$ACTIVITI_VER.zip
unzip -oq activiti-$ACTIVITI_VER.zip 
cp -r activiti-$ACTIVITI_VER/wars/* $CATALINA_HOME/webapps/
wget http://cdn.mysql.com/Downloads/Connector-J/mysql-connector-java-$MYSQL_JAVA_CONNECTOR_VER.zip -Omysql-connector-java-$MYSQL_JAVA_CONNECTOR_VER.zip
unzip -oq mysql-connector-java-$MYSQL_JAVA_CONNECTOR_VER.zip 
cp mysql-connector-java-$MYSQL_JAVA_CONNECTOR_VER/mysql-connector-java-$MYSQL_JAVA_CONNECTOR_VER-bin.jar $CATALINA_HOME/lib/
wget http://central.maven.org/maven2/xerces/xercesImpl/$XERCES_VER/xercesImpl-$XERCES_VER.jar -OxercesImpl-$XERCES_VER.jar
unzip xercesImpl-$XERCES_VER.jar -d/opt/kaltura/web/content/clientlibs/bpmn/deploy/src
/etc/init.d/tomcat restart
mv $CATALINA_HOME/webapps/activiti-rest/WEB-INF/classes/db.properties{,.orig}
mv $CATALINA_HOME/webapps/activiti-explorer/WEB-INF/classes/db.properties{,.orig}
echo "jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://$DB1_HOST:$DB1_PORT/activiti
jdbc.username=$DB1_USER
jdbc.password=$DB1_PASS" >> $CATALINA_HOME/webapps/activiti-rest/WEB-INF/classes/db.properties
echo "jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://$DB1_HOST:$DB1_PORT/activiti
jdbc.username=$DB1_USER
jdbc.password=$DB1_PASS" >> $CATALINA_HOME/webapps/activiti-explorer/WEB-INF/classes/db.properties
# Allow tomcat to start listeners 
sleep 10
curl  -I -v http://127.0.0.1:8080/activiti-explorer/
echo "CREATE DATABASE activiti;
GRANT ALL ON activiti.* TO '$DB1_USER'@'%';
FLUSH PRIVILEGES;" | mysql -uroot -p$SUPER_USER_PASSWD 
cp $WEB_DIR/content/clientlibs/bpmn/deploy/src/activiti.cfg.template.xml $WEB_DIR/content/clientlibs/bpmn/deploy/src/activiti.cfg.xml 
sed -i -e "s#@DB1_HOST@#$DB1_HOST#g" -e "s#@DB1_PORT@#$DB1_PORT#g" -e "s#@DB1_USER@#$DB1_USER#g" -e "s#@DB1_PASS@#$DB1_PASS#g" $WEB_DIR/content/clientlibs/bpmn/deploy/src/activiti.cfg.xml
cd $WEB_DIR/content/clientlibs/bpmn
ant
php $APP_DIR/tests/standAloneClient/exec.php $APP_DIR/tests/standAloneClient/activitiServer.xml
