%define prefix /opt/kaltura
Name:	kaltura-clipapp
Version: v1.0.7
Release: 1
Epoch: 1
Summary: Kaltura Clipper App 
License: AGPLv3+	
URL: http://kaltura.org
Source0: %{name}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: kaltura-base, httpd	
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

This package installs the Kaltura Clipper App, used for clipping segments from a video.

%prep
%setup -qn %{name} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/apps/clipapp
cp -r %{_builddir}/%{name}/%{version} $RPM_BUILD_ROOT/%{prefix}/apps/clipapp
cp %{_builddir}/%{name}/%{version}_saas/config.local.php $RPM_BUILD_ROOT/%{prefix}/apps/clipapp/%{version}/config.local.php

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/apps/clipapp


%changelog
* Tue Feb 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.0.7-1
- Need the cnfig.local.php from saas for this one to work.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- initial package.
