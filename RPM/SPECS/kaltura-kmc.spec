%define prefix /opt/kaltura
Name:	kaltura-kmc
Version: v5.39.8
Release: 2
Summary: Kaltura Management Console

Group: System Management	
License: AGPLv3+	
URL: https://github.com/kaltura/kmc 
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
if [ -L %{prefix}/web/content/uiconf ];then
	rm %{prefix}/web/content/uiconf
fi
# remove link and resym.
if [ -L %{prefix}/web/content/uiconf/kaltura/kmc ];then
	rm %{prefix}/web/content/uiconf/kaltura/kmc
fi

mkdir -p %{prefix}/web/content/uiconf/kaltura
cp -r %{prefix}/web/flash/kmc/%{version}/uiconf/kaltura/kmc %{prefix}/web/content/uiconf/kaltura
#if [ -r "%{prefix}/app/configurations/local.ini" -a -r "%{prefix}/app/configurations/system.ini" ];then
#	php %{prefix}/app/deployment/uiconf/deploy_v2.php --ini=%{prefix}/web/flash/kmc/%{version}/config.ini >> %{prefix}/log/deploy_v2.log  2>&1
#fi

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/login
mkdir -p $RPM_BUILD_ROOT%{prefix}/app/alpha/web/lib
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content/docs/pdf
#cp doc/pdf/KMC_User_Manual.pdf $RPM_BUILD_ROOT%{prefix}/web/content/docs/pdf
cp -r doc/* $RPM_BUILD_ROOT%{prefix}/web/content/docs/
mv doc/pdf $RPM_BUILD_ROOT%{prefix}/app/alpha/web/lib/ 
mv %{_builddir}/%{name}-%{version}/login/%{kmc_login_version} $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/login/ 
mkdir $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/%{version}
cp -r %{_builddir}/%{name}-%{version}/%{version}/* $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/
mv %{_builddir}/%{name}-%{version}/uiconf $RPM_BUILD_ROOT%{prefix}/web/flash/kmc/%{version}/
cp %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/web/flash/kmc/%{version}/config.ini

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
* Thu Aug 20 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.8-2
- Version bounce to align with kaltura-html5lib v2.34.

* Thu Aug 6 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.8-1
- Version bounce to align with server 10.17.0.

* Fri Jul 24 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.6-1
- PLAT-3409 - CustomData.System name with underscore is not supported by KMC->Mapping fields fail.

* Sun Jun 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.3-4
- Ver bounce of HTML5 to v2.32.1

* Sun Jun 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.3-3
- Ver bounce of HTML5 to v2.32

* Sun Jun 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.1-3
- SUP-4926 - Wrong KMC owner accounts - change to right account not saved

* Sun May 31 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.1-3
- New HTML5 lib - v2.31.

* Mon May 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.1-2
- New HTML5 lib.

* Sat Apr 25 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.39.1-1
- SUP-4303 - A redundant message when creating or editing a conversion profile
- PLAT-2796 - User get error messages on transcoding setting screen when user role sets with "transcoding setting-view only"
- PLAT-2815 - Cannot save current transcoding profile without flavors

* Sun Apr 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.38.11-1
- SUP-3963 - Issue with Date time field in the Video Metadata
- SUP-4105 - Error is thrown when accessing upload center
- SUP-4009 - Unable to change account owner
- PLAT-2608 - Link to live analytics exits on content tab when user dont have permissions to analytics

* Mon Mar 9 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-2
- new HTML5 lib ver.

* Sat Feb 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.10-1
- Ver bounce.

* Sun Feb 8 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.9-1
- SUP-3658 - KMC Error Message and Crash
- SUP-3681 - KMC doesn't set required tags when logging as a "Content Moderator" role
- FEC-2653 - KMC: after click on Studio tab, the flash studio appears for 1-2 seconds and after U.studio loaded
- FEC-2654 - KMC: If select Flash Studio, after U. Studio and refresh the web page - Flash studio loaded

* Sun Jan 25 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.8-1
- SUP-3531 - Analytic data inconsistency in certain scenario

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.7-4
- Copy the entire doc tree to web/content/docs.

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.7-1
- PLAT-2243 - kmc - kms categories Bulk delete Warning message is incorrect
- PLAT-2242 - KMS \ KMC _edit warning category- Warning is not provided when changing between catrgoried 

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.4-2
- Bounce versions in config.

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.4-1
- Support for Live Analytics
- Prevent player v2 from throwing live events from KMC
- PLAT-2157 - Akamai live streaming exported XML should specify video format 
- PLAT-1703 - Add a warning in KMC when user trying to edit/delete one of KMS native categories 

* Thu Dec 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.30-1
- PLAT-2157 - Akamai live streaming exported XML should specify video format
- PLAT-1703 - Add a warning in KMC when user trying to edit/delete one of KMS native categories
- FEC-2282 - Lead with Universal studio ( instead of flash ) when pressing studio in KMC
- SUP-3269 - Edit Entry window of live entry with Manager KMC role
- PLAT-2081 - New live transcording profile is added to new streaming window just after refreshing KMC browser
- PLAT-1908 - Missing exception on approve content when user does not have permission
- PLAT-2223 - KMC - New Transcoding Profile - The creation of a new transcoding profile redirects the KMC to the Content tab (once per session) 

* Mon Dec 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.27-4
- HTML5lib bounce to v2.22.

* Tue Nov 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.27-3
- Bounce HTML5 lib ver in config.ini to v2.21.

* Sun Nov 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.27-2
- Bounce HTML5 lib ver in config.ini to v2.20.

* Sun Oct 5 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.27-1
- PLAT-1681 - KMC- Manual livestream entry has "hdnetworkmanifest" livestream configuration though no HDS url was configured
- SUP-2392 - Disable editing of existing webvtt captions as well as not allow adding new ones (was "Webvtt upload from the KMC is not working")
- SUP-2817 - KMC Date/Time bug

* Sun Sep 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.24-1
- ver bounce.

* Sun Aug 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.22-2
- Upped HTML5 version

* Thu Jul 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.22-1
- PLAT-1342 - Reflect replacement ERROR status in the KMC
- PLAT-1389 - New Access Control Profiles are missing "Allow All" settings for IPs (the default access control profile is missing it too)
- FEC-1463 - on line help - broken links to live reports and live transcoding profiles' pages
- PLAT-340 - B&S report is cut in KMC while using resolution low then 1400 * 1050 

* Sat Jun 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.21-1
- PLAT-974 - add partner Reference ID to KMC and Multi-Account console

* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.20-2
- Bounce the HTML5 and KMC versions in config.

* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.20-1
- PLAT-671 - KMC - Bulk Action - Remove Tags - Causes popup when opening category
- FEC-1302 - security-fix (Oracle) - KMC support form does not validate input on GET parameters (XSS)
- FEC-1402 - CLONE - security-fix (Oracle) - KMC support form does not validate input on GET parameters (XSS)

* Wed May 7 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.17-6
- Added URL pointing to GIT repo.

* Sat Apr 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.17-3
- Bounce KMC and HTML5lib vers in config.ini.

* Thu Apr 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.17-1
- PLAT-1242 - Uploading a "m4a" file from desktop - the file media type is not automatically chosen
- PLAT-1265 - KMC online guide broken link on submitbulkoptions.htm

* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.16-1
- Live Reports in Analytics (phase 0)
- Legacy embed code removed from Preview & Embed page for Players falling back to HTML5 v2
- SUP-1713 - Analytics categories filter is not needed 
- FEC-1131 - When only universal studio is enabled for partner - the main studio menu is not displayed at all in KMC 

* Wed Mar 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v5.37.14-3
- kmc_config.ini updated with new kmc ver.

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
