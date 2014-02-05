%define kmc_login_version v1.2.3
%define prefix /opt/kaltura
Name:	kaltura-kmc	
Version: v5.37.10
Release: 11 
Summary: Kaltura Management Console

Group: System Management	
License: AGPLv3+	
URL: http://kaltura.org
Source0: %{name}-%{version}.tar.bz2
Source1: kmc_config.ini
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

This package installs the KMC Flash web interface.

%prep
%setup -q 

%build
%post
if [ "$1" = 2 ];then
	php %{prefix}/app/deployment/uiconf/deploy_v2.php --ini=%{prefix}/web/flash/kmc/%{version}/config.ini >> %{prefix}/log/deploy_v2.log  2>&1
fi

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/login
mv %{_builddir}/%{name}-%{version}/login/%{kmc_login_version} $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/login/ 
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}
cp %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/config.ini


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/kmc
%config %{prefix}/web/flash/kmc/%{version}/config.ini


%changelog
* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.37.10-11
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-10
- Moving to KDP3 v3.9.7.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-9
- Added nab UI confs.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-7
- Added dep on kaltura-html5-studio

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-4
- Replace version in base.ini

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-2
- Added the login dir.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-1
- Ver bounce.

* Fri Jan 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.36.10-1
- initial package.
