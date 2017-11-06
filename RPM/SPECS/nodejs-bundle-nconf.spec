%global npm_name nconf
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.8.4
Release: 1
Summary: Hierarchical node
License: MIT
URL: http://github.com/flatiron/nconf.git
Source0: http://registry.npmjs.org/nconf/-/nconf-0.8.4.tgz
Source1: http://registry.npmjs.org/ini/-/ini-1.3.4.tgz
Source2: http://registry.npmjs.org/async/-/async-1.5.2.tgz
Source3: http://registry.npmjs.org/secure-keys/-/secure-keys-1.0.0.tgz
Source4: http://registry.npmjs.org/yargs/-/yargs-3.32.0.tgz
Source5: http://registry.npmjs.org/camelcase/-/camelcase-2.1.1.tgz
Source6: http://registry.npmjs.org/decamelize/-/decamelize-1.2.0.tgz
Source7: http://registry.npmjs.org/os-locale/-/os-locale-1.4.0.tgz
Source8: http://registry.npmjs.org/cliui/-/cliui-3.2.0.tgz
Source9: http://registry.npmjs.org/y18n/-/y18n-3.2.1.tgz
Source10: http://registry.npmjs.org/string-width/-/string-width-1.0.2.tgz
Source11: http://registry.npmjs.org/window-size/-/window-size-0.1.4.tgz
Source12: http://registry.npmjs.org/lcid/-/lcid-1.0.0.tgz
Source13: http://registry.npmjs.org/strip-ansi/-/strip-ansi-3.0.1.tgz
Source14: http://registry.npmjs.org/wrap-ansi/-/wrap-ansi-2.1.0.tgz
Source15: http://registry.npmjs.org/invert-kv/-/invert-kv-1.0.0.tgz
Source16: http://registry.npmjs.org/code-point-at/-/code-point-at-1.1.0.tgz
Source17: http://registry.npmjs.org/is-fullwidth-code-point/-/is-fullwidth-code-point-1.0.0.tgz
Source18: http://registry.npmjs.org/ansi-regex/-/ansi-regex-2.1.1.tgz
Source19: http://registry.npmjs.org/number-is-nan/-/number-is-nan-1.0.1.tgz
Source20: nconf-0.8.4-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(nconf) = 0.8.4
Provides: bundled-npm(ini) = 1.3.4
Provides: bundled-npm(async) = 1.5.2
Provides: bundled-npm(secure-keys) = 1.0.0
Provides: bundled-npm(yargs) = 3.32.0
Provides: bundled-npm(camelcase) = 2.1.1
Provides: bundled-npm(decamelize) = 1.2.0
Provides: bundled-npm(os-locale) = 1.4.0
Provides: bundled-npm(cliui) = 3.2.0
Provides: bundled-npm(y18n) = 3.2.1
Provides: bundled-npm(string-width) = 1.0.2
Provides: bundled-npm(window-size) = 0.1.4
Provides: bundled-npm(lcid) = 1.0.0
Provides: bundled-npm(strip-ansi) = 3.0.1
Provides: bundled-npm(wrap-ansi) = 2.1.0
Provides: bundled-npm(invert-kv) = 1.0.0
Provides: bundled-npm(code-point-at) = 1.1.0
Provides: bundled-npm(is-fullwidth-code-point) = 1.0.0
Provides: bundled-npm(ansi-regex) = 2.1.1
Provides: bundled-npm(number-is-nan) = 1.0.1
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

%setup -T -q -a 20 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd /tmp/node_modules/nconf
cp -pfr .npmignore .travis.yml CHANGELOG.md LICENSE README.md lib package.json test usage.js node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
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
%doc %{nodejs_sitelib}/%{npm_name}/CHANGELOG.md
%doc %{nodejs_sitelib}/%{npm_name}/README.md

%changelog
* Mon Nov 6 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.8.4-1
- First release 
