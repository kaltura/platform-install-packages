%define kaltura_prefix /opt/kaltura
%define prefix %{kaltura_prefix}/prometheus-exporters
%global exporter_name            prom-nginx-exporter
%global debug_package %{nil}

Summary: Prometheus Nginx Exporter
Name: kaltura-nginx-exporter
Version: 1.0.0
Release: 1
License: MIT
Group: System Environment/Daemons
URL: https://github.com/monitoring-tools/%{exporter_name}

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.

Source: https://github.com/monitoring-tools/prom-nginx-exporter/archive/%{exporter_name}-v%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: golang-bin glide

%description
Prometheus is a monitoring system and time series database.
It collects metrics from configured targets at given intervals, evaluates 
rule expressions, displays the results, and can trigger alerts if some 
condition is observed to be true.

This package provides the Prometheus Nginx exporter meant to be 
used with Kaltura Server.


%prep
%setup -qn %{exporter_name}-%{version}

%build
make build-linux

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}
install -p -m 0755 linux_amd64/%{exporter_name} $RPM_BUILD_ROOT/%{prefix}

%clean
%{__rm} -rf %{buildroot} %{_tmppath}/%{name}-%{version}

%files
%doc LICENSE README.md
%{prefix}/%{exporter_name}


%changelog
* Tue Feb 20 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- First release
