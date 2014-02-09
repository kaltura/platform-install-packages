%define prefix /opt/kaltura

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5lib
Version: v2.1.1
Release: 6 
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/kaltura/mwEmbed/tarball/%{name}-%{version}.tar.gz 
Source1: LocalSettings.php
URL: http://kaltura.org
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

This package installs the Kaltura HTML5 library.

%prep
%setup -q



%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/%{version}
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/web/html5/html5lib/%{version}

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-, root, root, 0755)
%doc COPYING README.markdown 
%{prefix}/web/html5/html5lib/%{version}
%config %{prefix}/web/html5/html5lib/%{version}/LocalSettings.KalturaPlatform.php

%changelog
* Sun Feb 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-6
- Fixed https://github.com/kaltura/platform-install-packages/issues/24

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-5
- LocalSettings.php is ALWAYS the same, it has no custom data, why not just bring it as part of the package??

* Wed Jan 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-3
- Moved root dir to %{prefix}/web.

* Tue Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-2
- Added %%doc.

* Tue Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v2.1.1-1
- initial package.
