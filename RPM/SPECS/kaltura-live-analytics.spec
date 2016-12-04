%define prefix /opt/kaltura 
Summary: Kaltura Server release file and package configuration
Name: kaltura-live-analytics
Version: v0.5.26
Release: 2
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
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: dsc22 cassandra22 spark-core spark-master spark-worker tomcat java-1.8.0-openjdk kaltura-nginx

%description
Kaltura Server release file. This package contains yum 
configuration for the Kaltura RPM Repository, as well as the public
GPG keys used to sign them.




%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/data/geoip $RPM_BUILD_ROOT%{prefix}/lib $RPM_BUILD_ROOT/usr/share/tomcat/lib $RPM_BUILD_ROOT/var/lib/tomcat/webapps/
tar zxf %{SOURCE0} -C $RPM_BUILD_ROOT%{prefix}/lib
unzip -o -q %{SOURCE6} -d $RPM_BUILD_ROOT
cp $RPM_BUILD_ROOT/jaxws-ri/lib/*jar $RPM_BUILD_ROOT/usr/share/tomcat/lib
rm -rf $RPM_BUILD_ROOT/jaxws-ri
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/lib/config.template.properties
cp %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/lib/log4j.properties
cp %{SOURCE3} $RPM_BUILD_ROOT/var/lib/tomcat/webapps/
cp %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT%{prefix}/lib

%clean
%{__rm} -rf %{buildroot}

%post
for DAEMON in cassandra spark-master spark-worker tomcat ;do
	service $DAEMON start
done

%files
%dir %{prefix}/data/geoip
%{prefix}/lib/*jar
%config %{prefix}/lib/config.template.properties
%config %{prefix}/lib/log4j.properties
/var/lib/tomcat/webapps/KalturaLiveAnalytics.war
/usr/share/tomcat/lib/*jar

%changelog
* Sat Dec 3 2016 jess.portnoy@kaltura.com <Jess Portnoy> - 12.6.0-1
- First release
