%define prefix /opt/kaltura
Name:	kaltura-kmcng
Version: v5.4.2
Release: 1
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

%preun

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/apps/kmcng/%{version}
%config %{prefix}/apps/kmcng/%{version}/deploy/*


%changelog
* Mon Oct 8 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v5.4.2-1
- content/category: fix "Move Category" panel height to support other languages (211ba28)
- content/entry: fix entry actions button width on Firefox (058bb95)
- help: add missing help links to settings/account information section (7b75185)
- hide OTT players from VOD Share & Embed players list (561d159)
- settings/account-info: fix form sending error (6affdc3)

* Mon Aug 27 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v5.3.2-1
- content/entries: adjust position of the Youtube icon on entry thumbnails (825d2f3)
- content/entry: disable entry download if user doesn't have the required permissions (872799b)
- upload: fix "Create from URL" upload button label (3439b78)
- upload: set entry name and format for entries created from URL (#798) (b7d3621)

* Fri Aug 10 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v5.2.1
- Custom Data - Some characters entered in custom text fields are displayed with their character reference and break-lines are ignored
- Entries - Scrolling down action isn't smooth in IE11, edge and Firefox

* Wed Jun 27 2018 jess.portnoy@kaltura.com <Jess Portnoy> - v4.5.1
- First release
