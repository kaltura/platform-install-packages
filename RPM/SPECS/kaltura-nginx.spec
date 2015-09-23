#
%define nginx_home %{_localstatedir}/cache/nginx
%define nginx_user kaltura
%define nginx_group kaltura

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 5
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl
BuildRequires: openssl-devel
%endif

%if 0%{?rhel}  == 6
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%define with_spdy 1
%endif

%if 0%{?rhel}  == 7
Group: System Environment/Daemons
Requires(pre): shadow-utils
Requires: systemd
Requires: openssl >= 1.0.1
BuildRequires: systemd
BuildRequires: openssl-devel >= 1.0.1
Epoch: 1
%define with_spdy 1
%endif

%if 0%{?suse_version}
Group: Productivity/Networking/Web/Servers
BuildRequires: libopenssl-devel
Requires(pre): pwdutils
%endif

%define nginx_vod_module_ver 1.2
%define nginx_secure_token_ver 1.0.1
%define nginx_token_validate_ver 1.0.1
%define nginx_vts_ver 0.1.2
# end of distribution specific definitions

Summary: High performance web server customized for Kaltura VOD
Name: kaltura-nginx
Version: 1.8.0
Release: 6
Vendor: Kaltura inc.
URL: http://nginx.org/

Source0: %{name}-%{version}.tar.gz
Source1: nginx.logrotate
Source2: nginx.init
Source3: nginx.sysconf
Source4: nginx.conf
Source5: nginx.vh.default.conf
Source6: nginx.vh.example_ssl.conf
Source7: nginx.suse.init
Source8: nginx.service
Source9: nginx.upgrade.sh
Source10: nginx-vod-module-%{nginx_vod_module_ver}.zip  
Source11: nginx-secure-token-module-%{nginx_secure_token_ver}.zip
Source12: nginx-akamai-token-validate-module-%{nginx_token_validate_ver}.zip
Source13: nginx-module-vts-v%{nginx_vts_ver}.zip
#Patch1: nginx_kaltura.diff 

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel

Provides: webserver
Conflicts: nginx

%description
nginx [engine x] is an HTTP and reverse proxy server, as well as
a mail proxy server.
This is a custom Nginx build for the Kaltura VOD module.
Please see: https://github.com/kaltura/nginx-vod-module for more info.

%package debug
Summary: debug version of nginx
Group: System Environment/Daemons
Requires: kaltura-nginx, kaltura-postinst
%description debug
Not stripped version of nginx built with the debugging log support.

%prep
%setup -qn nginx-%{version}
#%patch1 -p1 -b ngx_http_upstream.c.orig 
unzip -o %{SOURCE10}

unzip -o %{SOURCE11}

unzip -o %{SOURCE12}

unzip -o %{SOURCE13}


%build
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        --with-debug \
        %{?with_spdy:--with-http_spdy_module} \
	--with-threads \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
	--add-module=./nginx-vod-module-%{nginx_vod_module_ver} \
	--add-module=./nginx-secure-token-module-%{nginx_secure_token_ver} \
	--add-module=./nginx-akamai-token-validate-module-%{nginx_token_validate_ver} \
	--add-module=./nginx-module-vts-%{nginx_vts_ver} \
        $*
make %{?_smp_mflags}
%{__mv} %{_builddir}/nginx-%{version}/objs/nginx \
        %{_builddir}/nginx-%{version}/objs/nginx.debug
./configure \
        --prefix=%{_sysconfdir}/nginx \
        --sbin-path=%{_sbindir}/nginx \
        --conf-path=%{_sysconfdir}/nginx/nginx.conf \
        --error-log-path=%{_localstatedir}/log/nginx/error.log \
        --http-log-path=%{_localstatedir}/log/nginx/access.log \
        --pid-path=%{_localstatedir}/run/nginx.pid \
        --lock-path=%{_localstatedir}/run/nginx.lock \
        --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp \
        --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp \
        --user=%{nginx_user} \
        --group=%{nginx_group} \
        --with-http_ssl_module \
        --with-http_realip_module \
        --with-http_addition_module \
        --with-http_sub_module \
        --with-http_dav_module \
        --with-http_flv_module \
        --with-http_mp4_module \
        --with-http_gunzip_module \
        --with-http_gzip_static_module \
        --with-http_random_index_module \
        --with-http_secure_link_module \
        --with-http_stub_status_module \
        --with-http_auth_request_module \
        --with-mail \
        --with-mail_ssl_module \
        --with-file-aio \
        --with-ipv6 \
        %{?with_spdy:--with-http_spdy_module} \
	--with-threads \
        --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
	--add-module=./nginx-vod-module-%{nginx_vod_module_ver} \
	--add-module=./nginx-secure-token-module-%{nginx_secure_token_ver} \
	--add-module=./nginx-akamai-token-validate-module-%{nginx_token_validate_ver} \
	--add-module=./nginx-module-vts-%{nginx_vts_ver} \
        $*
