%global npm_name body-parser
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 1.17.1
Release: 1
Summary: Node
License: MIT
URL: FIXME
Source0: http://registry.npmjs.org/body-parser/-/body-parser-1.17.1.tgz
Source1: http://registry.npmjs.org/debug/-/debug-2.6.1.tgz
Source2: http://registry.npmjs.org/bytes/-/bytes-2.4.0.tgz
Source3: http://registry.npmjs.org/content-type/-/content-type-1.0.2.tgz
Source4: http://registry.npmjs.org/depd/-/depd-1.1.1.tgz
Source5: http://registry.npmjs.org/iconv-lite/-/iconv-lite-0.4.15.tgz
Source6: http://registry.npmjs.org/http-errors/-/http-errors-1.6.1.tgz
Source7: http://registry.npmjs.org/on-finished/-/on-finished-2.3.0.tgz
Source8: http://registry.npmjs.org/qs/-/qs-6.4.0.tgz
Source9: http://registry.npmjs.org/ms/-/ms-0.7.2.tgz
Source10: http://registry.npmjs.org/type-is/-/type-is-1.6.15.tgz
Source11: http://registry.npmjs.org/depd/-/depd-1.1.0.tgz
Source12: http://registry.npmjs.org/raw-body/-/raw-body-2.2.0.tgz
Source13: http://registry.npmjs.org/inherits/-/inherits-2.0.3.tgz
Source14: http://registry.npmjs.org/setprototypeof/-/setprototypeof-1.0.3.tgz
Source15: http://registry.npmjs.org/statuses/-/statuses-1.3.1.tgz
Source16: http://registry.npmjs.org/ee-first/-/ee-first-1.1.1.tgz
Source17: http://registry.npmjs.org/mime-types/-/mime-types-2.1.16.tgz
Source18: http://registry.npmjs.org/media-typer/-/media-typer-0.3.0.tgz
Source19: http://registry.npmjs.org/mime-db/-/mime-db-1.29.0.tgz
Source20: http://registry.npmjs.org/unpipe/-/unpipe-1.0.0.tgz
Source21: body-parser-1.17.1-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(body-parser) = 1.17.1
Provides: bundled-npm(debug) = 2.6.1
Provides: bundled-npm(bytes) = 2.4.0
Provides: bundled-npm(content-type) = 1.0.2
Provides: bundled-npm(depd) = 1.1.1
Provides: bundled-npm(iconv-lite) = 0.4.15
Provides: bundled-npm(http-errors) = 1.6.1
Provides: bundled-npm(on-finished) = 2.3.0
Provides: bundled-npm(qs) = 6.4.0
Provides: bundled-npm(ms) = 0.7.2
Provides: bundled-npm(type-is) = 1.6.15
Provides: bundled-npm(depd) = 1.1.0
Provides: bundled-npm(raw-body) = 2.2.0
Provides: bundled-npm(inherits) = 2.0.3
Provides: bundled-npm(setprototypeof) = 1.0.3
Provides: bundled-npm(statuses) = 1.3.1
Provides: bundled-npm(ee-first) = 1.1.1
Provides: bundled-npm(mime-types) = 2.1.16
Provides: bundled-npm(media-typer) = 0.3.0
Provides: bundled-npm(mime-db) = 1.29.0
Provides: bundled-npm(unpipe) = 1.0.0
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

%setup -T -q -a 21 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/body-parser
cp -pfr HISTORY.md LICENSE README.md index.js lib package.json node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
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
* Wed Aug 2 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.17.1-1
- First release 
