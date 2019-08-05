%define __jar_repack 0
%define debug_package %{nil}
%define _name	     kafka
%define _user	     kafka
%define _group	     kafka
%define _prefix      /opt
%define _conf_dir    %{_sysconfdir}/%{_name}
%define _log_dir     %{_var}/log/%{_name}
%define _data_dir    %{_sharedstatedir}/%{_name}

Summary: Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.
Name: kafka
Version: %{version}
Release: %{build_number}
License: Apache License, Version 2.0
URL: http://kafka.apache.org/
Source0: %{source}
Source1: %{_name}.service
Source2: %{_name}.logrotate
Source3: %{_name}.log4j.properties
Source4: %{_name}.sysconfig
%if %{build_with_metrics}
# adding metric specific sources.
Source6: metrics-graphite-2.2.0.jar
Source7: kafka-graphite-1.0.5.jar
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}
Vendor: Apache Software Foundation
Packager: Ivan Dyachkov <ivan.dyachkov@klarna.com>
Provides: kafka kafka-server
BuildRequires: systemd
%systemd_requires

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization. It can be elastically and transparently expanded without downtime. Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers. Messages are persisted on disk and replicated within the cluster to prevent data loss.

%prep
%setup -n %{source_name}

%build
rm -f libs/{*-javadoc.jar,*-scaladoc.jar,*-sources.jar,*-test.jar}

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{_name}/{libs,bin,config}
mkdir -p $RPM_BUILD_ROOT%{_log_dir}
mkdir -p $RPM_BUILD_ROOT%{_data_dir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 755 bin/*.sh $RPM_BUILD_ROOT%{_prefix}/%{_name}/bin
install -p -D -m 644 config/* $RPM_BUILD_ROOT%{_prefix}/%{_name}/config
install -p -D -m 644 config/server.properties $RPM_BUILD_ROOT%{_conf_dir}/
sed -i "s:^log.dirs=.*:log.dirs=%{_data_dir}:" $RPM_BUILD_ROOT%{_conf_dir}/server.properties
install -p -D -m 755 %{S:1} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 644 %{S:2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{_name}
install -p -D -m 644 %{S:3} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{_name}
install -p -D -m 644 libs/* $RPM_BUILD_ROOT%{_prefix}/%{_name}/libs
%if %{build_with_metrics}
# adding metric specific sources.
install -p -D -m 644 %{S:6} $RPM_BUILD_ROOT%{_prefix}/%{_name}/libs
install -p -D -m 644 %{S:7} $RPM_BUILD_ROOT%{_prefix}/%{_name}/libs
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group %{_group} >/dev/null || /usr/sbin/groupadd -r %{_group}
/usr/bin/getent passwd %{_user} >/dev/null || /usr/sbin/useradd -r \
  -g %{_group} -d %{_prefix}/%{_name} -s /bin/bash -c "Kafka" %{_user}

%post
%systemd_post %{_name}.service

%preun
%systemd_preun %{_name}.service

%postun
%systemd_postun %{_name}.service

%files
%defattr(-,root,root)
%{_unitdir}/%{_name}.service
%config(noreplace) %{_sysconfdir}/logrotate.d/%{_name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{_name}
%config(noreplace) %{_conf_dir}/*
%{_prefix}/%{_name}
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}
%doc NOTICE
%doc LICENSE
