#
# spec file for sphinx 
#

%define sphinx_user kaltura
%define sphinx_group kaltura
%define prefix	/opt/kaltura/sphinx
# this isn't really a stand location for placing conf files but we wish to remain compatible with the current config dir tree used by Kaltura
%define confdir	/opt/kaltura/app/configurations/sphinx

Name:           kaltura-sphinx
Version:        2.2.1
Release:        1%{?dist}
Summary:        Sphinx full-text search server - for Kaltura

Group:          Applications/Text
License:        GPLv2
URL:            http://sphinxsearch.com
Vendor:         Sphinx Technologies Inc.
Packager:       Kaltura Inc.

Source0:       	%{name}-%{version}.tar.gz 
Source1:        %{name}.init
Source2:	http://snowball.tartarus.org/dist/libstemmer_c.tgz
Source3:	re2.tar.gz
Source4:	kaltura.conf.template
Patch0:		config-main.patch
Patch1:		config.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

BuildRequires:  mysql-devel
BuildRequires:	expat-devel

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires: mysql-libs zlib openssl expat libgcc krb5-libs, kaltura-base


%description
Sphinx is a full-text search server that adds many advanced features
on top of plain old text searching. Data can be fetched directly from
a database, or streamed in XML format. MySQL, PostgreSQL, SQL Server,
Oracle, and other databases are supported. Client programs can query
Sphinx either using native SphinxAPI library, or using regular MySQL
client programs and libraries via SQL-like SphinxQL interface.


%prep
%setup -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%setup -D -T -a 2 -n %{name}-%{version}
%setup -D -T -a 3 -n %{name}-%{version}

# Fix wrong-file-end-of-line-encoding
sed -i 's/\r//' api/ruby/spec/sphinx/sphinx_test.sql
sed -i 's/\r//' api/java/mk.cmd
sed -i 's/\r//' api/ruby/spec/fixtures/keywords.php
sed -i 's/\r//' api/ruby/lib/sphinx/response.rb


%build

%configure --sysconfdir=/opt/kaltura/app/configurations/sphinx  --with-mysql --with-libstemmer --with-unixodbc --with-iconv --enable-id64 --with-syslog --prefix=/opt/kaltura/sphinx-%{version} --mandir=/opt/kaltura/sphinx-%{version}/share/man --bindir=/opt/kaltura/sphinx-%{version}/bin
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p -c"
mkdir $RPM_BUILD_ROOT/opt/kaltura/sphinx-%{version}/lib
#mv $RPM_BUILD_ROOT/usr/local/lib/libre2* $RPM_BUILD_ROOT/opt/kaltura/sphinx/lib
# Install sphinx initscript
install -p -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/kaltura-sphinx

# Create /var/log/sphinx
mkdir -p $RPM_BUILD_ROOT%{prefix}-%{version}/log/sphinx

# Create /var/run/sphinx
mkdir -p $RPM_BUILD_ROOT%{prefix}-%{version}/run/sphinx

# Create /var/lib/sphinx
mkdir -p $RPM_BUILD_ROOT%{prefix}-%{version}/lib/sphinx

# Create sphinx.conf
install -p -D -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{confdir}/kaltura_sphinx.conf.template

# Copy the test suite

# Create /etc/logrotate.d/sphinx
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sphinx << EOF
/var/log/sphinx/*.log {
       weekly
       rotate 10
       copytruncate
       delaycompress
       compress
       notifempty
       missingok
}
EOF

mkdir $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kaltura_sphinx.sh << EOF
PATH=$PATH:%{prefix}-%{version}/bin
export PATH
EOF

%clean
rm -rf $RPM_BUILD_ROOT


%post
ldconfig
# register service
if [ "$1" = 1 ];
then
    /sbin/chkconfig --add kaltura-sphinx
fi

# create user/group, and update permissions
chown -R %{sphinx_user}:%{sphinx_group} %{prefix}-%{version}/var/lib/sphinx %{prefix}-%{version}/var/log/sphinx %{prefix}-%{version}/var/run/sphinx

# print some further pointers
echo
echo "Sphinx installed!"
echo "Now create a full-text index, start the search daemon, and you're all set."
echo
echo "To manage indexes:"
echo "    editor %{_sysconfdir}/sphinx/sphinx.conf"
echo
echo "To rebuild all disk indexes:"
echo "    sudo -u sphinx indexer --all --rotate"
echo
echo "To start/stop search daemon:"
echo "    service kaltura-sphinx start/stop"
echo
echo "To query search daemon using MySQL client:"
echo "    mysql -h 0 -P 9306"
echo "    mysql> SELECT * FROM test1 WHERE MATCH('test');"
echo
echo "See the manual at /usr/share/doc/sphinx-%{version} for details."
echo
echo "For commercial support please contact Sphinx Technologies Inc at"
echo "http://sphinxsearch.com/contacts.html"
echo




%preun
if [ "$1" = 0 ] ; then
    /sbin/service kaltura-sphinx stop >/dev/null 2>&1
    /sbin/chkconfig --del kaltura-sphinx
fi


%files
%defattr(-,root,root,-)
%{prefix}-%{version}/share/man/man1/*
%doc COPYING doc/sphinx.html doc/sphinx.txt sphinx-min.conf.dist sphinx.conf.dist example.sql
%dir %{confdir}
#%config(missingok) %{confdir}/kaltura_sphinx.conf
%config %{_sysconfdir}/profile.d/kaltura_sphinx.sh
%exclude %{confdir}/*.conf.dist
%exclude %{confdir}/example.sql
%{_initrddir}/kaltura-sphinx
%config(noreplace) %{_sysconfdir}/logrotate.d/sphinx
%{prefix}-%{version}/bin/*
%dir %{prefix}-%{version}/log/sphinx
%dir %{prefix}-%{version}/run/sphinx
#%exclude %{prefix}-%{version}/libstemmer_c/include



%changelog
* Tue Dec 24 2013 Jess Portnoy <jess.portnoy@kaltura.com> 2.2.1.r4097-1
First build.
