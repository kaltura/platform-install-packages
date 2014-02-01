%define prefix /opt/kaltura

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5-studio
Version: v0.3
Release: 1 
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.bz2 
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
cp -r %{_builddir}/%{name}-%{version} $RPM_BUILD_ROOT%{prefix}/apps/studio/%{version}

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-, root, root, 0755)
%{prefix}/apps/studio/%{version}

%changelog
* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - v0.3-1
- initial package.
