%define baseurl 54.211.235.142 
%define path kaltura-ce-rpm
Summary: Kaltura Server release file and package configuration
Name: kaltura-release
Version: 9.7.0
Release: 2 
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
#gpgkey = file:///etc/pki/rpm-gpg/
gpgcheck = 0

[Kaltura-noarch]
name = Kaltura Server arch independent
baseurl = http://%{baseurl}/%{path}/noarch
#gpgkey = file:///etc/pki/rpm-gpg/
gpgcheck = 0
EOF

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0644 kaltura.repo %{buildroot}%{_sysconfdir}/yum.repos.d/kaltura.repo

%clean
%{__rm} -rf %{buildroot}

%post
#rpm -q gpg-pubkey-e42d547b-3960bdf1 &>/dev/null || rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-matthias
exit 0

%files
#%defattr(-, root, root, 0755)
#%if %{!?_without_rpmpubkey:1}0
#%pubkey RPM-GPG-KEY-rpmforge-dag
#%else
#%doc RPM-GPG-KEY-rpmforge-matthias
#%endif
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/kaltura.repo
#%dir %{_sysconfdir}/pki/rpm-gpg/
#%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-*

%changelog
* Wed Jan 22 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- initial release.
