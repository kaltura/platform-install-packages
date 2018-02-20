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

Source: https://github.com/prometheus/mysqld_exporter/releases/download/v%{version}/mysqld_exporter-%{version}.linux-amd64.tar.gz

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
mkdir -p $RPM_BUILD_ROOT/%{prefix}
install -p -m 0755 %{exporter_name} $RPM_BUILD_ROOT/%{prefix}

%clean
%{__rm} -rf %{buildroot} 

%files
%{prefix}/%{exporter_name}


%changelog
* Tue Feb 20 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 0.10.0-1
- First release
