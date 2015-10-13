Summary: Red5 Server
Name: kaltura-red5
Version: 1.0.6
Release: 1
Source0: %{name}-%{version}.tar.gz
#Source1: %{name}-flash-%{version}.tar.bz2
Source2: red5.init
License: Apache Software License 2.0
URL: http://www.red5.org/
Group: Applications/Networking
BuildRoot: %{_builddir}/%{name}-%{version}-%{release}-root
Requires: chkconfig,jre >= 1.7.0

%define red5_lib    /usr/lib/red5
%define red5_log    /var/log/red5
%define debug_package %{nil}

%description
The Red5 open source Flash server allows you to record and stream video to the Flash Player.

%prep
%setup -qn red5-server-%{version}-RELEASE

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib
cp -r %{_builddir}/red5-server-%{version}-RELEASE $RPM_BUILD_ROOT/%{red5_lib}
rm $RPM_BUILD_ROOT/%{red5_lib}/*.bat
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
%doc %{red5_lib}/license.txt 


%attr(0755,root,root) %dir %{red5_log}


%post
/sbin/chkconfig --add red5
chkconfig red5 on
/etc/init.d/red5 start

%postun
/sbin/service red5 restart > /dev/null 2>&1 || :

%preun
if [ "$1" = 0 ]; then
    /sbin/service/red5 stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del red5
fi

%changelog
* Tue Oct 13  2015 Jess Portnoy <jess.portnoy@kaltura.com> 1.0.6-1
- https://github.com/Red5/red5-server/releases/tag/v1.0.6-RELEASE

* Sat Jan 3 2015 Jess Portnoy <jess.portnoy@kaltura.com> 1.0.4-1
- New ver.
- No need to build anymore as Red5 offers prebuilt package.

* Tue Nov 11 2014 Jess Portnoy <jess.portnoy@kaltura.com> 1.0.3-1
- New ver.

* Wed Feb 19 2014 Jess Portnoy <jess.portnoy@kaltura.com> 1.0.2-1
- Maybe this version is better? LOVE using RC versions.. sigh.

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> 1.0.0-2
- Start at init.

* Wed Dec 26 2012 Tetsuya Morimoto <tetsuya.morimoto at gmail.com> 1.0.0-1
- first packaging for Red5 1.0 Final