make %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/nginx
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/html $RPM_BUILD_ROOT%{_datadir}/nginx/

%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/*.default
%{__rm} -f $RPM_BUILD_ROOT%{_sysconfdir}/nginx/fastcgi.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/nginx
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/nginx

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{SOURCE4} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/nginx.conf
%{__install} -m 644 -p %{_builddir}/nginx-%{version}/nginx-vod-module-%{nginx_vod_module_ver}/conf/kaltura.conf.template \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/kaltura.conf.template
%{__install} -m 644 -p %{SOURCE6} \
   $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/example_ssl.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/nginx

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE8 \
        $RPM_BUILD_ROOT%{_unitdir}/kaltura-nginx.service
%{__mkdir} -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx
%{__install} -m755 %SOURCE9 \
        $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%if 0%{?suse_version}
%{__install} -m755 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_initrddir}/kaltura-nginx
%else
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/kaltura-nginx
%endif
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/nginx
%{__install} -m644 %{_builddir}/nginx-%{version}/objs/nginx.debug \
   $RPM_BUILD_ROOT%{_sbindir}/nginx.debug

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%{_sbindir}/nginx

%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d

%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config %{_sysconfdir}/nginx/conf.d/kaltura.conf.template
%config(noreplace) %{_sysconfdir}/nginx/conf.d/example_ssl.conf
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%config(noreplace) %{_sysconfdir}/nginx/win-utf

%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%config(noreplace) %{_sysconfdir}/sysconfig/nginx
%if %{use_systemd}
%{_unitdir}/kaltura-nginx.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/kaltura-nginx
%endif

%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*

%attr(0755,root,root) %dir %{_localstatedir}/cache/nginx
%attr(0755,root,root) %dir %{_localstatedir}/log/nginx

%files debug
%attr(0755,root,root) %{_sbindir}/nginx.debug

%pre
# Add the "nginx" user
#getent group %{nginx_group} >/dev/null || groupadd -r %{nginx_group}
#getent passwd %{nginx_user} >/dev/null || \
#    useradd -r -g %{nginx_group} -s /sbin/nologin \
#    -d %{nginx_home} -c "nginx user"  %{nginx_user}
#exit 0
if ! id -u %{nginx_user} >>/dev/null 2>&1 ;then
	groupadd -r %{nginx_group} -g7373 2>/dev/null || true
	useradd -M -r -u7373 -d %{prefix} -s /bin/bash -c "Kaltura server" -g %{nginx_group} %{nginx_user} 2>/dev/null || true
fi

%post
# Register the nginx service
if [ $1 -eq 1 ]; then
%if %{use_systemd}
    /usr/bin/systemctl preset nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/chkconfig --add kaltura-nginx
%endif
    # print site info
    cat <<BANNER
----------------------------------------------------------------------

Thanks for using nginx!

Please find the official documentation for nginx here:
* http://nginx.org/en/docs/

Commercial subscriptions for nginx are available on:
* http://nginx.com/products/

----------------------------------------------------------------------
BANNER

    # Touch and set permisions on default log files on installation

    if [ -d %{_localstatedir}/log/nginx ]; then
        if [ ! -e %{_localstatedir}/log/nginx/access.log ]; then
            touch %{_localstatedir}/log/nginx/access.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/access.log
            %{__chown} %{nginx_user}:adm %{_localstatedir}/log/nginx/access.log
        fi

        if [ ! -e %{_localstatedir}/log/nginx/error.log ]; then
            touch %{_localstatedir}/log/nginx/error.log
            %{__chmod} 640 %{_localstatedir}/log/nginx/error.log
            %{__chown} %{nginx_user}:adm %{_localstatedir}/log/nginx/error.log
        fi
    fi
fi

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
    /usr/bin/systemctl --no-reload disable kaltura-nginx.service >/dev/null 2>&1 ||:
    /usr/bin/systemctl stop kaltura-nginx.service >/dev/null 2>&1 ||:
%else
    /sbin/service kaltura-nginx stop > /dev/null 2>&1
    /sbin/chkconfig --del kaltura-nginx
%endif
fi

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
    /sbin/service kaltura-nginx status  >/dev/null 2>&1 || exit 0
    /sbin/service kaltura-nginx upgrade >/dev/null 2>&1 || echo \
        "Binary upgrade failed, please check nginx's error.log"
fi
%changelog
* Wed Sep 23 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.8.0-6
- With VTS v0.1.2 - https://github.com/vozlt/nginx-module-vts/issues/19

* Mon Sep 21 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.8.0-5
- nginx-vod-module tag 1.2
- disabled vts until https://github.com/vozlt/nginx-module-vts/commit/47b07ac42c8f9f895774318e7d117bb2dbf88403 is included in a new tag

* Sun May 31 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.8.0-4
- VTS module now tagged.

* Wed May 13 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.8.0-3
- nginx-vod-module tag 1.1

* Tue May 12 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.8.0-2
- Now with the VTS module from https://github.com/vozlt/nginx-module-vts

* Thu Apr 30 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.8.0-1
- Upgraded nginx to 1.8.0 and enabled threads. Needed by Ks new feature.
- See http://nginx.org/en/CHANGES-1.8 for changelog.

* Tue Apr 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.6.3-1
- 1.6.3 is now stable:
- Feature: now the "tcp_nodelay" directive works with SPDY connections.
- Bugfix: in error handling. Thanks to Yichun Zhang and Daniil Bondarev.
- Bugfix: alerts "header already sent" appeared in logs if the "post_action" directive was used; the bug had appeared in 1.5.4.
- Bugfix: alerts "sem_post() failed" might appear in logs.
- Bugfix: in hash table handling. Thanks to Chris West.
- Bugfix: in integer overflow handling. Thanks to Régis Leroy.

* Tue Apr 28 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.6.2-11
- Kaltura modules tag 1.0.1

* Tue Apr 14 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 1.6.2-8
- Kaltura Nginx modules are now tagged.

* Sun Dec 7 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.6.2-2
- Nginx precompiled with https://github.com/kaltura/nginx-vod-module

* Tue Sep 16 2014 Sergey Budnevitch <sb@nginx.com>
- epoch added to the EPEL7/CentOS7 spec to override EPEL one
- 1.6.2

* Tue Aug  5 2014 Sergey Budnevitch <sb@nginx.com>
- 1.6.1

* Sat Jul 12 2014 Sergey Budnevitch <sb@nginx.com>
- incorrect sysconfig filename finding in the initscript fixed

* Thu Apr 24 2014 Konstantin Pavlov <thresh@nginx.com>
- 1.6.0
- http-auth-request module added

* Tue Mar 18 2014 Sergey Budnevitch <sb@nginx.com>
- 1.4.7
- spec cleanup
- openssl version dependence added
- upgrade() function in the init script improved
- warning added when binary upgrade returns non-zero exit code

* Tue Mar  4 2014 Sergey Budnevitch <sb@nginx.com>
- 1.4.6

* Tue Feb 11 2014 Konstantin Pavlov <thresh@nginx.com>
- 1.4.5

* Tue Nov 19 2013 Sergey Budnevitch <sb@nginx.com>
- 1.4.4

* Tue Oct  8 2013 Sergey Budnevitch <sb@nginx.com>
- 1.4.3

* Wed Jul 17 2013 Sergey Budnevitch <sb@nginx.com>
- 1.4.2

* Mon May 6 2013 Sergey Budnevitch <sb@nginx.com>
- 1.4.1

* Wed Apr 24 2013 Sergey Budnevitch <sb@nginx.com>
- gunzip module added
- 1.4.0

* Tue Apr  2 2013 Sergey Budnevitch <sb@nginx.com>
- set permissions on default log files at installation
- 1.2.8

* Tue Feb 12 2013 Sergey Budnevitch <sb@nginx.com>
- excess slash removed from --prefix
- 1.2.7

* Tue Dec 11 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.6

* Tue Nov 13 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.5

* Tue Sep 25 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.4

* Tue Aug  7 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.3
- nginx-debug package now actually contains non stripped binary

* Tue Jul  3 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.2

* Tue Jun  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.1

* Mon Apr 23 2012 Sergey Budnevitch <sb@nginx.com>
- 1.2.0

* Thu Apr 12 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.15

* Thu Mar 15 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.14
- OpenSUSE init script and SuSE specific changes to spec file added

* Mon Mar  5 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.13

* Mon Feb  6 2012 Sergey Budnevitch <sb@nginx.com>
- 1.0.12
- banner added to install script

* Thu Dec 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.11
- init script enhancements (thanks to Gena Makhomed)
- one second sleep during upgrade replaced with 0.1 sec usleep

* Tue Nov 15 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.10

* Tue Nov  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.9
- nginx-debug package added

* Tue Oct 11 2011 Sergey Budnevitch <sb@nginx.com>
- spec file cleanup (thanks to Yury V. Zaytsev)
- log dir permitions fixed
- logrotate creates new logfiles with nginx owner
- "upgrade" argument to init-script added (based on fedora one)

* Sat Oct  1 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.8
- built with mp4 module

* Fri Sep 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.7

* Tue Aug 30 2011 Sergey Budnevitch <sb@nginx.com>
- 1.0.6
- replace "conf.d/*" config include with "conf.d/*.conf" in default nginx.conf

* Wed Aug 10 2011 Sergey Budnevitch
- Initial release
