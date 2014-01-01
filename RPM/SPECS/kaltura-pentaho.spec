%define prefix /usr/local/pentaho 

Name:		kaltura-pentaho
Version:	4.2.1
Release:	1
Summary:	Pentaho Open Source Suite Data Integration Community Edition (CE).
Group:		System Management
License:	LGPLv2+
URL:		http://wiki.pentaho.org	
Source0:	http://sourceforge.net/projects/pentaho/files/Data%20Integration/%{version}-stable/pdi-ce-%{version}-stable.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: 	noarch

Requires:	java

%description
Pentaho Open Source Data Integration Community Edition (CE).

%prep
%setup -qn data-integration 


%build


%install


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc



%changelog
* Wed Jan 1 2014 Jess Portnoy <jess.portnoy@kaltura.com> - 4.2.1-1
- First package
