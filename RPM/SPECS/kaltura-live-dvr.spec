%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
%define kaltura_root_prefix	/opt/kaltura
%define livedvr_prefix %{kaltura_root_prefix}/livedvr
%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define ffmpeg_version 3.0
%define nginx_conf_dir /etc/nginx/conf.d/

Summary: Kaltura Open Source Video Platform - Live DVR
Name: kaltura-livedvr
Version: 1.20.2
Release: 1
License: AGPLv3+
Group: Server/Platform 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-monit kaltura-base redhat-lsb-core nodejs >= 6.0.0 kaltura-nginx nodejs-chunked-stream nodejs-commander  nodejs-bundle-log4js nodejs-bundle-glob nodejs-bundle-mkdirp nodejs-q nodejs-bundle-q-io nodejs-bundle-touch nodejs-underscore nodejs-bundle-v8-profiler nodejs-nconf 
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
BuildRequires: unzip
Source0: %{name}-%{version}.tar.gz


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

This package sets up a Kaltura LiveDvr.

%clean
rm -rf %{buildroot}

%prep
%setup -qn liveDVR-%{version}

%build
NODE_PATH=~/node_modules
mkdir -p %{buildroot}/%{name}-%{version}/tmp/build 
./build_scripts/build_ffmpeg.sh %{buildroot}/%{name}-%{version}/tmp/build %{ffmpeg_version}
./build_scripts/build_ts2mp4_convertor.sh ./liveRecorder %{buildroot}/%{name}-%{version}/tmp/build/ffmpeg-%{ffmpeg_version} 
npm install nan
./build_scripts/build_addon.sh `pwd` %{buildroot}/%{name}-%{version}/tmp/build/ffmpeg-%{ffmpeg_version} Release


%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT%{livedvr_prefix}/bin $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/bin $RPM_BUILD_ROOT%{livedvr_prefix}/common/config/ $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/Config $RPM_BUILD_ROOT%{livedvr_prefix}/log $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/recordings/newSession $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/recordings/append $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/error $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/incoming $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/recordings $RPM_BUILD_ROOT%{nginx_conf_dir}
cp %{_builddir}/liveDVR-%{version}/liveRecorder/bin/ts_to_mp4_convertor $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/bin/ts_to_mp4_convertor
cp %{_builddir}/liveDVR-%{version}/node_addons/FormatConverter/build/Release/FormatConverter.so $RPM_BUILD_ROOT%{livedvr_prefix}/bin/FormatConverter.node
strip $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/bin/ts_to_mp4_convertor
strip $RPM_BUILD_ROOT%{livedvr_prefix}/bin/FormatConverter.node
cp %{_builddir}/liveDVR-%{version}/common/config/configMapping.json.template $RPM_BUILD_ROOT%{livedvr_prefix}/common/config
cp %{_builddir}/liveDVR-%{version}/liveRecorder/Config/configMapping.ini.template $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/Config
cp %{_builddir}/liveDVR-%{version}/serviceWrappers/linux/kLiveController $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/%{name} 
cp %{_builddir}/liveDVR-%{version}/liveRecorder/serviceWrappers/linux/liveRecorder $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/kaltura-live-recorder 
sed 's#@CONTENT_DIR@#%{kaltura_root_prefix}/web#g' %{_builddir}/liveDVR-%{version}/packager/config/nginx.conf.live.bootstrap.template > $RPM_BUILD_ROOT%{nginx_conf_dir}/nginx.conf.live.bootstrap
cp %{_builddir}/liveDVR-%{version}/packager/config/nginx.conf.live.conf.template $RPM_BUILD_ROOT%{nginx_conf_dir}/live.conf
cp %{_builddir}/liveDVR-%{version}/packager/config/nginx.conf.live.protocols.template $RPM_BUILD_ROOT%{nginx_conf_dir}/


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
if [ "$1" = 1 ];then
	/sbin/chkconfig --add %{name}
	/sbin/chkconfig %{name} on
	/sbin/chkconfig --add kaltura-live-recorder
	/sbin/chkconfig kaltura-live-recorder on
fi
%preun
if [ "$1" = 0 ] ; then
	/sbin/chkconfig --del %{name}
	service %{name} stop
	/sbin/chkconfig --del kaltura-live-recorder
	service kaltura-live-recorder stop
fi
%postun

%files
%defattr(-, %{kaltura_user}, %{kaltura_group} , 0775)
%dir %{livedvr_prefix}
%{livedvr_prefix}
%{kaltura_root_prefix}/web/content/kLive/liveRecorder/*
%config %{livedvr_prefix}/common/config/*
%config %{livedvr_prefix}/liveRecorder/Config/*
%config %{nginx_conf_dir}/*
%{_sysconfdir}/init.d/%{name}
%{_sysconfdir}/init.d/kaltura-live-recorder


%changelog
* Thu Oct 26 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 1.20.2-1
- PLAT-8051: Recording, jobs in processing queue of UploadTask, are not handled (https://github.com/kaltura/liveDVR/pull/534)
- Replace number with explicit kalturaLiveStatus

* Fri Mar 31 2016 Jess Portnoy <jess.portnoy@kaltura.com> - 1.9.2-1
- First package.

