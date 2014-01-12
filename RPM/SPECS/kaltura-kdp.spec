%define prefix /opt/kaltura
%define kdp_vers "v3.5.21 v3.8.9 v3.9.1 v3.9.2"
Name:	kaltura-kdp	
Version: 3.0.0 
Release: 1
Summary: Kaltura Dynamic Player
License: AGPLv3+	
URL: http://kaltura.org
Source0: %{name}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

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

This package installs the KDP Flash player.

%prep
%setup -qn %{name} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/kdp3
for i in %{kdp_vers};do
	cp -r %{_builddir}/%{name}/$i $RPM_BUILD_ROOT/%{prefix}/web/flash/kdp3/
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/kdp3


%changelog
* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 3.0.0-1
- initial package.
