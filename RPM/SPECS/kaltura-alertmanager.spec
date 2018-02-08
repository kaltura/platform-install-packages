%define prometheus_user	prometheus
%define prometheus_group prometheus

%define kaltura_prefix /opt/kaltura
%define prefix %{kaltura_prefix}/prometheus/alertmanager
Summary: Alertmanager handles alerts sent by client applications such as the Prometheus server
Name: kaltura-alertmanager
Version: 0.13.0
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

Source: https://github.com/prometheus/alertmanager/releases/download/v%{version}/alertmanager-%{version}.linux-amd64.tar.gz 
Source1: alertmanager.yml
Source2: %{name}_kaltura.tmpl
Source3: %{name}.service
Source4: %{name}.sysconf
Source5: %{name}.init

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


%description
Alertmanager handles alerts sent by client applications such as the 
Prometheus server. It takes care of deduplicating, grouping, and routing them to 
the correct receiver integrations such as email, PagerDuty, or OpsGenie. 
It also takes care of silencing and inhibition of alerts.

This package provides the Prometheus Alertmanager daemon and configuration meant to be 
used with Kaltura Server.


%prep
%setup -qn alertmanager-%{version}.linux-amd64



%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/etc/templates
mkdir -p $RPM_BUILD_ROOT%{prefix}/data
mkdir -p $RPM_BUILD_ROOT%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{kaltura_prefix}/var/run/alertmanager
mkdir -p $RPM_BUILD_ROOT%{kaltura_prefix}/log/alertmanager
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/etc
cp %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/etc/templates/kaltura.tmpl
cp alertmanager $RPM_BUILD_ROOT%{prefix}/bin/
cp amtool $RPM_BUILD_ROOT%{prefix}/bin/

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE4 \
        $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE5} \
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
%{prefix}/etc
%config(noreplace) %{prefix}/etc/alertmanager.yml
%config(noreplace) %{prefix}/etc/templates/*.tmpl
%{prefix}/bin
%defattr(-, %{prometheus_user}, %{prometheus_group}, 0755)
%{kaltura_prefix}/var/run/alertmanager
%{kaltura_prefix}/log/alertmanager
%{prefix}/data




%changelog
* Thu Feb 8 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 0.13.0-1
- First release
