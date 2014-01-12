%define prefix /opt/kaltura
%define batch_confdir %{prefix}/app/configurations/batch/ 
%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define apache_user	apache
%define apache_group	apache
Summary: Kaltura Open Source Video Platform - batch server 
Name: kaltura-batch
Version: 9.7.0
Release: 13 
License: AGPLv3+
Group: Server/Platform 
#Source0: https://github.com/kaltura/server/archive/IX-%{version}.zip 
Source0: zz-%{name}.ini
Source1: kaltura-batch
Source2: kaltura-batch.conf
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-base, kaltura-ffmpeg, kaltura-ffmpeg-aux, php, curl, httpd, sox, ImageMagick, kaltura-sshpass, php-pecl-memcached, php-mcrypt,php-pecl-memcached,mediainfo, kaltura-segmenter
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
BuildArch: noarch

%description
Kaltura is the world's first Open Source Online Video Platform, transforming the way people work, 
learn, and entertain using online video. 
The Kaltura platform empowers media applications with advanced video management, publishing, 
and monetization tools that increase their reach and monetization and simplify their video operations. 
Kaltura improves productivity and interaction among millions of employees by providing enterprises 
powerful online video tools for boosting internal knowledge sharing, training, and collaboration, 
and for more effective marketing. Kaltura offers next generation learning for millions of students and 
teachers by providing educational institutions disruptive online video solutions for improved teaching,
learning, and increased engagement across campuses and beyond. 
For more information visit: http://corp.kaltura.com, http://www.kaltura.org and http://www.html5video.org.

This package sets up a node to be a batch server.


%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/php.d
mkdir -p $RPM_BUILD_ROOT/%{batch_confdir}
cp %{SOURCE0} $RPM_BUILD_ROOT/%{_sysconfdir}/php.d/zz-%{name}.ini
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/%{name}
sed 's#@WEB_DIR@#%{prefix}/web#' -i $RPM_BUILD_ROOT/%{_sysconfdir}/php.d/zz-%{name}.ini
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d


%clean
rm -rf %{buildroot}

%post
sed 's#@LOG_DIR@#%{prefix}/log#'  %{prefix}/app/configurations/monit.avail/batch.template.rc > %{prefix}/app/configurations/monit.avail/batch.rc
sed 's#@APP_DIR@#%{prefix}/app#' -i %{prefix}/app/configurations/monit.avail/batch.rc 
sed 's#@APP_DIR@#%{prefix}/app#' %{prefix}/app/configurations/monit.avail/httpd.template.rc > %{prefix}/app/configurations/monit.avail/httpd.rc 
sed 's#@APACHE_SERVICE@#httpd#g' -i %{prefix}/app/configurations/monit.avail/httpd.rc

ln -fs %{prefix}/app/configurations/monit.avail/httpd.rc %{prefix}/app/configurations/monit.d/httpd.rc
ln -fs %{prefix}/app/configurations/monit.avail/batch.rc %{prefix}/app/configurations/monit.d/batch.rc
if [ "$1" = 1 ];then
	/sbin/chkconfig --add kaltura-batch
echo"#####################################################################################################################################
Installation of %{name} %{version} completed
Please run: 
# %{prefix}/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
fi

# now replace tokens
sed 's#@WEB_DIR@#%{prefix}/web#' $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini.template > $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini
sed 's#@LOG_DIR@#%{prefix}/log#' -i  $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini
sed 's#@APP_DIR@{prefix}/app#' -i  $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini
sed 's#@BASE_DIR@#%{prefix}#' -i $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini
sed 's#@PHP_BIN@#%{_bindir}/php#' -i $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini
sed 's#@BIN_DIR@#%{prefix}/bin#' -i $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini
sed -i 's@^\(params.ImageMagickCmd\)\s*=.*@\1=%{bindir}/convert@' $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini
sed 's#@TMP_DIR@#%{prefix}/tmp#' -i $RPM_BUILD_ROOT/%{batch_confdir}/batch.ini
service httpd restart

chown %{kaltura_user}:%{kaltura_group} %{prefix}/log 
chown %{kaltura_user}:%{apache_group} %{prefix}/app/batch
chmod 775 %{prefix}/log
service kaltura-batch restart


%preun
if [ "$1" = 0 ] ; then
	/sbin/chkconfig --del kaltura-batch
	rm %{prefix}/app/configurations/monit.d/httpd.rc %{prefix}/app/configurations/monit.d/batch.rc || true
fi
service kaltura-batch restart

%postun
service httpd restart

%files
%config /etc/php.d/zz-%{name}.ini
%config %{_sysconfdir}/httpd/conf.d/kaltura-batch.conf

%{_sysconfdir}/init.d/%{name}


%changelog
* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-13
- Dedicated Apache config for a batch node.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-12
- Use the monit scandir mechanism.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-11
- Set correct path to 'convert' binary
- Replace TMP_DIR token.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-10
- Added dep on kaltura-segmenter.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-9
- Once again:(

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-7
- Wrong config path.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-6
- Handle Monit config tmplts

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-5
- [Re]start daemon.

* Fri Jan 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-3
- restart Apache at post and preun.

* Fri Jan 3 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-2
- Added chown on log and batch dir.

* Mon Dec 23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- First package.

