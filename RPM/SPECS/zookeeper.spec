%define __jar_repack 0
%define debug_package %{nil}
%define name         zookeeper
%define _prefix      /opt
%define _conf_dir    %{_sysconfdir}/%{name}
%define _log_dir     %{_var}/log/%{name}
%define _data_dir    %{_sharedstatedir}/%{name}

Summary: ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.
Name: zookeeper
Version: 3.4.10
Release: 1
License: Apache License, Version 2.0
Group: Applications/Databases
URL: http://zookeper.apache.org/
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.service
Source2: %{name}.logrotate
Source3: zoo.cfg
Source4: %{name}.log4j.properties
Source5: %{name}.log4j-cli.properties
Source6: %{name}.sysconfig
Source7: %{name}.zkcli
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}
Vendor: Apache Software Foundation
Packager: Ivan Dyachkov <ivan.dyachkov@klarna.com>
Provides: %{name}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or another by distributed applications. Each time they are implemented there is a lot of work that goes into fixing the bugs and race conditions that are inevitable. Because of the difficulty of implementing these kinds of services, applications initially usually skimp on them ,which make them brittle in the presence of change and difficult to manage. Even when done correctly, different implementations of these services lead to management complexity when the applications are deployed.

%prep
%setup -q

%build

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/zookeeper
mkdir -p $RPM_BUILD_ROOT%{_log_dir}
mkdir -p $RPM_BUILD_ROOT%{_data_dir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service.d
mkdir -p $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 zookeeper-%{version}.jar $RPM_BUILD_ROOT%{_prefix}/zookeeper/
install -p -D -m 644 lib/*.jar $RPM_BUILD_ROOT%{_prefix}/zookeeper/
install -p -D -m 755 %{S:1} $RPM_BUILD_ROOT%{_unitdir}/
install -p -D -m 644 %{S:2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zookeeper
install -p -D -m 644 %{S:3} $RPM_BUILD_ROOT%{_conf_dir}/
install -p -D -m 644 %{S:4} $RPM_BUILD_ROOT%{_conf_dir}/log4j.properties
install -p -D -m 644 %{S:5} $RPM_BUILD_ROOT%{_conf_dir}/log4j-cli.properties
install -p -D -m 644 %{S:6} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/zookeeper
install -p -D -m 755 %{S:7} $RPM_BUILD_ROOT%{_bindir}/zkcli
install -p -D -m 644 conf/configuration.xsl $RPM_BUILD_ROOT%{_conf_dir}/
# stupid systemd fails to expand file paths in runtime
CLASSPATH=
for i in $RPM_BUILD_ROOT%{_prefix}/zookeeper/*.jar
do
  CLASSPATH="%{_prefix}/zookeeper/$(basename ${i}):${CLASSPATH}"
done
echo "[Service]" > $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service.d/classpath.conf
echo "Environment=CLASSPATH=${CLASSPATH}" >> $RPM_BUILD_ROOT%{_unitdir}/zookeeper.service.d/classpath.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/bin/getent group zookeeper >/dev/null || /usr/sbin/groupadd -r zookeeper
if ! /usr/bin/getent passwd zookeeper >/dev/null ; then
    /usr/sbin/useradd -r -g zookeeper -m -d %{_prefix}/zookeeper -s /bin/bash -c "Zookeeper" zookeeper
fi

%post
%systemd_post zookeeper.service

%preun
%systemd_preun zookeeper.service

%postun
# When the last version of a package is erased, $1 is 0
# Otherwise it's an upgrade and we need to restart the service
if [ $1 -ge 1 ]; then
    /usr/bin/systemctl restart zookeeper.service
fi
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%{_unitdir}/zookeeper.service
%{_unitdir}/zookeeper.service.d/classpath.conf
/usr/local/bin/zkcli
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%config(noreplace) %{_sysconfdir}/sysconfig/zookeeper
%config(noreplace) %{_conf_dir}/*
%attr(-,zookeeper,zookeeper) %{_prefix}/zookeeper
%attr(0755,zookeeper,zookeeper) %dir %{_log_dir}
%attr(0700,zookeeper,zookeeper) %dir %{_data_dir}

%changelog

* Tue Jul 23 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 3.4.10-1
- Initial release. Spec adopted from https://github.com/id/zookeeper-el7-rpm

