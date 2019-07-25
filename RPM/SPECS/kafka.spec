%define __jar_repack 0
%define debug_package %{nil}
%define build_with_metrics 1
%define _name	     kafka
%define _user	     kafka
%define _group	     kafka
%define _prefix      /opt
%define _conf_dir    %{_sysconfdir}/%{_name}
%define _log_dir     %{_var}/log/%{_name}
%define _data_dir    %{_sharedstatedir}/%{_name}
%define _scala_version 2.12

Summary: Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.
Name: kafka
Version: 2.3.0
Release: 1
License: Apache License, Version 2.0
URL: http://kafka.apache.org/
Source0: %{name}_%{_scala_version}-%{version}.tgz
Source1: %{name}.service
Source2: %{name}.logrotate
Source3: %{name}.log4j.properties
Source4: %{name}.sysconfig
%if %{build_with_metrics}
# adding metric specific sources.
Source6: metrics-graphite-2.2.0.jar
Source7: kafka-graphite-1.0.5.jar
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}
Vendor: Apache Software Foundation
Provides: kafka kafka-server
BuildRequires: systemd
%systemd_requires

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization. It can be elastically and transparently expanded without downtime. Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers. Messages are persisted on disk and replicated within the cluster to prevent data loss.

%prep
%setup -q -n %{name}_%{_scala_version}-%{version}

%build
rm -f libs/{*-javadoc.jar,*-scaladoc.jar,*-sources.jar,*-test.jar}

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{name}/{libs,bin,config}
mkdir -p $RPM_BUILD_ROOT%{_log_dir}
mkdir -p $RPM_BUILD_ROOT%{_data_dir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 755 bin/*.sh $RPM_BUILD_ROOT%{_prefix}/%{name}/bin
install -p -D -m 644 config/* $RPM_BUILD_ROOT%{_prefix}/%{name}/config
install -p -D -m 644 config/server.properties $RPM_BUILD_ROOT%{_conf_dir}/
sed -i "s:^log.dirs=.*:log.dirs=%{_data_dir}:" $RPM_BUILD_ROOT%{_conf_dir}/server.properties
install -p -D -m 755 %{S:1} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 644 %{S:2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 644 %{S:3} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -p -D -m 644 libs/* $RPM_BUILD_ROOT%{_prefix}/%{name}/libs
%if %{build_with_metrics}
# adding metric specific sources.
install -p -D -m 644 %{S:6} $RPM_BUILD_ROOT%{_prefix}/%{name}/libs
install -p -D -m 644 %{S:7} $RPM_BUILD_ROOT%{_prefix}/%{name}/libs
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group %{_group} >/dev/null || /usr/sbin/groupadd -r %{_group}
/usr/bin/getent passwd %{_user} >/dev/null || /usr/sbin/useradd -r \
  -g %{_group} -d %{_prefix}/%{name} -s /bin/bash -c "Kafka" %{_user}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root)
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_conf_dir}/*
%{_prefix}/%{name}
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}
%doc NOTICE
%doc LICENSE

%changelog
* Thu Jul 25 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 2.3.0-1
- Initial release. Spec adopted from https://github.com/id/kafka-el7-rpm

