%define prefix /opt/kaltura
%define studio_prefix %{prefix}/apps/player-studio-v7

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5-studio7
Version: v1.4.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz 
URL: https://github.com/kaltura/player-studio-v7/archive/refs/tags/%{name}.tar.gz
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

This package installs the Kaltura HTML5 Studio v7.

%prep
%setup -q



%install
mkdir -p $RPM_BUILD_ROOT%{studio_prefix}
npm install --legacy-peer-deps 
npm run build
cp -r build $RPM_BUILD_ROOT%{studio_prefix}/%{version}

%clean
rm -rf %{buildroot}

%post


%postun

%files
%defattr(-, root, root, 0755)
%{studio_prefix}/%{version}

%changelog
* Mon Feb 27 2023 jess.portnoy@kaltura.com <Jess Portnoy> - v1.4.0-1
- Support image playback
- Bug fixes

* Fri Jan 13 2023 jess.portnoy@kaltura.com <Jess Portnoy> - v1.1.0-1
- Player colors configuration
- Additional properties configuration for the Related plugin
- UI enhancements

* Mon Jan 2 2023 jess.portnoy@kaltura.com <Jess Portnoy> - v1.0.0-1
- Initial build
