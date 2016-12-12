%define prefix /opt/kaltura 
Summary: Kaltura Server release file and package configuration
Name: kaltura-live-analytics
Version: v0.5.26
Release: 3
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
Source7: %{name}_nginx.conf
Source8: https://raw.githubusercontent.com/kaltura/live_analytics/v0.5/setup/create_cassandra_tables.cql
Source9: %{name}_register_log.sh
Source10: %{name}_live_stats
Source11: %{name}_rotate_live_stats.template
Source12: %{name}_live-analytics-driver.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: dsc22 cassandra22 tomcat java-1.8.0-openjdk kaltura-nginx kaltura-spark

%description
Kaltura Server release file. This package contains yum 
configuration for the Kaltura RPM Repository, as well as the public
GPG keys used to sign them.




%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/data/geoip $RPM_BUILD_ROOT%{prefix}/bin $RPM_BUILD_ROOT%{prefix}/lib $RPM_BUILD_ROOT/usr/share/tomcat/lib $RPM_BUILD_ROOT/var/lib/tomcat/webapps/ $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cassandra $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cron $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/logrotate

tar zxf %{SOURCE0} -C $RPM_BUILD_ROOT%{prefix}/lib
unzip -o -q %{SOURCE6} -d $RPM_BUILD_ROOT
cp $RPM_BUILD_ROOT/jaxws-ri/lib/*jar $RPM_BUILD_ROOT/usr/share/tomcat/lib
rm -rf $RPM_BUILD_ROOT/jaxws-ri
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/lib/config.template.properties
cp %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/lib/log4j.properties
cp %{SOURCE3} $RPM_BUILD_ROOT/var/lib/tomcat/webapps/
cp %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT%{prefix}/lib
cp %{SOURCE8} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cassandra
chmod +x %{SOURCE9}
cp %{SOURCE9} $RPM_BUILD_ROOT%{prefix}/bin/kaltura_register_log.sh
cp %{SOURCE12} $RPM_BUILD_ROOT%{prefix}/bin/live-analytics-driver.sh
cp %{SOURCE10} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cron/live_stats
cp %{SOURCE11} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/logrotate/live_stats.template

%clean
%{__rm} -rf %{buildroot}

%post
for DAEMON in cassandra tomcat ;do
	service $DAEMON start
done

%files
%dir %{prefix}/data/geoip
%{prefix}/lib/*jar
%{prefix}/bin/*
%config %{prefix}/lib/config.template.properties
%config %{prefix}/lib/log4j.properties
%config %{prefix}/app/configurations/live_analytics/cassandra/*
%config %{prefix}/app/configurations/live_analytics/logrotate/*
%config %{prefix}/app/configurations/live_analytics/cron/*
/var/lib/tomcat/webapps/KalturaLiveAnalytics.war
/usr/share/tomcat/lib/*jar

%changelog
* Sat Dec 3 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.6.0-1
- First release
