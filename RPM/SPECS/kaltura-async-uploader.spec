%define prefix /opt/kaltura
%define kaltura_user kaltura
%define kaltura_rootdir %{_topdir}/../
%define postinst_dir %{_topdir}/scripts/postinst

Name:           kaltura-async-uploader
Version:         1.0
Release:        1%{?dist}
Summary:       Kaltura Open Source Video Platform - Media Server 
Group:          Server/Platform 
License:        AGPLv3+
URL:            https://github.com/kaltura/media-server-async-process
Source0:        https://github.com/kaltura/media-server-async-process/releases/download/rel-%{version}/AsyncMediaServerProcessClientApp-%{version}.zip
#Source1: %{postinst_dir}/%{name}-config.sh
#Source2: %{postinst_dir}/%{name}-config.sh
Source3:  kaltura_media_server_async_process.sh

BuildArch: 	noarch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:       php php-common php-mcrypt kaltura-media-server cronie ant >= 1.8.2 

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

The Kaltura platform enables video management, publishing, syndication and monetization, 
as well as providing a robust framework for managing rich-media applications, 
and developing a variety of online workflows for video. 

This package configures the AsyncMediaServerProcessClientApp component used in ECDN installation of Media Server. 

%prep
#%setup

%install

mkdir -p $RPM_BUILD_ROOT/%{prefix}/AsyncMediaServerProcessClientApp
unzip -d $RPM_BUILD_ROOT/%{prefix}/AsyncMediaServerProcessClientApp %{SOURCE0}
mkdir -p $RPM_BUILD_ROOT/%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT/etc/profile.d/
%{__install}  %{postinst_dir}/kaltura-async-uploader-config.sh   $RPM_BUILD_ROOT/%{prefix}/bin/
%{__install}  %{SOURCE3}   $RPM_BUILD_ROOT/%{prefix}/bin/


%clean
rm -rf %{buildroot}


%files
%dir %{prefix}/AsyncMediaServerProcessClientApp
%{prefix}/AsyncMediaServerProcessClientApp/*
%{prefix}/bin
%config %{prefix}/bin/kaltura_media_server_async_process.sh
%{prefix}/bin/*


%post

echo "
#####################################################################################################################################
Installation of %{name} %{version} completed
Please run 
# /opt/kaltura/bin/config_ecdn.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"

chmod +x %{prefix}/bin/kss_configure_firewall.sh

%changelog
* Mon Mar 9 2015 Igor Shevach <igor.shevach@kaltura.com> -  PLAT-2494
	 Initial release.
