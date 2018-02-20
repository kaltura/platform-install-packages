%define kaltura_prefix /opt/kaltura
%define prefix %{kaltura_prefix}/prometheus-exporters
%global exporter_name            memcached_exporter
%global debug_package %{nil}

Summary: Prometheus Memcached Exporter
Name: kaltura-memcached-exporter
Version: 0.4.1 
Release: 1
License: ASL 2.0
Group: System Environment/Daemons
URL: https://github.com/prometheus/memcached_exporter/%{exporter_name}

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.
BuildArch: x86_64

Source: https://github.com/prometheus/%{exporter_name}/releases/download/v%{version}/memcached_exporter-%{version}.linux-amd64.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Prometheus is a monitoring system and time series database.
It collects metrics from configured targets at given intervals, evaluates 
rule expressions, displays the results, and can trigger alerts if some 
condition is observed to be true.

This package provides the Prometheus Memcached exporter meant to be 
used with Kaltura Server.


%prep
%setup -qn %{exporter_name}-%{version}.linux-amd64

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}
install -p -m 0755 %{exporter_name} $RPM_BUILD_ROOT/%{prefix}

%clean
%{__rm} -rf %{buildroot} 

%files
%doc LICENSE NOTICE 
%{prefix}/%{exporter_name}


%changelog
* Tue Feb 20 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 0.4.1-1
- First release
