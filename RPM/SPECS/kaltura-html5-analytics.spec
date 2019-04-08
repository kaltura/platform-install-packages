%define prefix /opt/kaltura
%define analytics_prefix %{prefix}/apps/kmc-analytics

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5-analytics
Version: v0.2
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz 
URL: https://github.com/kaltura/analytics-front-end
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

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

This package installs the Kaltura HTML5 Analytics app.

%prep
%setup -q -n %{name}-%{version}



%install
mkdir -p $RPM_BUILD_ROOT%{analytics_prefix}
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT%{analytics_prefix}/%{version}

%clean
rm -rf %{buildroot}

%post


%postun

%files
%defattr(-, root, root, 0755)
%{analytics_prefix}/%{version}

%changelog
* Mon Apr 8 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v0.2-1
- Initial release
