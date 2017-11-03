%global npm_name log4js
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.6.37
Release: 1
Summary: Port of Log4js to work with node
License: Apache-2.0
URL: http://github.com/nomiddlename/log4js-node/issues
Source0: http://registry.npmjs.org/log4js/-/log4js-0.6.37.tgz
Source1: http://registry.npmjs.org/readable-stream/-/readable-stream-1.0.34.tgz
Source2: http://registry.npmjs.org/semver/-/semver-4.3.6.tgz
Source3: http://registry.npmjs.org/string_decoder/-/string_decoder-0.10.31.tgz
Source4: http://registry.npmjs.org/core-util-is/-/core-util-is-1.0.2.tgz
Source5: http://registry.npmjs.org/inherits/-/inherits-2.0.3.tgz
Source6: http://registry.npmjs.org/isarray/-/isarray-0.0.1.tgz
Source7: log4js-0.6.37-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(log4js) = 0.6.37
Provides: bundled-npm(readable-stream) = 1.0.34
Provides: bundled-npm(semver) = 4.3.6
Provides: bundled-npm(string_decoder) = 0.10.31
Provides: bundled-npm(core-util-is) = 1.0.2
Provides: bundled-npm(inherits) = 2.0.3
Provides: bundled-npm(isarray) = 0.0.1
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

%setup -T -q -a 7 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd /tmp/node_modules/log4js
cp -pfr .bob.json .jshintrc .npmignore .travis.yml README.md LICENSE double-stack.js examples lib package.json test node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
#cp -pf README.md ../../
# If any binaries are included, symlink them to bindir here


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc /usr/lib/node_modules/log4js/README.md 
%doc /usr/lib/node_modules/log4js/LICENSE

%changelog
* Thu Nov 2 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.6.37-1
- First release 
