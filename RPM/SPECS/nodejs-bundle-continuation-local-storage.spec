%global npm_name continuation-local-storage
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 3.2.0
Release: 1
Summary: userland implementation of https://github
License: BSD-2-Clause
URL: https://github.com/othiym23/node-continuation-local-storage.git
Source0: http://registry.npmjs.org/continuation-local-storage/-/continuation-local-storage-3.2.0.tgz
Source1: http://registry.npmjs.org/emitter-listener/-/emitter-listener-1.0.1.tgz
Source2: http://registry.npmjs.org/async-listener/-/async-listener-0.6.5.tgz
Source3: http://registry.npmjs.org/shimmer/-/shimmer-1.0.0.tgz
Source4: http://registry.npmjs.org/shimmer/-/shimmer-1.1.0.tgz
Source5: http://registry.npmjs.org/semver/-/semver-5.3.0.tgz
Source6: continuation-local-storage-3.2.0-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(continuation-local-storage) = 3.2.0
Provides: bundled-npm(emitter-listener) = 1.0.1
Provides: bundled-npm(async-listener) = 0.6.5
Provides: bundled-npm(shimmer) = 1.0.0
Provides: bundled-npm(shimmer) = 1.1.0
Provides: bundled-npm(semver) = 5.3.0
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

%setup -T -q -a 6 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd node_modules/continuation-local-storage
cp -pfr .eslintrc .npmignore .travis.yml CHANGELOG.md LICENSE README.md context.js package.json test node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf CHANGELOG.md README.md LICENSE ../../
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
%doc CHANGELOG.md
%doc README.md

%changelog
* Thu Apr 27 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 3.2.0-1
- First release 
