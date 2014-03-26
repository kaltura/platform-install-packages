%define kmc_login_version v1.2.3
%define prefix /opt/kaltura
Name:	kaltura-kmc	
Version: v5.37.14
Release: 2 
Summary: Kaltura Management Console

Group: System Management	
License: AGPLv3+	
URL: http://kaltura.org
Source0: %{name}-%{version}.tar.bz2
Source1: kmc_config.ini
Source2: kmc_doc.zip
Source3: KMC_User_Manual.pdf
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
unzip %{SOURCE2}

%build
%post
if [ -L %{prefix}/web/content/uiconf ];then
	rm %{prefix}/web/content/uiconf
fi
# remove link and resym.
if [ -L %{prefix}/web/content/uiconf/kaltura/kmc ];then
	rm %{prefix}/web/content/uiconf/kaltura/kmc
fi

ls -sf %{prefix}/web/flash/kmc/%{version}/uiconf/kaltura/kmc/appstudio %{prefix}/web/content/uiconf
ln -sf %{prefix}/web/flash/kmc/%{version}/uiconf/kaltura/kmc %{prefix}/web/content/uiconf/kaltura/
if [ -r "%{prefix}/app/configurations/local.ini" -a -r "%{prefix}/app/configurations/system.ini" ];then
	php %{prefix}/app/deployment/uiconf/deploy_v2.php --ini=%{prefix}/web/flash/kmc/%{version}/config.ini >> %{prefix}/log/deploy_v2.log  2>&1
fi

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/login $RPM_BUILD_ROOT%{prefix}/app/alpha/web/lib $RPM_BUILD_ROOT%{prefix}/web/content/docs/pdf
#$RPM_BUILD_ROOT%{prefix}/web/content/uiconf/kaltura/kmc
mv kmc-docs-master/pdf $RPM_BUILD_ROOT%{prefix}/app/alpha/web/lib/ 
cp -r %{_builddir}/%{name}-%{version}/kmc-docs-master/* $RPM_BUILD_ROOT%{prefix}/web/content/docs/
mv %{_builddir}/%{name}-%{version}/login/%{kmc_login_version} $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/login/ 
mkdir $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/%{version}
cp -r %{_builddir}/%{name}-%{version}/%{version}/* $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/
mv %{_builddir}/%{name}-%{version}/uiconf $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/%{version}/
#cp -r $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/uiconf/kaltura/kmc/* $RPM_BUILD_ROOT%{prefix}/web/content/uiconf/kaltura/kmc/
cp %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/config.ini
cp %{SOURCE3} $RPM_BUILD_ROOT%{prefix}/web/content/docs/pdf

%preun
#if [ "$1" = 0 ] ; then
#	rm -f %{prefix}/web/content/uiconf/appstudio
#fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/kmc
%doc %{prefix}/web/content/docs/
%doc %{prefix}/app/alpha/web/lib/pdf/*
#%{prefix}/web/content/uiconf/kaltura/kmc
%config %{prefix}/web/flash/kmc/%{version}/config.ini


%changelog
* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.14-1
- SUP-1581 - Remix feature is exposed to customers in Old KDP templates
- KMC - After closing the "Support" page, the KMC is not usable
- PLAT-1038 - Closing the "Preview & Embed" page is causing a change in the KMC's layout

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.12-1
- Upgrade to 5.37.12, fixes:
  SUP-1634 - KMC will not alert when the user is uploading a file that is larger than 2GB using upload from desktop 
  PLAT-994 - enable use of draft entries in playlists - when video media is not expected 
  PLAT-985 - "Copy" button in "Preview & Embed" page is not working 
- Removed the limitation of not being able to create a transcoding profile with no flavors.
- Added the ability to choose transcoding profile for draft entry based on the permission "Enable KMC transcoding profile selection for draft entries".

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.11-1
- Upgrade to 5.37.11, fixes:
  SUP-1491 - Cannot configure content distribution role Ready for Deployment
  SUP-1265 - SEO values not populating Ready for Deployment
  SUP-1382 - KMC Return 2 Source flavors Ready for Deployment 

* Fri Feb 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.37.10-17
- Yet another symlink needed in %%post

* Wed Feb 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.37.10-16
- Fix preun error.

* Wed Feb 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v3.37.10-14
- docs added

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
