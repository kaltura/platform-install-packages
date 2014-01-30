%define prefix /opt/kaltura

Summary: Kaltura Open Source Video Platform 
Name: kaltura-postinst 
Version: 1.0.2
Release: 21 
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz
Source1: post_inst_mail.template
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

This package includes post install scripts to be run post RPM install as they require user input.

%prep
%setup -qn postinst

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT/%{prefix}/app/configurations
chmod +x *.sh 
mv  *.sh *.rc $RPM_BUILD_ROOT/%{prefix}/bin
cp %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/app/configurations
sed -i 's#@APP_DIR@#%{prefix}/app#g' $RPM_BUILD_ROOT/%{prefix}/bin/*rc

%clean
rm -rf %{buildroot}

%post

%preun

%files
%{prefix}/bin/*
%config %{prefix}/bin/db_actions.rc
%config %{prefix}/app/configurations/*

%changelog
* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-8
- Modified post install mail template.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-7
- With post install mail template.
* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-8
- Now actually USE the templ to send it out.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-7
- With post install mail template.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-6
- Proper Analytics population msg.
- Change all server prompt defaults to 127.0.0.1.
- Changed inst complete msg.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-5
- bash -x on drop-db.sh

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-3
- Removed debug from front.
- Added DWH config to config-all.sh

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.2-1
- New minor release.

* Sat Jan 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-38
- Unsubscribe mail token now replaced
- Setting Apache on HTTP works
- Added port selection in front config
- Added export DB script
- Added %%prefix/bin/kaltura-drop-db.sh
- Added %%prefix/kaltura-mysql-settings.sh

* Sun Jan 19 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-15
- Version bounce. 

* Thu Jan 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-13
- Only run base-config if there's no lock indicating it already ran.

* Tue Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-12
- Additions to both base and db config scripts.

* Tue Jan 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-11
- Added DB config script and RC file.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-4
- Bounce.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-2
- Updated base config script.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- initial package. 
