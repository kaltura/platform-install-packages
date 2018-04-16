%define prometheus_user	prometheus
%define prometheus_group prometheus

%define kaltura_prefix /opt/kaltura
%define kaltura_prefix /opt/kaltura
%define prefix %{kaltura_prefix}/prometheus-exporters
%global exporter_name            sphinx-exporter
%global debug_package %{nil}

Summary: Prometheus Sphinx Exporter
Name: kaltura-sphinx-exporter
Version: 2.2.1 
Release: 1
License: AGPLv3+
Group: System Environment/Daemons
URL: https://github.com/jessp01/%{exporter_name}

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.

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


Source: https://github.com/jessp01/sphinx-exporter/archive/sphinx-exporter-%{version}.tar.gz
Source1: %{name}.service
Source2: %{name}.init
Source3: %{name}-consul.json 


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: golang-bin glide

%description
Prometheus is a monitoring system and time series database.
It collects metrics from configured targets at given intervals, evaluates 
rule expressions, displays the results, and can trigger alerts if some 
condition is observed to be true.

This package provides the Prometheus Sphinx exporter meant to be 
used with Kaltura Server.


%prep
%setup -qn sphinx-exporter-%{version}

%build
mkdir -p %{_tmppath}/%{name}-%{version}/go/src
ln -s `pwd` %{_tmppath}/%{name}-%{version}/go/src/%{name}
export GOPATH=%{_tmppath}/%{name}-%{version}/go
cd %{_tmppath}/%{name}-%{version}/go/src/%{name}
glide init --non-interactive
glide install
go build -o %{exporter_name} -ldflags '-buildid %{name}-%{version}-%{release}-RPM'

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

%{__install} -m644 %SOURCE3 $RPM_BUILD_ROOT%{kaltura_prefix}/consul/etc/consul.d/sphinx.json

%clean
%{__rm} -rf %{buildroot} %{_tmppath}/%{name}-%{version}

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


%files
%{prefix}/%{exporter_name}
%if %{use_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif
%config %{kaltura_prefix}/consul/etc/consul.d/sphinx.json
%defattr(-, %{prometheus_user}, %{prometheus_group}, 0755)
%{kaltura_prefix}/var/run/prometheus/exporters
%{kaltura_prefix}/log/prometheus/exporters


%changelog
* Mon Feb 19 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 2.2.1-1
- First release
