%define prefix /opt/kaltura 
Summary: Kaltura Live Analytics
Name: kaltura-live-analytics
Version: v0.5.35
Release: 4
License: AGPLv3+
Group: Server/Platform 
URL: http://kaltura.org
Source0: register-file-deps-jars.tar.gz
Source1: %{name}_config.template.properties 
Source2: %{name}_log4j.properties
Source3: https://github.com/kaltura/live_analytics/releases/download/%{version}/KalturaLiveAnalytics.war
Source4: https://github.com/kaltura/live_analytics/releases/download/%{version}/live-analytics-driver.jar
Source5: https://github.com/kaltura/live_analytics/releases/download/%{version}/register-file.jar
Source6: http://repo.maven.apache.org/maven2/com/sun/xml/ws/jaxws-ri/2.2.10/jaxws-ri-2.2.10.zip
Source7: %{name}_nginx_live.template.conf
Source8: https://github.com/kaltura/live_analytics/raw/%{version}/setup/create_cassandra_tables.cql
Source9: %{name}_register_log.sh
Source10: %{name}_live_stats
Source11: %{name}_rotate_live_stats.template
Source12: %{name}_live-analytics-driver.sh
Source13: %{name}_live-analytics-driver.service
Source14: %{name}_cassandra.service
Source15: %{name}_rotate_live-analytics-driver

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: dsc22 cassandra22 tomcat java-1.8.0-openjdk  kaltura-spark

%description
Kaltura is the world's first Open Source Online Video Platform, transforming the way people work, 
learn, and entertain using online video. 
The Kaltura platform empowers media applications with advanced video management, publishing, 
and monetization tools that increase their reach and monetization and simplify their video operations. 
Kaltura improves productivity and interaction among millions of employees by providing enterprises 
powerful online video tools for boosting internal knowledge sharing, training, and collaboration, 
and for more effective marketing. Kaltura offers next generation learning for millions of students and 
teachers by providing educational institutions disruptive online video solutions for improved teaching,
learning, and increased engagement across campuses and beyond. 
For more information visit: http://corp.kaltura.com, http://www.kaltura.org and http://www.html5video.org.

This package installs and configures the Kaltura Live Analytics backend.

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/data/geoip $RPM_BUILD_ROOT%{prefix}/bin $RPM_BUILD_ROOT%{prefix}/lib $RPM_BUILD_ROOT/usr/share/tomcat/lib $RPM_BUILD_ROOT/var/lib/tomcat/webapps/ $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cassandra $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cron $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/logrotate $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/nginx $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/driver $RPM_BUILD_ROOT%{prefix}/log/nginx $RPM_BUILD_ROOT%{prefix}/var/run/live-analytics-driver

tar zxf %{SOURCE0} -C $RPM_BUILD_ROOT%{prefix}/lib
unzip -o -q %{SOURCE6} -d $RPM_BUILD_ROOT
cp $RPM_BUILD_ROOT/jaxws-ri/lib/*jar $RPM_BUILD_ROOT/usr/share/tomcat/lib
rm -rf $RPM_BUILD_ROOT/jaxws-ri
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/config.template.properties
cp %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/lib/log4j.properties
cp %{SOURCE3} $RPM_BUILD_ROOT/var/lib/tomcat/webapps/
cp %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT%{prefix}/lib
cp %{SOURCE8} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cassandra
chmod +x %{SOURCE12} %{SOURCE9}
cp %{SOURCE9} $RPM_BUILD_ROOT%{prefix}/bin/kaltura_register_log.sh
cp %{SOURCE12} $RPM_BUILD_ROOT%{prefix}/bin/live-analytics-driver.sh
cp %{SOURCE10} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cron/live_stats
cp %{SOURCE11} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/logrotate/live_stats.template
cp %{SOURCE15} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/logrotate/live-analytics-driver
cp %{SOURCE7} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/nginx/live.template.conf
cp %{SOURCE13} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/driver/live-analytics-driver.service
cp %{SOURCE14} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/driver/cassandra.service

%clean
%{__rm} -rf %{buildroot}

%post
for DAEMON in cassandra tomcat ;do
	service $DAEMON restart
done
if [ -d /usr/lib/systemd/system ];then
	# symlink does not work, see https://github.com/systemd/systemd/issues/2298
	cp %{prefix}/app/configurations/live_analytics/driver/live-analytics-driver.service /usr/lib/systemd/system
	cp %{prefix}/app/configurations/live_analytics/driver/cassandra.service /usr/lib/systemd/system
    	/usr/bin/systemctl preset cassandra.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl enable cassandra.service
    	/usr/bin/systemctl preset live-analytics-driver.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl enable live-analytics-driver.service
	systemctl daemon-reload
	service cassandra start
else
	ln -sf %{prefix}/bin/live-analytics-driver.sh /etc/init.d/live-analytics-driver
	chkconfig  --add live-analytics-driver 
	chkconfig live-analytics-driver on
	chkconfig  --add cassandra 
	chkconfig cassandra on
fi
if [ "$1" = 2 ];then
	service live-analytics-driver restart
fi
ln -sf %{prefix}/app/configurations/live_analytics/logrotate/live-analytics-driver /etc/logrotate.d/

%preun
if [ "$1" = 0 ] ; then
	service live-analytics-driver stop
	for FILE in /usr/lib/systemd/system/live-analytics-driver.service /etc/init.d/live-analytics-driver /etc/cron.d/kaltura_live_stats /etc/logrotate.d/kaltura_live_stats /etc/logrotate.d/live-analytics-driver /etc/nginx/conf.d/live.conf ;do
		if [ -r $FILE ];then
			rm $FILE
		fi
	done
	service nginx reload
fi


%files
%dir %{prefix}/data/geoip
%dir %{prefix}/log/nginx
%dir %{prefix}/var/run/live-analytics-driver
%{prefix}/lib/*jar
%{prefix}/bin/*
%config %{prefix}/lib/log4j.properties
%config %{prefix}/app/configurations/live_analytics/config.template.properties
%config %{prefix}/app/configurations/live_analytics/cassandra/*
%config %{prefix}/app/configurations/live_analytics/logrotate/*
%config %{prefix}/app/configurations/live_analytics/cron/*
%config %{prefix}/app/configurations/live_analytics/nginx/*
%config %{prefix}/app/configurations/live_analytics/driver/*
/var/lib/tomcat/webapps/KalturaLiveAnalytics.war
/usr/share/tomcat/lib/*jar

%changelog
* Thu Mar 16 2017 jess.portnoy@kaltura.com <Jess Portnoy> - v0.5.35-4
- Adjusted logrotation for live-analytics-driver.log
- Added log4j directives for live-analytics-driver.log

* Thu Mar 16 2017 jess.portnoy@kaltura.com <Jess Portnoy> - v0.5.35-3
- Added logrotate config for live-analytics-driver.log

* Sun Jan 15 2017 jess.portnoy@kaltura.com <Jess Portnoy> - v0.5.35-1
- https://github.com/kaltura/live_analytics/pull/26

* Wed Jan 11 2017 jess.portnoy@kaltura.com <Jess Portnoy> - v0.5.34-1
- https://github.com/kaltura/live_analytics/pull/25

* Sat Dec 3 2016 jess.portnoy@kaltura.com <Jess Portnoy> - v0.5.26-1
- First release
