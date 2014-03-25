%define my_cnf "%{_sysconfdir}/my.cnf"

Name:		kaltura-mysql-config
Version:	1.0.0
Release:	1
Summary:	A wrapper that depends on the mysql-server package and makes Kaltura specific MySQL configurations.

Group: Server/Platform 
License:	AGPLv3+
URL:		http://www.kaltura.org	
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: mysql-server >= 5.1
Requires: chkconfig

%description
A wrapper that depends on the mysql-server package and makes Kaltura specific MySQL daemon configurations.
Sets MySQL daemon directives required for the Kaltura platform.

%post
# back it up as something that can be understood:
cp my_cnf my_cnf.%{name}-%{version}.rpm

sed -i '/^lower_case_table_names = 1$/d' my_cnf
sed -i '/^open_files_limit.*$/d' my_cnf
sed -i '/^max_allowed_packet.*$/d' my_cnf
sed -i 's@^\[mysqld\]$@[mysqld]\nlower_case_table_names = 1\n@' my_cnf
sed -i 's@^\[mysqld\]$@[mysqld]\ninnodb_file_per_table\n@' my_cnf
sed -i 's@^\[mysqld\]$@[mysqld]\ninnodb_log_file_size=32MB\n@' my_cnf
sed -i 's@^\[mysqld\]$@[mysqld]\nopen_files_limit = 20000\n@' my_cnf
sed -i 's@^\[mysqld\]$@[mysqld]\nmax_allowed_packet = 16M\n@' my_cnf

service mysqld restart
chkconfig mysqld on

%clean
rm -rf %{buildroot}

%changelog
* Thu Jan 2 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 1.0.0-1
- First package
