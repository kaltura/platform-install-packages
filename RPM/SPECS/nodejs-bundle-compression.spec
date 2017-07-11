%global npm_name compression
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 1.6.2
Release: 1
Summary: Node
License: MIT
URL: FIXME
Source0: http://registry.npmjs.org/compression/-/compression-1.6.2.tgz
Source1: http://registry.npmjs.org/bytes/-/bytes-2.3.0.tgz
Source2: http://registry.npmjs.org/accepts/-/accepts-1.3.3.tgz
Source3: http://registry.npmjs.org/compressible/-/compressible-2.0.10.tgz
Source4: http://registry.npmjs.org/debug/-/debug-2.2.0.tgz
Source5: http://registry.npmjs.org/vary/-/vary-1.1.1.tgz
Source6: http://registry.npmjs.org/on-headers/-/on-headers-1.0.1.tgz
Source7: http://registry.npmjs.org/mime-types/-/mime-types-2.1.15.tgz
Source8: http://registry.npmjs.org/negotiator/-/negotiator-0.6.1.tgz
Source9: http://registry.npmjs.org/ms/-/ms-0.7.1.tgz
Source10: http://registry.npmjs.org/mime-db/-/mime-db-1.28.0.tgz
Source11: http://registry.npmjs.org/mime-db/-/mime-db-1.27.0.tgz
Source12: compression-1.6.2-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(compression) = 1.6.2
Provides: bundled-npm(bytes) = 2.3.0
Provides: bundled-npm(accepts) = 1.3.3
Provides: bundled-npm(compressible) = 2.0.10
Provides: bundled-npm(debug) = 2.2.0
Provides: bundled-npm(vary) = 1.1.1
Provides: bundled-npm(on-headers) = 1.0.1
Provides: bundled-npm(mime-types) = 2.1.15
Provides: bundled-npm(negotiator) = 0.6.1
Provides: bundled-npm(ms) = 0.7.1
Provides: bundled-npm(mime-db) = 1.28.0
Provides: bundled-npm(mime-db) = 1.27.0
AutoReq: no 
AutoProv: no 


%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}

%description
%{summary}

%prep
mkdir -p %{npm_cache_dir}
for tgz in %{sources}; do
  echo $tgz | grep -q registry.npmjs.org || npm cache add --cache ./%{npm_cache_dir} $tgz
done

%setup -T -q -a 12 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/compression
cp -pfr HISTORY.md LICENSE README.md index.js package.json node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf HISTORY.md README.md LICENSE ../../
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc LICENSE
%doc HISTORY.md
%doc README.md

%changelog
* Wed Jun 21 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.6.2-1
- First release 
