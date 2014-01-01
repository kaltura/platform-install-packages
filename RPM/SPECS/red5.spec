Summary: Red5 Server
Name: red5
Version: 1.0.0
Release: 1
Source0: %{name}-%{version}.tar.gz
Source1: flash-demos.tar.gz
Source2: red5.init
License: Apache Software License 2.0
URL: http://www.red5.org/
Group: Applications/Networking
BuildRoot: %{_builddir}/%{name}-%{version}-%{release}-root
BuildRequires: ant
Requires: chkconfig
Requires: java

%define red5_lib    /usr/lib/red5
%define red5_log    /var/log/red5

%description
The Red5 open source Flash server allows you to record and stream video to the Flash Player.

%prep
%setup -q

%build
ant dist-installer

%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/usr
# extra files
tar zxvf %{SOURCE1}
cp -r demos $RPM_BUILD_ROOT%{red5_lib}/webapps/root/  # recursively install
install -m 0755 -d $RPM_BUILD_ROOT%{red5_lib}/plugins
install -m 0755 plugins/* $RPM_BUILD_ROOT%{red5_lib}/plugins
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/red5
install -d $RPM_BUILD_ROOT%{red5_log}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(0755,root,root) %dir %{red5_lib}
%attr(0644,root,root) %{red5_lib}/*.jar
%attr(0755,root,root) %{red5_lib}/*.sh

%attr(0755,root,root) %dir %{red5_lib}/lib
%attr(0644,root,root) %{red5_lib}/lib/*

%attr(0755,root,root) %dir %{red5_lib}/webapps
%attr(0644,root,root) %{red5_lib}/webapps/*

%attr(0755,root,root) %dir %{red5_lib}/plugins
%attr(0644,root,root) %{red5_lib}/plugins/*

%attr(0755,root,root) %dir %{red5_lib}/conf
%config %{red5_lib}/conf/*

%attr(0755,root,root) /etc/rc.d/init.d/red5
%doc license.txt doc/*

%attr(0755,root,root) %dir %{red5_log}

%post
/sbin/chkconfig --add red5

%postun
/sbin/service red5 restart > /dev/null 2>&1 || :

%preun
if [ "$1" = 0 ]; then
    /sbin/service/red5 stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del red5
fi

%changelog
* Wed Dec 26 2012 Tetsuya Morimoto <tetsuya.morimoto at gmail.com> 1.0.0-1%{?dist}
- first packaging for Red5 1.0 Final
