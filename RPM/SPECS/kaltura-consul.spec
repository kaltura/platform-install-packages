%define consul_user consul
%define consul_group consul

%define kaltura_prefix /opt/kaltura
%define prefix %{kaltura_prefix}/consul
Summary: Service Discovery and Configuration Made Easy
Name: kaltura-consul
Version: 1.0.6
Release: 2
BuildArch: x86_64
License: MPLv2.0 
Group: System Environment/Daemons
URL: http://consul.org/

Packager: Jess Portnoy <jess.portnoy@kaltura.com> 
Vendor: Kaltura, Inc.
Requires(pre): shadow-utils

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

Source: https://releases.hashicorp.com/consul/%{version}/consul_%{version}_linux_amd64.zip 
Source1: %{name}-server.service
Source2: %{name}-server.sysconf
Source3: %{name}-server.init
Source4: %{name}-client.service
Source5: %{name}-client.sysconf
Source6: %{name}-client.init
Source7: %{name}-server.json 
Source8: %{name}-client.json 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


%description
Consul makes it simple for services to register themselves 
and to discover other services via a DNS or HTTP interface.

This package provides the Consul daemon and configuration meant to be 
used with Kaltura Server.


#%prep
#%setup -qn .



%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/etc/consul.d/server $RPM_BUILD_ROOT%{prefix}/etc/consul.d/client
mkdir -p $RPM_BUILD_ROOT%{prefix}/var/data
mkdir -p $RPM_BUILD_ROOT%{prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{kaltura_prefix}/var/run/consul
mkdir -p $RPM_BUILD_ROOT%{kaltura_prefix}/log/consul
cp %{SOURCE7} $RPM_BUILD_ROOT%{prefix}/etc/consul.d/server/config.json
cp %{SOURCE8} $RPM_BUILD_ROOT%{prefix}/etc/consul.d/client/config.json
#cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/etc
cp consul $RPM_BUILD_ROOT%{prefix}/bin/

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE2} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}-server

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE5} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}-client


%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/%{name}-server.service
%{__install} -m644 %SOURCE4 \
        $RPM_BUILD_ROOT%{_unitdir}/%{name}-client.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE3} \
   $RPM_BUILD_ROOT%{_initrddir}/%{name}-server
%{__install} -m755 %{SOURCE6} \
   $RPM_BUILD_ROOT%{_initrddir}/%{name}-client
%endif


%clean
%{__rm} -rf %{buildroot}

%pre
#set -x
mkdir -p %{prefix}
# create user/group, and update permissions
getent group %{consul_group} >/dev/null || groupadd -r %{consul_group}  2>/dev/null
getent passwd %{consul_user} >/dev/null || useradd -m -r -d %{prefix} -s /sbin/nologin -c "Consul" -g %{consul_group} %{consul_user} 2>/dev/null
#set +x

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable %{name}-server.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop %{name}-server.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl --no-reload disable %{name}-client.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop %{name}-client.service >/dev/null 2>&1 ||:
%else
    /sbin/service %{name}-server stop > /dev/null 2>&1
    /sbin/service %{name}-client stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}-server
    /sbin/chkconfig --del %{name}-client
%endif
fi

%post
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset %{name}-server.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl preset %{name}-client.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add %{name}-server
    /sbin/chkconfig --add %{name}-client
%endif
fi

%postun 
%if %use_systemd
	/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif


%files
%defattr(-, root, root, 0755)
%{_sysconfdir}/sysconfig/%{name}-server
%{_sysconfdir}/sysconfig/%{name}-client
%if %{use_systemd}
%{_unitdir}/%{name}-server.service
%{_unitdir}/%{name}-client.service
%else
%{_initrddir}/%{name}-server
%{_initrddir}/%{name}-client
%endif
%{prefix}
%config(noreplace) %{prefix}/etc/consul.d/server/config.json
%config(noreplace) %{prefix}/etc/consul.d/client/config.json
%defattr(-, %{consul_user}, %{consul_group}, 0755)
%{kaltura_prefix}/var/run/consul
%{kaltura_prefix}/log/consul
%{prefix}/var/data




%changelog
* Thu Feb 22 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.6-1
- First release
