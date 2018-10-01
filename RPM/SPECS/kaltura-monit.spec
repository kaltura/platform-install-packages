%define prefix /opt/kaltura/
# this isn't really a stand location for placing conf files but we wish to remain compatible with the current config dir tree used by Kaltura
%define confdir /opt/kaltura/app/configurations/monit
%define logmsg logger -t %{name}/rpm
# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

Summary: Process monitor and restart utility
Name: kaltura-monit
Version: 5.25.2
Release: 2
License: GPLv3
Group: High Availability Management 
URL: http://mmonit.com/monit/

Packager: Jess Portnoy <jess.portnoy@kaltura.com>

Source0: http://mmonit.com/monit/dist/monit-%{version}.tar.gz
Source1: kaltura-monit
Source2: monit.template.conf
%if %{use_systemd}
Source3: %{name}.service
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: binutils
BuildRequires: byacc
BuildRequires: flex
BuildRequires: openssl-devel
BuildRequires: /usr/bin/logger
BuildRequires: pam-devel 
BuildRequires: chkconfig 
BuildRequires: initscripts 
%if %{use_systemd}
BuildRequires: systemd
%endif

%description
Monit is an utility for monitoring daemons or similar programs running on
a Unix system. It will start specified programs if they are not running
and restart programs not responding.

%prep
%setup -qn monit-%{version}

sed -i 's@\bmonitrc\b@monit.conf@' src/monit.h
sed -i 's@^#\s+\(include .*\)$@\1@' monitrc

# store id and state files in /var/monit
sed -i 's@^#\(\s+\)set \(id|state\)file /var/\.monit\.\(id|state\)$@set $2file /var/monit/$3@' monitrc


%build
./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --target=x86_64-redhat-linux-gnu --prefix=%{prefix} --bindir=%{prefix}/bin --sbindir=%{prefix}/sbin --sysconfdir=%{confdir} --datadir=%{prefix}/share --includedir=%{prefix}/include --libdir=%{prefix}/lib64 --libexecdir=%{prefix}/libexec --localstatedir=%{prefix}/var --sharedstatedir=%{prefix}/var/lib --mandir=%{prefix}/share/man --infodir=%{prefix}/share/info --with-ssl-lib-dir=/usr/lib64/openssl
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p -c"

#%{__install} -Dp -m0755 system/startup/rc.monit %{buildroot}%{_initrddir}/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
%{__install} -Dp -m0644 system/bash/monit %{buildroot}%{_sysconfdir}/bash_completion.d/
%{__install} -Dp -m0600 %{SOURCE2} %{buildroot}%{confdir}/monit.template.conf

%{__install} -d -m0755 %{buildroot}%{confdir}/monit.d/
%{__install} -d -m0755 %{buildroot}%{prefix}/var/lib/monit/

# create folder where state and id are stored
%{__install} -d -m0755 %{buildroot}%{prefix}/var/monit/
%if %{use_systemd}
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE3 \
        $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%endif
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE1} \
   $RPM_BUILD_ROOT%{_initrddir}/%{name}

%pre
if ! /usr/bin/id monit &>/dev/null; then
	/usr/sbin/useradd -M -r -d %{prefix}/var/lib/monit -s /bin/sh -c "monit daemon" monit || \
		%logmsg "Unexpected error adding user \"monit\". Aborting installation."
fi

%post
if [ "$1" -eq 1 ];then
%if %{use_systemd}
	#/usr/bin/systemctl preset %{name}.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl enable %{name}.service >/dev/null 2>&1 ||:
%else
	/sbin/chkconfig --add %{name}
	/sbin/chkconfig %{name} on
%endif
fi
/sbin/service monit restart &>/dev/null || :


%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
	/usr/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl stop %{name}.service >/dev/null 2>&1 ||:
%else
	service %{name} stop &>/dev/null || :
	/sbin/chkconfig --del %{name}
%endif
fi

