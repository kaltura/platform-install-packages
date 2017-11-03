%global npm_name q-io
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 1.13.4
Release: 1
Summary: IO using Q promises
License: MIT
URL: http://github.com/kriskowal/q-io/
Source0: http://registry.npmjs.org/q-io/-/q-io-1.13.4.tgz
Source1: http://registry.npmjs.org/collections/-/collections-0.2.2.tgz
Source2: http://registry.npmjs.org/mime/-/mime-1.4.1.tgz
Source3: http://registry.npmjs.org/qs/-/qs-6.5.1.tgz
Source4: http://registry.npmjs.org/q/-/q-1.5.1.tgz
Source5: http://registry.npmjs.org/mimeparse/-/mimeparse-0.1.4.tgz
Source6: http://registry.npmjs.org/weak-map/-/weak-map-1.0.0.tgz
Source7: http://registry.npmjs.org/url2/-/url2-0.0.0.tgz
Source8: q-io-1.13.4-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(q-io) = 1.13.4
Provides: bundled-npm(collections) = 0.2.2
Provides: bundled-npm(mime) = 1.4.1
Provides: bundled-npm(qs) = 6.5.1
Provides: bundled-npm(q) = 1.5.1
Provides: bundled-npm(mimeparse) = 0.1.4
Provides: bundled-npm(weak-map) = 1.0.0
Provides: bundled-npm(url2) = 0.0.0
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

%setup -T -q -a 8 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd /tmp/node_modules/q-io
cp -pfr .gitattributes .npmignore .travis.yml CHANGES.md LICENSE README.md buffer-stream.js coverage-report.js deprecate.js fs-boot.js fs-common.js fs-mock.js fs-root.js fs.js fs2http.js http-apps http-apps.js http-cookie.js http.js package.json reader.js writer.js node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
#cp -pf CHANGES.md README.md LICENSE ../../
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc %{nodejs_sitelib}/%{npm_name}/LICENSE
%doc %{nodejs_sitelib}/%{npm_name}/CHANGES.md
%doc %{nodejs_sitelib}/%{npm_name}/README.md

%changelog
* Thu Nov 2 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.13.4-1
- First release 
