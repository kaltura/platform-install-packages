%define baseurl installrepo.kaltura.org
%define path releases/stable/RPMS
%define testpath releases/nightly/RPMS
%define prefix /opt/kaltura 
Summary: Kaltura Server release file and package configuration
Name: kaltura-release
Version: 9.12.0
Release: 5 
License: AGPLv3+
Group: Server/Platform 
URL: http://kaltura.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
Kaltura Server release file. This package contains yum 
configuration for the Kaltura RPM Repository, as well as the public
GPG keys used to sign them.




%build
%{__cat} <<EOF >kaltura.repo
# URL: http://kaltura.org/
[Kaltura]
name = Kaltura Server
baseurl = http://%{baseurl}/%{path}/\$basearch/
gpgkey = http://%{baseurl}/%{path}/\$basearch/RPM-GPG-KEY-kaltura
gpgcheck = 0 
enabled = 1

[Kaltura-noarch]
name = Kaltura Server arch independent
baseurl = http://%{baseurl}/%{path}/noarch
gpgkey = http://%{baseurl}/%{path}/noarch/RPM-GPG-KEY-kaltura
gpgcheck = 0
enabled = 1

[Kaltura-testing]
name = Kaltura Server arch independent
baseurl = http://%{baseurl}/%{testpath}/\$basearch/
gpgkey = http://%{baseurl}/%{testpath}/\$basearch/RPM-GPG-KEY-kaltura

gpgcheck = 0 
enabled = 0

[Kaltura-testing-noarch]
name = Kaltura Server arch independent
baseurl = http://%{baseurl}/%{testpath}/noarch
gpgkey = http://%{baseurl}/%{testpath}/noarch/RPM-GPG-KEY-kaltura
gpgcheck = 0
enabled = 0
EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 kaltura.repo %{buildroot}%{_sysconfdir}/yum.repos.d/kaltura.repo

%clean
%{__rm} -rf %{buildroot}

%post
if [ "$1" = 2 ];then
	if [ -r  %{prefix}/bin/kaltura-functions.rc ];then
		. %{prefix}/bin/kaltura-functions.rc
		if [ -r /etc/sysconfig/clock ];then
			. /etc/sysconfig/clock
		else 
			ZONE='unknown'
	  	fi
		send_install_becon %{name}-%{version}-%{release} $ZONE install_upgrade
	fi
fi
exit 0

%files
%dir %{_sysconfdir}/yum.repos.d/
%config %{_sysconfdir}/yum.repos.d/kaltura.repo

%changelog
* Tue Mar 18 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-2
- We will be signing our RPMs from now on.

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.12.0-1
- Ver Bounce to 9.12.0

* Thu Feb 27 2014 David Bezemer <info@davidbezemer.nl> - 9.11.0-6
- Add testing to base package

* Wed Feb 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-5
- Added update becon.

* Tue Feb 25 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-3
- URL to repo modified to include 'releases' in path.

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-2
- dont need i686

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.11.0-1
- 9.11.0

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.9.0-1
- 9.9.0

* Sun Jan 26 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-3
- Added 32bit repos.

* Wed Jan 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- initial release.

