%define prefix /opt/kaltura
Name:	kaltura-kmcng
Version: v4.8.1
Release: 2
Summary: Kaltura HTML5 Management Console

Group: System Management	
License: AGPLv3+	
URL: https://github.com/kaltura/kmcng 
Source0: %{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: kaltura-base, httpd, kaltura-html5-studio,php-cli	

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

This package installs the KMC HTML5 web interface.

%prep
%setup -q -n %{name}-%{version} 

%build
%post

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/apps/kmcng
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT%{prefix}/apps/kmcng/%{version}
sed -i 's@useSecuredProtocol:!0@useSecuredProtocol:false@g' $RPM_BUILD_ROOT%{prefix}/apps/kmcng/%{version}/main.*.bundle.js

%preun

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/apps/kmcng/%{version}
%config %{prefix}/apps/kmcng/%{version}/deploy/*


%changelog
* Wed Jun 27 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v4.5.1
- First release
