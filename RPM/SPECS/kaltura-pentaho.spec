%define prefix /opt/kaltura/pentaho 

%define kaltura_user	kaltura
%define kaltura_group	kaltura

Name:		kaltura-pentaho
Version:	4.2.1
Release:	2
Summary:	Pentaho Open Source Suite Data Integration Community Edition (CE).
Group:		System Management
License:	LGPLv2+
URL:		http://wiki.pentaho.org	
Source0:	http://sourceforge.net/projects/pentaho/files/Data%20Integration/%{version}-stable/pdi-ce-%{version}-stable.tar.gz
# http://download.softagency.net/MySQL/Downloads/Connector-J/mysql-connector-java-5.1.35.tar.gz
Source1: 	mysql-connector-java-5.1.35-bin.jar
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#BuildArch: 	noarch

Requires:	jre >= 1.7.0

%description
Pentaho Open Source Data Integration Community Edition (CE).

%prep
%setup -qn data-integration 


%build


%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/pdi
cp -r * $RPM_BUILD_ROOT%{prefix}/pdi
rm $RPM_BUILD_ROOT%{prefix}/pdi/libext/JDBC/mysql-connector-java-5.1.17.jar
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/pdi/libext/JDBC

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc docs README_INFOBRIGHT.txt README_LINUX.txt 
%defattr(-, %{kaltura_user}, %{kaltura_group} , 0755)
%{prefix}/pdi/*


%changelog
* Sun Jun 21 2015 Jess Portnoy <jess.portnoy@kaltura.com> - 4.2.1-2
- Use newer mysql-connector-java - needed for MySQL 5.6 integration.

* Wed Jan 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 4.2.1-1
- First package
