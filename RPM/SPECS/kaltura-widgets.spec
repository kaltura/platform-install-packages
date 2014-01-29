Summary: Kaltura widgets
Name: kaltura-widgets
Version: 1.0.0
Release: 5 
License: AGPLv3+
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: kaltura-clipapp, kaltura-kmc, kaltura-kdp, kaltura-kcw kaltura-kdp kaltura-kdp3 kaltura-kdp3wrapper kaltura-kvpm, kaltura-kclip kaltura-kdpwrapper

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

This package install the Kaltura Flash widgets: KMC, KDP3, KCW, KDP3Wrapper, KVPM.

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files

%changelog
* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-5
- Require kdp wrapper

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-4
- Require kclip

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-3
- kaltura-kclip added

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-2
- Corrected deps.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- Initial package. 
