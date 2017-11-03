%global npm_name mkdirp
%global enable_tests 0

%{?nodejs_find_provides_and_requires}

Name: nodejs-%{npm_name}
Version: 0.5.1
Release: 1
Summary: Recursively mkdir, like `mkdir -p`
License: MIT
URL: https://github.com/substack/node-mkdirp.git
Source0: http://registry.npmjs.org/mkdirp/-/mkdirp-0.5.1.tgz
Source1: http://registry.npmjs.org/minimist/-/minimist-0.0.8.tgz
Source2: mkdirp-0.5.1-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: bundled-npm(mkdirp) = 0.5.1
Provides: bundled-npm(minimist) = 0.0.8
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

%setup -T -q -a 2 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache . --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cd /tmp/node_modules/mkdirp
cp -pfr .travis.yml LICENSE bin examples index.js package.json readme.markdown test node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pf readme.markdown LICENSE ../../
# If any binaries are included, symlink them to bindir here
mkdir -p %{buildroot}%{nodejs_sitelib}/${npm_name}/bin 
mkdir -p %{buildroot}%{_bindir}/ 
install -p -D -m0755 bin/cmd.js %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/cmd.js
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/cmd.js %{buildroot}%{_bindir}/cmd.js


%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
#$CHECK
%endif

%files
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/cmd.js
%doc %{nodejs_sitelib}/%{npm_name}/LICENSE
%doc %{nodejs_sitelib}/%{npm_name}/readme.markdown

%changelog
* Thu Nov 2 2017 jess.portnoy@kaltura.com <Jess Portnoy> - 0.5.1-1
- First release 
