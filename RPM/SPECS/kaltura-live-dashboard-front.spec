%define base_prefix /opt/kaltura
%define app_prefix %{base_prefix}/apps/liveDashboard

Summary: Kaltura Live Dashboard
Name: kaltura-live-dashboard-front
Version: 1.1.1
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-v%{version}.tar.gz 
URL: https://github.com/kaltura/kmc-live-dashboard/archive/v%{version}.tar.gz 
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

This package installs the Kaltura Live Dashboard FrontEnd.

%prep
%setup -q -n kmc-live-dashboard-%{version}



%install
mkdir -p $RPM_BUILD_ROOT%{app_prefix}/v%{version}
cp -r %{_builddir}/kmc-live-dashboard-%{version}/* $RPM_BUILD_ROOT%{app_prefix}/v%{version}/

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-, root, root, 0755)
%{app_prefix}/v%{version}

%changelog
* Mon Nov 13 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 1.1.1-1
- First release
