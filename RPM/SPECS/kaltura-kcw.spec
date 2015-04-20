%define prefix /opt/kaltura
%define widget_name kcw
Name:	kaltura-%{widget_name}
Version: 2.2.4 
Release: 1 
Summary: Kalture Contribution Wizard 
License: AGPLv3+	
URL: http://kaltura.org
Source0: %{name}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: kaltura-base, httpd	

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

This package installs the Kaltura Contribution Wizard.

%prep
%setup -qn %{name} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/%{widget_name}
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content
mkdir -p $RPM_BUILD_ROOT/%{prefix}/web/content/uiconf/kaltura/generic
mv %{_builddir}/%{name}/uiconf/kaltura/generic/kcw_%{kcw_uiconf_ver} $RPM_BUILD_ROOT/%{prefix}/web/content/uiconf/kaltura/generic/kcw_%{kcw_uiconf_ver}
cp -r %{_builddir}/%{name}/v%{version} $RPM_BUILD_ROOT/%{prefix}/web/flash/%{widget_name}
find $RPM_BUILD_ROOT/%{prefix}/web/flash/%{widget_name} -name ".project" -exec rm {} \;


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/%{widget_name}
%{prefix}/web/content/uiconf/kaltura/generic/kcw_%{kcw_uiconf_ver}

%changelog
* Mon Apr 20 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 2.2.4
- We don't need more than one KCW version. Bundle only latest.

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-6
- Placing uiconfs in the right location.

* Mon Feb 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-4
- We also seem to need ver 2.2.4..

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-3
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Wed Jan 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-2
- Added uiconfs.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- initial package.
