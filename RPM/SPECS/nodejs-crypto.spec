%global npm_name crypto
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.0.3
Release: 1
Summary: JavaScript implementations of standard and secure cryptographic algorithms
License: FIXME
URL: http://github.com/Gozala/crypto/issues/
Source0: http://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

%{?nodejs_find_provides_and_requires}

%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}

%description
%{summary}

%prep
%setup -q -n package

%build
%nodejs_symlink_deps --build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr .md5.js.un~ .package.json.un~ .sha1.js.un~ History.md Readme.md md5.js package.json sha1.js test %{buildroot}%{nodejs_sitelib}/%{npm_name}
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc 
%doc .md5.js.un~
%doc History.md
%doc Readme.md

%changelog
* Thu Apr 27 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.0.3-1
- First release 
