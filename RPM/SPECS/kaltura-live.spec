%define wowza_version 4.3.0
%define wowza_prefix /usr/local/WowzaStreamingEngine-%{wowza_version}
%define media_server_version 4.5.10.72
%define kaltura_prefix /opt/kaltura
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
%define kaltura_user	kaltura
%define kaltura_group	kaltura

Summary: Kaltura Open Source Video Platform - Live Streaming Server  
Name: kaltura-live
Version: 12.14.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: java-1.8.0-openjdk,ant, kaltura-monit, kaltura-base, redhat-lsb-core
# ant-trax
BuildArch: noarch
BuildRequires: unzip
#Source0: WowzaStreamingEngine-%{wowza_version}-linux-x64-installer.run
Source1: https://github.com/kaltura/media-server/releases/download/rel-%{media_server_version}/KalturaWowzaServer-install-%{media_server_version}.zip
Source2: WowzaStreamingEngine.service
Source3: WowzaStreamingEngineManager.service
#Source4: build.xml
#Source5: configure.xsl
#Source6: hdfvr.xml
Source7: oflaDemo.xml
Source8: wowza.rc
Source9: junit-dep-4.7.jar 
Source10: json-20090211.jar
Source11: hamcrest-core-1.1.jar
Source12: commons-logging-1.0.4.jar
Source13: commons-httpclient-3.1.jar
Source14: commons-codec-1.4.jar


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

This package sets up a Kaltura Live Streaming server including technology from Wowza.

%clean
rm -rf %{buildroot}

%install
mkdir -p $RPM_BUILD_ROOT%{kaltura_prefix}/var/tmp $RPM_BUILD_ROOT%{kaltura_prefix}/var/live/dvr $RPM_BUILD_ROOT%{wowza_prefix}/conf/oflaDemo $RPM_BUILD_ROOT%{wowza_prefix}/applications/oflaDemo $RPM_BUILD_ROOT%{wowza_prefix}/transcoder/templates $RPM_BUILD_ROOT%{kaltura_prefix}/app/configurations/monit/monit.avail
unzip -o %{SOURCE1} -d $RPM_BUILD_ROOT%{kaltura_prefix}/var/tmp
mv $RPM_BUILD_ROOT%{kaltura_prefix}/var/tmp/lib $RPM_BUILD_ROOT%{wowza_prefix}/
%{__install} -m644  %{SOURCE9} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} $RPM_BUILD_ROOT%{wowza_prefix}/lib
#mv  $RPM_BUILD_ROOT%{kaltura_prefix}/var/tmp/build.xml $RPM_BUILD_ROOT%{wowza_prefix}/
#mv  $RPM_BUILD_ROOT%{kaltura_prefix}/var/tmp/configure.xsl $RPM_BUILD_ROOT%{wowza_prefix}/
rm -rf $RPM_BUILD_ROOT%{kaltura_prefix}/var/tmp
#cp %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT%{wowza_prefix}/
#cp %{SOURCE6} $RPM_BUILD_ROOT%{wowza_prefix}/transcoder/templates/
cp %{SOURCE7} $RPM_BUILD_ROOT%{wowza_prefix}/conf/oflaDemo/Application.xml
cp %{SOURCE8} $RPM_BUILD_ROOT%{kaltura_prefix}/app/configurations/monit/monit.avail

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/WowzaStreamingEngine.service
%{__install} -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/WowzaStreamingEngineManager.service
%endif


%pre
# maybe one day we will support SELinux in which case this can be ommitted.
if which getenforce >> /dev/null 2>&1; then
	
	if [ `getenforce` = 'Enforcing' ];then
		echo "You have SELinux enabled, please change to permissive mode with:
# setenforce permissive
and then edit /etc/selinux/config to make the change permanent."
		exit 1;
	fi
fi
# create user/group, and update permissions
getent group %{kaltura_group} >/dev/null || groupadd -r %{kaltura_group} -g7373 2>/dev/null
getent passwd %{kaltura_user} >/dev/null || useradd -m -r -u7373 -d %{prefix} -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null

usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
%post

%preun

%postun

%files
%{wowza_prefix}
%config %{wowza_prefix}/conf/oflaDemo/Application.xml
#%config %{wowza_prefix}/transcoder/templates/hdfvr.xml
#%config %{wowza_prefix}/configure.xsl
#%config %{wowza_prefix}/build.xml
%config %{kaltura_prefix}/app/configurations/monit/monit.avail/wowza.rc
%defattr(-, %{kaltura_user}, %{kaltura_group} , 0775)
%dir %{kaltura_prefix}/var/live/dvr

%if %{use_systemd}
%{_unitdir}/WowzaStreamingEngine.service
%{_unitdir}/WowzaStreamingEngineManager.service
%endif


%changelog
* Tue Nov 29 2016 Jess Portnoy <jess.portnoy@kaltura.com> - 12.6.0-1 
- First package.

