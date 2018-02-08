%define prometheus_user	prometheus
%define prometheus_group prometheus

%define kaltura_prefix /opt/kaltura
%define prefix %{kaltura_prefix}/prometheus
Summary: Prometheus is a monitoring system and time series database
Name: kaltura-prometheus
Version: 2.1.0 
Release: 1
License: ASL 2.0
Group: System Environment/Daemons
URL: http://prometheus.org/

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.
Requires(pre): shadow-utils

%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
%if 0%{?rhel}  == 6
Requires: initscripts >= 8.36
Requires: daemon
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires: systemd
BuildRequires: systemd
%endif

Source: https://github.com/prometheus/prometheus/releases/download/v%{version}/prometheus-%{version}.linux-amd64.tar.gz
Source1: prometheus.yml
Source2: %{name}_0_general.yml
Source3: %{name}_1_memcached.yml
Source4: %{name}.service
Source5: %{name}.sysconf
Source6: %{name}.init

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


%description
Prometheus is a monitoring system and time series database.
It collects metrics from configured targets at given intervals, evaluates 
rule expressions, displays the results, and can trigger alerts if some 
condition is observed to be true.

This package provides the Prometheus daemon and configuration meant to be 
used with Kaltura Server.


%prep
%setup -qn prometheus-%{version}.linux-amd64



%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/etc/rules
mkdir -p $RPM_BUILD_ROOT%{prefix}/data
mkdir -p $RPM_BUILD_ROOT%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{kaltura_prefix}/var/run/prometheus
mkdir -p $RPM_BUILD_ROOT%{kaltura_prefix}/log/prometheus
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/etc
cp %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/etc/rules/0_general.yml
cp %{SOURCE3} $RPM_BUILD_ROOT%{prefix}/etc/rules/1_memcached.yml
cp prometheus $RPM_BUILD_ROOT%{prefix}/bin/
cp promtool $RPM_BUILD_ROOT%{prefix}/bin/
cp -r console_libraries $RPM_BUILD_ROOT%{prefix}/
cp -r consoles $RPM_BUILD_ROOT%{prefix}/

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE4 \
        $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE6} \
   $RPM_BUILD_ROOT%{_initrddir}/%{name}
%endif


%clean
%{__rm} -rf %{buildroot}

%pre
# create user/group, and update permissions
getent group %{prometheus_group} >/dev/null || groupadd -r %{prometheus_group}  2>/dev/null
getent passwd %{prometheus_user} >/dev/null || useradd -m -r -d %{prefix} -s /sbin/nologin -c "Prometheus Server" -g %{prometheus_group} %{prometheus_user} 2>/dev/null

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop %{name}.service >/dev/null 2>&1 ||:
%else
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
%endif
fi

%post
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset %{name}.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add %{name}
%endif
fi

%postun 
%if %use_systemd
	/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif


%files
%defattr(-, root, root, 0755)
%doc LICENSE NOTICE 
%{_sysconfdir}/sysconfig/%{name}
%if %{use_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%{prefix}/consoles
%{prefix}/etc
%{prefix}/console_libraries
%{prefix}/bin
%defattr(-, %{prometheus_user}, %{prometheus_group}, 0755)
%{kaltura_prefix}/var/run/prometheus
%{kaltura_prefix}/log/prometheus
%{prefix}/data




%changelog
* Thu Feb 8 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 2.1.0-1
- First release