%postun
%if %use_systemd
	/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
/sbin/service monit condrestart &>/dev/null || :
if [ $1 -eq 0 ]; then
	/usr/sbin/userdel monit || %logmsg "User \"monit\" could not be deleted."
fi

%clean
%{__rm} -rf %{buildroot}


%files
%doc COPYING README* CONTRIBUTORS
%doc %{prefix}/share/man/man?/*
%defattr(-, root, root, 0755)
%if %{use_systemd}
%{_unitdir}/%{name}.service
%endif
%{_initrddir}/%{name}
%config %{confdir}/monit.d/
%defattr(-, root, root, 0600)
%config %{confdir}/monit.template.conf
%config %{prefix}/var/monit/
%config %{_sysconfdir}/bash_completion.d/monit
%{prefix}/var/lib/monit/
%attr(0755, root, root) %{prefix}/bin/monit
#%attr(0600, root, root) %config(noreplace) %{confdir}/monit.conf

%changelog
* Mon Oct 1 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 5.25.2-2
- Added bash completion file

* Mon Oct 1 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 5.25.2-1
- New upstream version [https://mmonit.com/monit/changes]
- Log monit events to a dedicated log rather than syslog

* Tue Feb 27 2018 Jess Portnoy <jess.portnoy@kaltura.com> - 5.25.1-2
- New upstream version [https://mmonit.com/monit/changes]
- Bind HTTP daemon to loopback

* Tue Aug 29 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 5.23.0-2
- Added set mailserver 127.0.0.1 to monit.conf

* Tue Aug 1 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 5.23.0-1
- New Upstream Release, see: https://mmonit.com/monit/changes

* Mon May 22 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 5.21.0-2
- Added systemd config

* Tue Apr 18 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 5.21.0-1
- https://bitbucket.org/tildeslash/monit/commits/tag/release-5-21-0

* Thu Sep 22 2016 David Bezemer <david.bezemer@kaltura.com> - 5.19.0-1
- New Upstream Release, see: https://mmonit.com/monit/changes

* Wed Jun 22 2016 Jess Portnoy <jess.portnoy@kaltura.com> - 5.18-1
- New Upstream Release, see: https://mmonit.com/monit/changes

* Thu May 8 2015 David Bezemer <david.bezemer@kaltura.com> - 5.13-1
- New Upstream Release 5.13
- Adding MMonit support

* Thu Mar 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-13
- Generate random monit passwd.

* Thu Mar 13 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-12
- Placeholders instead of hard coded host and path to APP_DIR.
- Commented section about setting up monit over SSL.

* Mon Feb 17 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-11
- Fix for https://github.com/kaltura/platform-install-packages/issues/41

* Sun Feb 16 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-10
- monit.conf needs to be templated because of the email addr.

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-9
- monit.conf: set daemon 10 # Poll every 10 seconds

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-8
- Changed monit confdir.

* Sat Feb 15 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-7
- chkconfig monit on.
- Modications to the init script.

* Sun Jan 12 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-5
- Added monit.conf

* Sun Jan 12 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-4
- Changes to init script.

* Sun Jan 12 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-3
- Only chkconfig on first install.

* Thu Jan 2 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-2
- Corrected daemon name to be 'kaltura-monit'

* Thu Jan 2 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 5.6-1
- This package was originally taken from the Dag repo.
- The reason for creating kaltura-monit
	0. none standard prefix so that one can also install the original monit package if one is inclined or needs it for other packages.
	1. the monit package is not an official RHEL/CentOS package and we wish to avoid forcing the user into adding additional repos.

* Mon Dec 17 2012 David Hrbáč <david@hrbac.cz> - 5.5-1
- new upstream release

* Mon May 28 2012 David Hrbáč <david@hrbac.cz> - 5.4-1
- new upstream release

* Tue Apr 17 2012 Derek Tamsen <dtamsen@gmail.com> - 5.3.2-3
- Fixed monitor.h source path so it can be patched to reference /etc/monit.conf instead of /etc/monitrc
- Updated /etc/init.d/monit so config path is /etc/monit.conf
- Added /var/monit so the state and id files can be create upon monit startup
- Updated post section to move /etc/monitrc to /etc/monit.conf for os standardization

* Mon Jan 23 2012 David Hrbáč <david@hrbac.cz> - 5.3.2-2
- use upstream configuration file location

* Tue Jan 17 2012 David Hrbáč <david@hrbac.cz> - 5.3.2-1
- new upstream release

* Mon Apr 04 2011 David Hrbáč <david@hrbac.cz> - 5.2.5-1
- new upstream release

* Tue Feb 22 2011 David Hrbáč <david@hrbac.cz> - 5.2.4-1
- new upstream release

* Tue Nov 30 2010 Steve Huff <shuff@vecna.org> - 5.2.3-1
- Updated to release 5.2.3.

* Thu Sep 23 2010 Steve Huff <shuff@vecna.org> - 5.2-1
- Updated to release 5.2.

* Mon Apr 12 2010 Chris Butler <rf@crustynet.org.uk> - 5.1.1-1
- Updated to release 5.1.1

* Tue Dec 8 2009 Yury V. Zaytsev <yury@shurup.com> - 5.0.3-2
- Committed to RPMForge.

* Mon Nov 16 2009 Justin Shepherd <jshepher@rackspace.com> - 5.0.3-1
- Updated to release 5.0.3.
- Using the provided monit init script.

* Sat Apr 18 2009 Dries Verachtert <dries@ulyssis.org> - 5.0-1
- Updated to release 5.0.

* Mon Jun 18 2007 Dag Wieers <dag@wieers.com> - 4.9-2
- Enable the use of /etc/monit.d/ in the config-file. (Oren Held)

* Tue Feb 20 2007 Dag Wieers <dag@wieers.com> - 4.9-1
- Updated to release 4.9.

* Tue Jun 13 2006 Dag Wieers <dag@wieers.com> - 4.8.1-4
- Fixed type in %%preun that failed to stop monit. (Jim Robinson)

* Mon May 29 2006 Dag Wieers <dag@wieers.com> - 4.8.1-3
- Fixed reference to monitrc from monitor.h. (Tim Jackson)

* Thu May 18 2006 Dag Wieers <dag@wieers.com> - 4.8.1-2
- Fixed the nagios references in the monit user creation. (Tim Jackson)
- Removed the -o option to useradd. (Tim Jackson)

* Wed May 17 2006 Dag Wieers <dag@wieers.com> - 4.8.1-1
- Updated to release 4.8.1.
- Added /opt/kaltura/app/configurations/monit.d/ and /opt/kaltura/app/monit/lib/monit/. (Michael C. Hoffman)
- Creation/removal of user monit. (Michael C. Hoffman)

* Mon May 08 2006 Dag Wieers <dag@wieers.com> - 4.8-1
- Updated to release 4.8.

* Thu Jan 12 2006 Dag Wieers <dag@wieers.com> - 4.7-1
- Updated to release 4.7.

* Fri Sep 24 2004 Dag Wieers <dag@wieers.com> - 4.4-1
- Updated to release 4.4.

* Thu May 13 2004 Dag Wieers <dag@wieers.com> - 4.3-1
- Updated to release 4.3.

* Mon Apr 05 2004 Dag Wieers <dag@wieers.com> - 4.2.1-1
- Updated to release 4.2.1.

* Fri Mar 26 2004 Dag Wieers <dag@wieers.com> - 4.2.0-0
- Updated to release 4.2.0.

* Sun Nov 23 2003 Dag Wieers <dag@wieers.com> - 4.1.1-0
- Updated to release 4.1.1.

* Mon Oct 13 2003 Dag Wieers <dag@wieers.com> - 4.0-0
- Initial package. (using DAR)
