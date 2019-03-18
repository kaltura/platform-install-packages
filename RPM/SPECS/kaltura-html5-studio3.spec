%define prefix /opt/kaltura
%define studio_prefix %{prefix}/apps/studioV3

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5-studio3
Version: v3.3.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.bz2 
Source1: studio3.template.ini
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

This package installs the Kaltura HTML5 Studio v3.

%prep
%setup -q



%install
mkdir -p $RPM_BUILD_ROOT%{studio_prefix}
rm -f %{_builddir}/%{name}-%{version}/studio.ini
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT%{studio_prefix}/%{version}
cp %{SOURCE1} $RPM_BUILD_ROOT%{studio_prefix}/%{version}/studio.template.ini
sed -i "s#@HTML5_STUDIO3_VER@#%{version}#g" $RPM_BUILD_ROOT%{studio_prefix}/%{version}/studio.template.ini

%clean
rm -rf %{buildroot}

%post


%postun

%files
%defattr(-, root, root, 0755)
%{studio_prefix}/%{version}

%changelog
* Mon Mar 18 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v3.3.0-1
- FEC-8880: add support for youtube
- FEC-8805: playlist support
- FEC-8894: OVP player identified as OTT after creating OTT player
- FEC-8895: OTT player identified as OVP


* Thu Feb 7 2019 jess.portnoy@kaltura.com <Jess Portnoy> - v3.2.3-1
- First release
