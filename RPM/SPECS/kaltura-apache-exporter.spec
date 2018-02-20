%define kaltura_prefix /opt/kaltura
%define prefix %{kaltura_prefix}/prometheus-exporters
%global exporter_name            apache_exporter
%global debug_package %{nil}

Summary: Prometheus Apache Exporter
Name: kaltura-apache-exporter
Version: 0.5.0 
Release: 1
License: MIT
Group: System Environment/Daemons
URL: https://github.com/prometheus/apache_exporter/%{exporter_name}

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.
BuildArch: x86_64

Source: https://github.com/prometheus/apache_exporter/releases/download/v%{version}/apache_exporter-%{version}.linux-amd64.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Prometheus is a monitoring system and time series database.
It collects metrics from configured targets at given intervals, evaluates 
rule expressions, displays the results, and can trigger alerts if some 
condition is observed to be true.

This package provides the Prometheus Apache exporter meant to be 
used with Kaltura Server.


%prep
%setup -qn %{exporter_name}-%{version}.linux-amd64

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}
install -p -m 0755 %{exporter_name} $RPM_BUILD_ROOT/%{prefix}

%clean
%{__rm} -rf %{buildroot} 

%files
%doc LICENSE
%{prefix}/%{exporter_name}


%changelog
* Tue Feb 20 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 0.5.0-1
- First release
