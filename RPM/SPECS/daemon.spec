Summary: daemon - turns other processes into daemons
Name: daemon
Version: 0.6.4
Release: 1
Group: System Environment/Daemons
Source: http://libslack.org/daemon/download/daemon-0.6.4.tar.gz
URL: http://libslack.org/daemon/
License: GPL
%description
Daemon turns other processes into daemons. There are many tasks that need to
be performed to correctly set up a daemon process. This can be tedious.
Daemon performs these tasks for other processes. This is useful for writing
daemons in languages other than C, C++ or Perl (e.g. /bin/sh, Java).

If you want to write daemons in languages that can link against C functions
(e.g. C, C++), see libslack which contains the core functionality of daemon.

%prep
%setup -q
%build
make
%install
make PREFIX="${RPM_BUILD_ROOT}%_prefix" install-daemon
%files
%_bindir/daemon
%doc %_mandir/man1/daemon.1.gz
%doc %_mandir/man5/daemon.conf.5.gz
