%define prefix /opt/kaltura
%define widget_name kcw
#%define kcw_vers "v2.1.6.7 v2.1.5 v2.2.1 v2.2.3 v2.1.4 v2.1.6.7 v2.1.6.7 v1.5.4 v2.1.6.7 v2.1.2 v2.0.7 v2.1.6.3 v1.6.5 v1.6.5.24461"
%define kcw_vers "v1.5.4 v1.6.5 v1.6.5.24461 v2.0.7 v2.1.2 v2.1.4 v2.1.5 v2.1.6.3 v2.1.6.7 v2.2.1 v2.2.3"
Name:	kaltura-%{widget_name}
Version: 1.0.0 
Release: 1
Summary: Kaltura KCW - used for recording from web cam
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

This package installs the Kaltura KCW - used for recording from web cam.

%prep
%setup -qn %{name} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/%{widget_name}
for i in %{kcw_vers};do
	cp -r %{_builddir}/%{name}/$i $RPM_BUILD_ROOT/%{prefix}/web/flash/%{widget_name}
	find $RPM_BUILD_ROOT/%{prefix}/web/flash/%{widget_name} -name ".project" -exec rm {} \;
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/%{widget_name}


%changelog
* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- initial package.
