%define prometheus_user	prometheus
%define prometheus_group prometheus

%define kaltura_prefix /opt/kaltura
%define prefix %{kaltura_prefix}/prometheus-exporters
%global exporter_name            mysqld_exporter
%global debug_package %{nil}

Summary: Prometheus MySQL Exporter
Name: kaltura-mysql-exporter
Version: 0.10.0 
Release: 1
License: ASL 2.0
Group: System Environment/Daemons
URL: https://github.com/prometheus/mysqld_exporter/%{exporter_name}

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.
BuildArch: x86_64

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


Source: https://github.com/prometheus/mysqld_exporter/releases/download/v%{version}/mysqld_exporter-%{version}.linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.init
Source3: %{name}-consul.json 
Source4: %{name}


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Prometheus is a monitoring system and time series database.
It collects metrics from configured targets at given intervals, evaluates 
rule expressions, displays the results, and can trigger alerts if some 
condition is observed to be true.

This package provides the Prometheus MySQL exporter meant to be 
used with Kaltura Server.


%prep
%setup -qn %{exporter_name}-%{version}.linux-amd64

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix} \
$RPM_BUILD_ROOT%{kaltura_prefix}/var/run/prometheus/exporters \
$RPM_BUILD_ROOT%{kaltura_prefix}/log/prometheus/exporters \
$RPM_BUILD_ROOT%{kaltura_prefix}/consul/etc/consul.d

install -p -m 0755 %{exporter_name} $RPM_BUILD_ROOT/%{prefix}

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/%{name}
%endif

%{__install} -m644 %SOURCE3 $RPM_BUILD_ROOT%{kaltura_prefix}/consul/etc/consul.d/mysqld.json
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m644 %SOURCE4 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/kaltura-mysqld-exporter

%pre
# create user/group, and update permissions
mkdir -p %{prefix}/prometheus 
getent group %{prometheus_group} >/dev/null || groupadd -r %{prometheus_group}  2>/dev/null
getent passwd %{prometheus_user} >/dev/null || useradd -m -r -d %{prefix}/prometheus -s /sbin/nologin -c "Prometheus Server" -g %{prometheus_group} %{prometheus_user} 2>/dev/null

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
service %{name} restart

%postun 
%if %use_systemd
	/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif


%clean
%{__rm} -rf %{buildroot} 

%files
%doc LICENSE NOTICE 
%{prefix}/%{exporter_name}
%if %{use_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%config %{kaltura_prefix}/consul/etc/consul.d/mysqld.json
%config(noreplace) %{_sysconfdir}/sysconfig/kaltura-mysqld-exporter
%defattr(-, %{prometheus_user}, %{prometheus_group}, 0755)
%{kaltura_prefix}/var/run/prometheus/exporters
%{kaltura_prefix}/log/prometheus/exporters


%changelog
* Tue Feb 20 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 0.10.0-1
- First release
