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


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc docs README_INFOBRIGHT.txt README_LINUX.txt 
%defattr(-, %{kaltura_user}, %{kaltura_group} , 0755)
%{prefix}/pdi/*


%changelog
* Wed Jan 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 4.2.1-1
- First package
