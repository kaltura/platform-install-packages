%define base_prefix /opt/kaltura
%define app_prefix %{base_prefix}/apps/liveanalytics/

Summary: Kaltura Live Analytics Front End
Name: kaltura-live-analytics-front
Version: v2.7.3
Release: 1
License: AGPLv3+
Group: Server/Platform 
#Source0: %{name}-%{version}.tar.bz2 
Source0: %{name}-%{version}.zip 
URL: https://github.com/kaltura/live-analytics-front-end/releases/download/%{version}/%{version}.zip 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: kaltura-base

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

This package installs the Kaltura Live Analytics Front End.

%prep
%setup -q -n %{version}



%install
mkdir -p $RPM_BUILD_ROOT%{app_prefix}
cp -r %{_builddir}/%{version} $RPM_BUILD_ROOT%{app_prefix}/%{version}

%clean
rm -rf %{buildroot}

%post
php %{base_prefix}/app/deployment/uiconf/deploy_v2.php --ini=%{app_prefix}/%{version}/deploy/config.ini

%postun

%files
%defattr(-, root, root, 0755)
%{app_prefix}/%{version}
%config %{app_prefix}/%{version}/deploy/config.ini

%changelog
* Fri Dec 2 2016 Jess Portnoy <jess.portnoy@kaltura.com> - v2.6-1
- First release
