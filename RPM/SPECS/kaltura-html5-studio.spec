%define prefix /opt/kaltura

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5-studio
Version: v2.0.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.bz2 
Source1: studio.template.ini
URL: https://github.com/kaltura/player-studio/releases/download/%{version}/studio_%{version}.zip 
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

This package installs the Kaltura HTML5 Studio.

%prep
%setup -q



%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/apps/studio/
rm -f %{_builddir}/%{name}-%{version}/studio.ini
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT%{prefix}/apps/studio/%{version}
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/apps/studio/%{version}/
sed -i "s#@HTML5_STUDIO_VER@#%{version}#g" $RPM_BUILD_ROOT%{prefix}/apps/studio/%{version}/studio.template.ini

%clean
rm -rf %{buildroot}

%post


%postun

%files
%defattr(-, root, root, 0755)
%{prefix}/apps/studio/%{version}

%changelog
* Fri Jul 24 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v2.0.0-1
- Ver bounce. Aligned with HTML5lib 2.33.

* Sun Jun 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.9-1
- Add Studio support for Embed.ly embeds and Multi DRM plugins
- FEC-3611 Studio v2: after adding new boolean plugin, grey square displayed over 'delete' icon
- FEC-3612 Studio v2: need to add validation for Rate Selector selectable speeds
- FEC-3615 Give more width to player in studio better support on page plugins
- FEC-3628 Studio v2: need to click twice "Play" button after change player size, if 'auto preview' selected
- FEC-3613 Studio v2: Strings plugin - possible to add new strings, even if the plugin unchecked
- FEC-3609 Studio v2: incorrect aspect ratio selected ,if "Auto Preview" was checked
- SUP-4846 Cannot set mediaProxy.preferedFlavorBR without turning the SourceSelector on
- FEC-3628 Studio v2: need to click twice "Play" button after change player size, if 'auto preview' selected

* Sun May 31 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.8-1
- Ver bounce.

* Sun May 4 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.7-1
- Ver bounce.

* Sun Apr 5 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.6-1
- Ver bounce.

* Sun Mar 8 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.5-1
- SUP-3496 - Change file name when download with Universal studio

* Sun Jan 25 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.4-1
- FEC-2673 - Universal Studio allows to save empty UIVars

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.3-1
- SUP-3132 - Control Bar Icons are not transparent

* Thu Dec 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.2-1
- FEC-2401 - Add Strings plugin to Studio

* Mon Dec 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9.1-1
- SUP-3132 - Control Bar Icons are not transparent

* Sun Nov 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.9-1
- FEC-2049 - Send a notification of an error when the s_code in omniture fails to load

* Sun Sep 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.8-1
- Bouncing.

* Sun Aug 31 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.5-2
- https://github.com/kaltura/platform-install-packages/issues/214

* Thu Jul 10 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.5-1
- Disable player upgrade in case of playlist

* Sat Jun 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.1-4
- Bouncing.
 
* Wed May 21 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v1.1-1
- Additional Player v2 configurations available

* Thu Apr 24 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.9.7-1
- SUP-1805 - Studio V2 features - logo plugin
- SUP-1808 - Studio V2 features - Info plugin
- SUP-1928 - Studio V2 features - Watched color selector

* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.9.6-1
- FEC-1166 - Player Studio "does not support IE8 message" 
- FEC-1163 - Player studio gives absolute http urls for players, breaks HTTPS
- FEC-1162 - Can't scroll in player list in Universal studio
- FEC-1157 - Studio Duplicate should not require up-to-date player 
- FEC-1155 - Studio search is cut off in firefox 

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.9.4-1
- Navigation menu added
- FEC-1097 Default value is missing in L&F ( title label)
- FEC-1116 Flash Tabs no longer display UI after clicking on Studio in Firefox
- FEC-1112 Bumper is not playing while adding in v2 studio
- FEC-1018 Performance issue on IE8
- FEC-893 Cache issue with new players in P&E



* Fri Mar 14 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.9.2-1
- IE8 support
- FEC-883 vast UI
- FEC-1073 various UI issues with shlomit & michael
- FEC-995 Support HTML Companions ads vast default config.

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.9-1
- Fixes:  
    FEC-1008 Unable to Update player in IE9
    FEC-1003 video is not loading on ie9
    FEC-835 Studio v2: Unable to Create or Edit a player on IE8
    FEC-1010 Vast is not shown on IE19 in Edit Page (Happens now in all features, not only in Vast)
    FEC-1004 Features form is not expanding on ie10 while a feature is disabled
    FEC-1001 Scroll bar is not shown on Look&feel while expanding all features (All browsers)
    FEC-968 Studio v2: List of players is not refreshed after going back to list from duplicated player
    FEC-898 issues with help descriptions (tooltips) in analytics tab
    FEC-965 Studio v2: Number of players in players list is not kept (returns to default) after closing the player edit page
    FEC-922 Vast plugin doesn't have help icon and description
    FEC-975 cell hight doesn't match fonts size on ie10
    FEC-988 Apply changes button is green even while you load at first time the player
    FEC-964 line in all dropboxes is asymmetric

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.3-3
- Fixes the other points in https://github.com/kaltura/platform-install-packages/issues/30.

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.3-2
- Fixes  https://github.com/kaltura/platform-install-packages/issues/30
'Also /opt/kaltura/apps/studio/v0.3/ contains the zip archive that contains the same files as the directory, and should be cleaned up'
* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.3-1
- initial package.
