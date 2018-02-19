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

Source: https://github.com/jessp01/sphinx-exporter/archive/sphinx-exporter-%{version}.tar.gz

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
mkdir -p $RPM_BUILD_ROOT/%{prefix}
install -p -m 0755 %{exporter_name} $RPM_BUILD_ROOT/%{prefix}

%clean
%{__rm} -rf %{buildroot} %{_tmppath}/%{name}-%{version}

%files
%{prefix}/%{exporter_name}


%changelog
* Mon Feb 19 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 2.2.1-1
- First release
