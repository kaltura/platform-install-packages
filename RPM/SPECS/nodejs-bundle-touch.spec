%global npm_name touch
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 1.0.0
Release: 1
Summary: like touch(1) in node
License: ISC
URL: FIXME
Source0: http://registry.npmjs.org/touch/-/touch-1.0.0.tgz
Source1: http://registry.npmjs.org/nopt/-/nopt-1.0.10.tgz
Source2: http://registry.npmjs.org/abbrev/-/abbrev-1.1.1.tgz
Source3: touch-1.0.0-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(touch) = 1.0.0
Provides: bundled-npm(nopt) = 1.0.10
Provides: bundled-npm(abbrev) = 1.1.1
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

%setup -T -q -a 3 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd /tmp/node_modules/touch
cp -pfr .npmignore .travis.yml LICENSE README.md bin package.json test touch.js node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf README.md LICENSE ../../
# If any binaries are included, symlink them to bindir here
mkdir -p %{buildroot}%{nodejs_sitelib}/${npm_name}/bin 
mkdir -p %{buildroot}%{_bindir}/ 
install -p -D -m0755 bin/touch.js %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/touch.js
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/touch.js %{buildroot}%{_bindir}/touch.js


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/touch.js
%doc %{nodejs_sitelib}/%{npm_name}/LICENSE
%doc %{nodejs_sitelib}/%{npm_name}/README.md

%changelog
* Fri Nov 3 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.0-1
- First release 
