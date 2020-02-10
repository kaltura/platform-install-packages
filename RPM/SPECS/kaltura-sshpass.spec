%define prefix /opt/kaltura
Summary: Non-interactive SSH authentication utility
Name: kaltura-sshpass
Version: 1.06
Release: 1
License: GPLv2
Group: Applications/Internet
URL: http://sshpass.sourceforge.net/

Source: http://downloads.sourceforge.net/project/sshpass/sshpass/%{version}/sshpass-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description
Tool for non-interactively performing password authentication with so called
"interactive keyboard password authentication" of SSH. Most users should use
more secure public key authentication of SSH instead.

%prep
%setup -qn sshpass-%{version}

%build
./configure --prefix=%{prefix}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS
%doc %{prefix}/share/man/man1/sshpass.1*
%{prefix}/bin/sshpass

%changelog
* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.05-1
- Initial package.
