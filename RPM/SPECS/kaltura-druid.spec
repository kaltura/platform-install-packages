%define __jar_repack 0
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0
%define druid_user kaltura
%define druid_group kaltura 
%define prefix /opt/kaltura
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

Name: kaltura-druid	
Version: 0.16.0
Release: 1
Summary: Druid	
Group: Applications/Internet
License: Apache License, Version 2.0
URL: http://%{name}.io/
Source0: http://mirror.vorboss.net/apache/incubator/druid/%{version}-incubating/apache-druid-%{version}-incubating-bin.tar.gz

Source1: %{name}.env.sh.source
Source2: %{name}.initscript
Source3: %{name}.service
Source4: %{name}_broker.service
Source5: %{name}_coordinator.service
Source6: %{name}_historical.service
Source9: %{name}_middle_manager.service
Source10: %{name}_overlord.service


BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Requires: kaltura-kava
%if %{use_systemd}
Requires: systemd
BuildRequires: systemd
%else
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

AutoReqProv: no

%description
An open-source, real-time data store designed to power interactive applications at scale.

%pre
%{__mkdir_p} %{prefix}
# create user/group, and update permissions
getent group %{kaltura_group} >/dev/null || groupadd -r %{kaltura_group} -g7373 2>/dev/null
getent passwd %{kaltura_user} >/dev/null || useradd -m -r -u7373 -d %{prefix} -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null


%prep
%setup -q -n apache-druid-%{version}-incubating 

%build

%install
# create directory skeleton
%{__mkdir_p} %{buildroot}/usr/lib/druid
%{__mkdir_p} %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/druid
%{__mkdir_p} %{buildroot}%{_var}/log/druid
%{__mkdir_p} %{buildroot}%{_var}/run/druid
%{__mkdir_p} %{buildroot}%{_var}/tmp/druid

# install custom variables and initscript
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}
%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
for SERVICE in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE9} %{SOURCE10}; do
%{__install} -m644 $SERVICE \
        $RPM_BUILD_ROOT%{_unitdir}/
done

%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-server
%endif

# install druid libraries
%{__cp} -Rv lib/* %{buildroot}/usr/lib/druid/
%{__cp} -Rv extensions %{buildroot}/usr/lib/druid/


%files
%defattr(-,%{druid_user},%{druid_group},755)
/usr/lib/druid
%dir %{_var}/log/druid 
%dir %{_var}/tmp/druid 
%dir %{_var}/run/druid
%defattr(755,root,root)
%defattr(644,root,root)
%{_sysconfdir}/%{name}
%if %{use_systemd}
%{_unitdir}/%{name}*.service
%else
%{_initrddir}/%{name}-server
%endif

%post
if [ $1 -eq 1 ]; then
%if %{use_systemd}
for SERVICE in druid_broker.service druid_coordinator.service druid_historical.service druid_middle_manager.service druid_overlord.service; do 
    /usr/bin/systemctl preset `basename $SERVICE` >/dev/null 2>&1 ||:
done
%else
    /sbin/chkconfig --add %{name}-server
%endif
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
for SERVICE in druid_broker.service druid_coordinator.service druid_historical.service  druid_middle_manager.service druid_overlord.service; do
    /usr/bin/systemctl --no-reload disable $SERVICE >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop $SERVICE >/dev/null 2>&1 ||:
done
%else
    /sbin/service %{name}-server stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}-server
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 11 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.16.0-1
- New upstream release

* Thu Jul 25 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.15.0-1
- New ver

* Thu Jan 14 2016 Luciano Coutinho <lucianocoutinho@live.com> 0.6.171-0.2
- fixed typos in initscript and updated the build process to preserve 
  original source file as-is.

* Mon Feb 02 2015 Cleber Rodrigues <cleber@cleberar.com> 0.6.171-0.1
- first
