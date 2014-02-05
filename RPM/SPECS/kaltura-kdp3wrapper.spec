%define prefix /opt/kaltura
Name:	kaltura-kdp3wrapper	
Version: v37.0 
Release: 3 
Summary: Kaltura KDP3 Wrapper
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

This package installs the KDP3 Wrapper.

%prep
%setup -qn %{name} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash
cp -r %{_builddir}/%{name} $RPM_BUILD_ROOT/%{prefix}/web/flash/kdp3wrapper

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/kdp3wrapper


%changelog
* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v37.0-3
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v37.0-1
- initial package.
